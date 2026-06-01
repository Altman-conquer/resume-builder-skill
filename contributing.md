# Contributing

Contributions are welcome when they improve the `chinese-resume-builder` skill, its template index, or its utility scripts.

## Template Index Changes

When adding or updating a template in `skills/chinese-resume-builder/references/templates.json`, include:

- stable `id`;
- template `name`;
- upstream `url`;
- `category`;
- original `source`;
- intended `audience`;
- expected `build` tool;
- `license` metadata;
- `vendored: false` unless redistribution has been explicitly reviewed.

Do not add third-party template source files unless their license clearly permits redistribution and attribution requirements are preserved.

## Skill Changes

Keep `SKILL.md` concise. Move detailed guidance into `references/` and repeatable automation into `scripts/`.

Run these checks before opening a PR:

```bash
python3 -m unittest discover -s tests
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/chinese-resume-builder
```
