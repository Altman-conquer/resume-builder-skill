import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "chinese-resume-builder"


def run_script(name, *args):
    return subprocess.run(
        [sys.executable, str(SKILL_DIR / "scripts" / name), *args],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    frontmatter = text.split("---\n", 2)[1]
    result = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"')
    return result


class SkillPackageTests(unittest.TestCase):
    def test_skill_metadata_is_valid(self):
        metadata = parse_frontmatter(SKILL_DIR / "SKILL.md")

        self.assertEqual(metadata["name"], "chinese-resume-builder")
        self.assertIn("中文简历", metadata["description"])
        self.assertIn("LaTeX", metadata["description"])
        self.assertIn("license", metadata["description"])

    def test_agent_metadata_exists(self):
        text = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertIn('display_name: "Chinese Resume Builder"', text)
        self.assertIn("$chinese-resume-builder", text)

    def test_template_index_has_required_fields(self):
        data = json.loads(
            (SKILL_DIR / "references" / "templates.json").read_text(encoding="utf-8")
        )

        self.assertGreaterEqual(len(data["templates"]), 20)
        categories = {entry["category"] for entry in data["templates"]}
        self.assertIn("latex", categories)
        self.assertIn("html-js", categories)
        self.assertIn("typst", categories)

        for entry in data["templates"]:
            for field in ("id", "name", "url", "category", "source", "license"):
                self.assertIn(field, entry)
            self.assertFalse(entry.get("vendored", False), entry["id"])

    def test_inspect_template_repo_outputs_github_metadata(self):
        result = run_script(
            "inspect_template_repo.py",
            "--url",
            "https://github.com/dyweb/Deedy-Resume-for-Chinese",
        )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["host"], "github.com")
        self.assertEqual(payload["owner"], "dyweb")
        self.assertEqual(payload["repo"], "Deedy-Resume-for-Chinese")
        self.assertTrue(payload["license_api_url"].endswith("/license"))

    def test_fetch_template_dry_run_prints_safe_clone_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_script(
                "fetch_template.py",
                "--dry-run",
                "--repo",
                "https://github.com/dyweb/Deedy-Resume-for-Chinese",
                "--dest",
                str(Path(tmp) / "deedy"),
            )

        self.assertIn("git clone --depth 1", result.stdout)
        self.assertIn("Deedy-Resume-for-Chinese", result.stdout)

    def test_compile_resume_dry_run_detects_xelatex(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "resume.tex").write_text(
                "% !TEX TS-program = xelatex\n\\documentclass{resume}\n",
                encoding="utf-8",
            )
            (project / "resume.cls").write_text("", encoding="utf-8")

            result = run_script("compile_resume.py", "--dry-run", str(project))

        self.assertIn("xelatex", result.stdout)
        self.assertIn("resume.tex", result.stdout)


if __name__ == "__main__":
    unittest.main()
