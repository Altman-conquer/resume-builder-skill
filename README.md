# resume-builder-skill

A Codex skill for building polished Chinese resumes from curated open-source templates.

This repository packages a `chinese-resume-builder` skill. The skill keeps a machine-readable index of Chinese-friendly resume templates, helps Codex choose a template for a user's target role, checks upstream license information before use, fetches templates on demand, and assists with content migration, compilation, and final resume review.

The template index is based on the original curated list in [dyweb/awesome-resume-for-chinese](https://github.com/dyweb/awesome-resume-for-chinese), extended with metadata that makes the list useful for automated template selection.

## Features

- Recommend Chinese resume templates by role, seniority, format, and toolchain.
- Support LaTeX, Typst, Markdown, HTML/JS, Jekyll, and JSON Resume workflows.
- Keep third-party templates as external upstream projects instead of vendoring their source.
- Check and preserve upstream license and attribution before using a template.
- Fetch selected templates with a safe, explicit `git clone --depth 1` workflow.
- Detect common build commands for LaTeX, Typst, Node, and Markdown-based resumes.
- Guide Codex through Chinese resume writing, content migration, layout review, and privacy checks.

## Repository Layout

```text
resume-builder-skill/
├── README.md
├── LICENSE
├── contributing.md
├── tests/
│   └── test_skill_package.py
└── skills/
    └── chinese-resume-builder/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── references/
        │   ├── license-checklist.md
        │   ├── resume-writing-guide.md
        │   ├── selection-guide.md
        │   └── templates.json
        └── scripts/
            ├── compile_resume.py
            ├── fetch_template.py
            └── inspect_template_repo.py
```

## Installation

Clone this repository:

```bash
git clone https://github.com/Altman-conquer/resume-builder-skill.git
```

Install the skill into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -r resume-builder-skill/skills/chinese-resume-builder "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart Codex after installation.

## Usage

After installation, ask Codex for Chinese resume tasks such as:

```text
Use $chinese-resume-builder to choose a LaTeX Chinese resume template for a new-grad algorithm engineer.
```

```text
Use $chinese-resume-builder to convert my existing Markdown resume into a one-page Chinese LaTeX resume.
```

```text
Use $chinese-resume-builder to inspect this template repo, verify its license, fetch it, and compile a sample resume.
```

```text
Use $chinese-resume-builder to review my Chinese resume for content density, wording, privacy, and layout issues.
```

Codex will read the skill instructions, inspect the indexed templates, recommend suitable options, verify license requirements, fetch the selected template when needed, and help produce a resume artifact.

## Included Utilities

Inspect a template repository URL:

```bash
python3 skills/chinese-resume-builder/scripts/inspect_template_repo.py \
  --url https://github.com/dyweb/Deedy-Resume-for-Chinese
```

Dry-run a safe fetch command:

```bash
python3 skills/chinese-resume-builder/scripts/fetch_template.py \
  --dry-run \
  --repo https://github.com/dyweb/Deedy-Resume-for-Chinese \
  --dest ./work/deedy-resume
```

Detect a resume build command:

```bash
python3 skills/chinese-resume-builder/scripts/compile_resume.py --dry-run ./work/deedy-resume
```

## Template Policy

The repository does not copy third-party template source code by default. Template entries point to upstream projects and preserve author attribution.

When using a template, Codex should:

- inspect the upstream repository or project page;
- confirm license and attribution requirements;
- avoid copying templates with unclear redistribution terms;
- keep upstream notices intact;
- fetch source only into the user's chosen workspace.

## Development

Run the test suite:

```bash
python3 -m unittest discover -s tests
```

Validate the skill package:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  skills/chinese-resume-builder
```

## Contributing

Template index improvements are welcome. A template entry should include its name, URL, category, source, intended audience, build tool, and license metadata.

For third-party templates, do not add vendored source files unless the upstream license explicitly allows redistribution and the attribution requirements are preserved.

## License

The skill code, scripts, and original documentation in this repository are licensed under the MIT License.

Third-party templates, fonts, screenshots, and examples remain under their original upstream licenses.
