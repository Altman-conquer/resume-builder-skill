---
name: chinese-resume-builder
description: Build, migrate, review, and compile 中文简历 / Chinese resumes using curated open-source templates. Use when Codex needs to choose a Chinese-friendly resume template, work with LaTeX/Typst/Markdown/HTML resume files, inspect template license terms, fetch an upstream template, adapt resume content for Chinese job applications, or troubleshoot resume compilation and layout issues.
---

# Chinese Resume Builder

## Core Workflow

1. Clarify the user's target: role, seniority, language, output format, page count, and whether the resume is for industry, research, internship, or graduate school.
2. Read `references/templates.json` and shortlist 2-3 templates that match the target.
3. Read `references/selection-guide.md` when trade-offs between template families matter.
4. Inspect license and attribution requirements before fetching or copying any third-party template. Use `references/license-checklist.md` and `scripts/inspect_template_repo.py`.
5. Fetch the selected template only into the user's workspace. Prefer `scripts/fetch_template.py` for Git repositories.
6. Migrate the user's content into the selected template. Use `references/resume-writing-guide.md` for Chinese resume phrasing and section-density guidance.
7. Compile or preview the resume. Use `scripts/compile_resume.py` to detect common build commands, then inspect output for page count, overflow, font issues, broken links, and private information.

## Template Selection

Prefer templates with clear build steps, active upstream repositories, and explicit license metadata. Match the template to the candidate rather than choosing only by appearance:

- LaTeX: best for one-page technical resumes, academic resumes, strict typography, and PDF-first delivery.
- Typst: best when the user wants LaTeX-like output with simpler syntax.
- Markdown or Pandoc: best when the user wants content-first editing and multiple export formats.
- HTML/JS: best when the user wants an online resume, interactive page, or web portfolio.
- JSON Resume: best when structured resume data should feed multiple themes.

Avoid templates with unclear redistribution terms unless the user only needs an external link and will review the license manually.

## License Handling

Treat the template index as metadata, not as permission to redistribute third-party files. Before using a template:

- inspect the upstream license or project page;
- preserve upstream copyright and attribution;
- keep original license files with copied template sources;
- do not vendor templates, fonts, screenshots, or examples with unclear license terms;
- clearly separate this skill's MIT-licensed files from third-party template assets.

If license details are missing, explain the uncertainty and either choose another template or ask the user whether to proceed with an external-link-only workflow.

## Content Migration

When adapting a resume:

- keep high-signal achievements and remove vague self-evaluation;
- prefer action, method, result, and metric in each bullet;
- compress repeated technology lists into section-specific evidence;
- keep contact information minimal and privacy-aware;
- verify all links before final delivery;
- fit industry resumes to one page unless the user explicitly wants a longer CV.

## Scripts

Use bundled scripts for repeatable steps:

- `scripts/inspect_template_repo.py --url <repo-url>`: normalize a template URL and print host/license metadata.
- `scripts/fetch_template.py --repo <repo-url> --dest <path>`: clone a template repository safely.
- `scripts/compile_resume.py [--dry-run] <project-dir>`: detect and optionally run a build command for common resume projects.

Prefer `--dry-run` before running commands that fetch dependencies, clone repositories, or compile files.
