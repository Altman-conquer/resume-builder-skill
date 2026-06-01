# resume-builder-skill

一个面向中文简历制作的 Codex Skill。它基于开源中文简历模板索引，帮助 Codex 为用户选择模板、检查授权、按需拉取模板、迁移简历内容、编译输出，并进行最终版面与隐私检查。

本仓库提供的实际 skill 名称是 `chinese-resume-builder`。模板索引主要参考 [dyweb/awesome-resume-for-chinese](https://github.com/dyweb/awesome-resume-for-chinese)，并补充了模板类型、适用场景、构建方式和授权检查信息，方便自动化选择。

## 功能

- 根据岗位、经验阶段、简历格式和工具链推荐中文简历模板。
- 支持 LaTeX、Typst、Markdown、HTML/JS、Jekyll 和 JSON Resume 工作流。
- 默认不打包第三方模板源码，而是保留上游链接和作者信息。
- 使用模板前检查并保留上游 license 与 attribution。
- 通过明确的 `git clone --depth 1` 流程按需拉取模板。
- 自动识别常见 LaTeX、Typst、Node、Markdown 简历项目的构建命令。
- 指导 Codex 完成中文简历内容改写、模板迁移、版面检查和隐私检查。

## 仓库结构

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

## 安装

克隆仓库：

```bash
git clone https://github.com/Altman-conquer/resume-builder-skill.git
```

安装到 Codex skills 目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -r resume-builder-skill/skills/chinese-resume-builder "${CODEX_HOME:-$HOME/.codex}/skills/"
```

安装完成后重启 Codex。

## 使用方式

安装后，可以直接向 Codex 提出中文简历相关请求：

```text
使用 $chinese-resume-builder 帮我选择一个适合应届算法工程师的 LaTeX 中文简历模板。
```

```text
使用 $chinese-resume-builder 把我现有的 Markdown 简历改成一页纸中文 LaTeX 简历。
```

```text
使用 $chinese-resume-builder 检查这个模板仓库的 license，确认能否拉取并编译示例简历。
```

```text
使用 $chinese-resume-builder 检查我的中文简历内容密度、措辞、隐私信息和版面问题。
```

Codex 会读取 skill 说明、查看模板索引、推荐合适模板、检查授权要求、按需拉取模板，并协助生成最终简历文件。

## 工具脚本

检查模板仓库 URL：

```bash
python3 skills/chinese-resume-builder/scripts/inspect_template_repo.py \
  --url https://github.com/dyweb/Deedy-Resume-for-Chinese
```

预览安全拉取命令：

```bash
python3 skills/chinese-resume-builder/scripts/fetch_template.py \
  --dry-run \
  --repo https://github.com/dyweb/Deedy-Resume-for-Chinese \
  --dest ./work/deedy-resume
```

检测简历项目构建命令：

```bash
python3 skills/chinese-resume-builder/scripts/compile_resume.py --dry-run ./work/deedy-resume
```

## 模板授权策略

本仓库默认不复制第三方模板源码。模板条目只指向上游项目，并保留作者与来源信息。

使用模板时，Codex 应当：

- 检查上游仓库或项目主页；
- 确认 license 和 attribution 要求；
- 避免复制授权不明确的模板源码；
- 保留上游版权声明和 license 文件；
- 只把模板源码拉取到用户指定的工作区。

## 开发

运行测试：

```bash
python3 -m unittest discover -s tests
```

校验 skill 结构：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  skills/chinese-resume-builder
```

## 贡献

欢迎改进模板索引、skill 指南和工具脚本。

新增模板条目时，请至少提供：

- 模板名称；
- 上游链接；
- 模板类型；
- 来源；
- 适用人群；
- 构建工具；
- license 信息；
- 是否 vendored。默认应为 `false`。

除非上游 license 明确允许再分发，并且已经保留 attribution 要求，否则不要把第三方模板源码直接加入本仓库。

## License

本仓库中的 skill 代码、脚本和原创文档使用 MIT License。

第三方模板、字体、截图和示例内容仍归各自上游项目所有，并遵循对应项目的 license。

---

## English

`resume-builder-skill` provides a Codex skill named `chinese-resume-builder` for building Chinese resumes from curated open-source templates.

It indexes Chinese-friendly resume templates, recommends suitable options by role and format, checks upstream license requirements, fetches selected templates on demand, helps migrate resume content, detects common build commands, and reviews the final resume for layout and privacy issues.

### Install

```bash
git clone https://github.com/Altman-conquer/resume-builder-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -r resume-builder-skill/skills/chinese-resume-builder "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart Codex after installation.

### Example Prompts

```text
Use $chinese-resume-builder to choose a LaTeX Chinese resume template for a new-grad algorithm engineer.
```

```text
Use $chinese-resume-builder to convert my existing Markdown resume into a one-page Chinese LaTeX resume.
```

```text
Use $chinese-resume-builder to inspect a template repository, verify its license, fetch it, and compile a sample resume.
```

The skill code, scripts, and original documentation are licensed under the MIT License. Third-party templates remain under their upstream licenses.
