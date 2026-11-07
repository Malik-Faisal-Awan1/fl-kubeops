"""Tests for tools/docs.py. Run: make test-tools"""
import tempfile
import textwrap
import unittest
from pathlib import Path

import docs  # tools/docs.py (unittest discover -s tools puts this directory on sys.path)

BASE_TOML = textwrap.dedent(
    """
    [project]
    name = "X"
    sprint = "S"
    sprint_status = "IN PROGRESS"
    sprint_dates = "d"
    objective = "o"
    capacity = "c"
    out_of_scope = ["a"]
    [[path]]
    path = "app"
    purpose = "app"
    [[path]]
    path = "docs"
    purpose = "docs"
    [[state]]
    label = "Code"
    glob = "app/src/**/*.py"
    kind = "code"
    [[command]]
    cmd = "make docs"
    target = "docs"
    purpose = "p"
    [[decision]]
    topic = "Ruff"
    value = "v"
    short = "ruff 1.0.0"
    pins = ["ruff==1.0.0"]
    [[blocked]]
    name = "grpcio-tools"
    until = "Sprint 4"
    why = "later"
    [[person]]
    name = "N"
    role = "R"
    stories = "S"
    [[task]]
    title = "t"
    owner = "o"
    done = false
    evidence = ["app/x.txt"]
    """
)


def block(name):
    return f"<!-- BEGIN GENERATED:{name} -->\n<!-- END GENERATED:{name} -->\n"


def make_repo(extra_toml="", with_docs=True):
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    (root / "app" / "src").mkdir(parents=True)
    (root / "project.toml").write_text(BASE_TOML + extra_toml, encoding="utf-8")
    (root / "Makefile").write_text("docs:\n\ttrue\n", encoding="utf-8")
    if with_docs:
        for rel, names in docs.TARGETS.items():
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("".join(block(n) for n in names), encoding="utf-8")
    return tmp, root


class DocsTests(unittest.TestCase):
    def test_real_repo_is_in_sync(self):
        errors, _ = docs.run(docs.ROOT, write=False)
        self.assertEqual(errors, [])

    def test_write_then_check_is_clean_and_idempotent(self):
        tmp, root = make_repo()
        with tmp:
            errors, updated = docs.run(root, write=True)
            self.assertEqual(errors, [])
            self.assertTrue(updated)
            errors, updated = docs.run(root, write=False)
            self.assertEqual(errors, [])
            errors, updated = docs.run(root, write=True)
            self.assertEqual(updated, [])

    def test_stale_docs_are_detected_after_state_change(self):
        tmp, root = make_repo()
        with tmp:
            docs.run(root, write=True)
            (root / "app" / "src" / "main.py").write_text("x = 1\n", encoding="utf-8")
            errors, _ = docs.run(root, write=False)
            self.assertTrue(any("out of date" in e for e in errors))
            docs.run(root, write=True)
            self.assertIn("present", (root / "AGENTS.md").read_text(encoding="utf-8"))

    def test_hand_edit_inside_markers_is_reverted(self):
        tmp, root = make_repo()
        with tmp:
            docs.run(root, write=True)
            p = root / "README.md"
            p.write_text(p.read_text(encoding="utf-8").replace("ruff 1.0.0", "ruff 9.9.9"), encoding="utf-8")
            errors, _ = docs.run(root, write=False)
            self.assertTrue(any("out of date" in e for e in errors))

    def test_pin_mismatch_is_detected(self):
        tmp, root = make_repo()
        with tmp:
            docs.run(root, write=True)
            (root / "app" / "pyproject.toml").write_text('dependencies = ["ruff==0.9.0"]\n', encoding="utf-8")
            errors, _ = docs.run(root, write=False)
            self.assertTrue(any("ruff==0.9.0" in e for e in errors))

    def test_matching_pin_and_local_version_suffix_ok(self):
        tmp, root = make_repo()
        with tmp:
            docs.run(root, write=True)
            (root / "app" / "requirements.lock").write_text("ruff==1.0.0 \\\n    --hash=sha256:abc\n", encoding="utf-8")
            errors, _ = docs.run(root, write=False)
            self.assertEqual(errors, [])

    def test_blocked_package_is_detected_but_comment_is_ignored(self):
        tmp, root = make_repo()
        with tmp:
            docs.run(root, write=True)
            (root / "app" / "requirements.txt").write_text("# grpcio-tools later\n", encoding="utf-8")
            self.assertEqual(docs.run(root, write=False)[0], [])
            (root / "app" / "requirements.txt").write_text("grpcio_tools==1.0\n", encoding="utf-8")
            errors, _ = docs.run(root, write=False)
            self.assertTrue(any("blocked package" in e for e in errors))

    def test_undeclared_top_level_folder_is_detected(self):
        tmp, root = make_repo()
        with tmp:
            docs.run(root, write=True)
            (root / "random").mkdir()
            errors, _ = docs.run(root, write=False)
            self.assertTrue(any("undeclared top-level folder 'random/'" in e for e in errors))

    def test_unpinned_action_latest_runner_and_missing_permissions(self):
        tmp, root = make_repo()
        with tmp:
            docs.run(root, write=True)
            wf = root / ".github" / "workflows"
            wf.mkdir(parents=True)
            (wf / "bad.yml").write_text(
                "on: push\njobs:\n  j:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n",
                encoding="utf-8",
            )
            errors, _ = docs.run(root, write=False)
            joined = "\n".join(errors)
            self.assertIn("not pinned to a full 40-char commit SHA", joined)
            self.assertIn("'-latest' runner", joined)
            self.assertIn("missing top-level 'permissions:'", joined)

    def test_pinned_action_with_permissions_passes(self):
        tmp, root = make_repo()
        with tmp:
            docs.run(root, write=True)
            wf = root / ".github" / "workflows"
            wf.mkdir(parents=True)
            sha = "a" * 40
            (wf / "ok.yml").write_text(
                f"on: push\npermissions:\n  contents: read\njobs:\n  j:\n    runs-on: ubuntu-24.04\n"
                f"    steps:\n      - uses: actions/checkout@{sha} # v1\n",
                encoding="utf-8",
            )
            self.assertEqual(docs.run(root, write=False)[0], [])

    def test_done_task_without_evidence_is_rejected(self):
        tmp, root = make_repo()
        with tmp:
            toml = (root / "project.toml").read_text(encoding="utf-8").replace("done = false", "done = true")
            (root / "project.toml").write_text(toml, encoding="utf-8")
            errors, _ = docs.run(root, write=True)
            self.assertTrue(any("marked done but evidence" in e for e in errors))
            (root / "app" / "x.txt").write_text("ok", encoding="utf-8")
            docs.run(root, write=True)
            self.assertEqual(docs.run(root, write=False)[0], [])

    def test_missing_marker_is_reported(self):
        tmp, root = make_repo()
        with tmp:
            (root / "README.md").write_text("no markers\n", encoding="utf-8")
            errors, _ = docs.run(root, write=False)
            self.assertTrue(any("missing block" in e for e in errors))

    def test_command_listed_only_if_makefile_target_exists(self):
        tmp, root = make_repo()
        with tmp:
            docs.run(root, write=True)
            self.assertIn("make docs", (root / "README.md").read_text(encoding="utf-8"))
            (root / "Makefile").write_text("other:\n\ttrue\n", encoding="utf-8")
            docs.run(root, write=True)
            self.assertIn("No commands exist yet", (root / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
