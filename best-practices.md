# Python 开源项目最佳实践清单

> 本文档由 Lindsey Zhang 在学习 `cookiecutter-pywf_open_source` 模板时整理。
> 70 个最佳实践点，覆盖从项目骨架到发布运营的每一个环节。
> 每个点回答三个问题：**是什么 / 为什么 / 在我项目里**。

---

## 阅读说明

- ✅ = 你项目已实现
- ⚠️ = 部分实现 / 待完善
- ❌ = 未实现 / 待添加
- 📌 = 高优先级 (mentor 已点名)

**学习方法：** 不要一次读完。每周挑一个章节深入，亲手在自己项目里做一遍。

---

## 目录

1. [项目结构](#1-项目结构) (5)
2. [包元数据 / pyproject.toml](#2-包元数据--pyprojecttoml) (8)
3. [依赖管理](#3-依赖管理) (5)
4. [测试](#4-测试) (7)
5. [代码覆盖率](#5-代码覆盖率) (4)
6. [文档系统](#6-文档系统) (7)
7. [CI/CD](#7-cicd) (6)
8. [版本控制 / Git](#8-版本控制--git) (6)
9. [包发布 / PyPI](#9-包发布--pypi) (5)
10. [外部服务集成](#10-外部服务集成) (4)
11. [代码质量](#11-代码质量) (5)
12. [开源协作规范](#12-开源协作规范) (5)
13. [进阶实践](#13-进阶实践) (5)

---

## 1. 项目结构

### 1.1 ✅ 包目录与项目目录分离 (`pkg/` vs `pkg-project/`)
- **是什么：** 仓库叫 `lindsey_learn_open_source_101-project`，包叫 `lindsey_learn_open_source_101`。
- **为什么：** 仓库根除了代码还要放 README/LICENSE/tests/docs/CI 配置，全混在一起会乱。`-project` 后缀让人一眼知道这是仓库不是包。
- **状态：** ✅

### 1.2 ✅ 测试目录在仓库根，不在包里
- **是什么：** `tests/` 与 `lindsey_learn_open_source_101/` 平级，不是 `lindsey_learn_open_source_101/tests/`。
- **为什么：** 测试代码不该被打包进 wheel 给用户。pyproject.toml 的 `exclude` 也排除了。
- **状态：** ✅ 见 [pyproject.toml:71-73](pyproject.toml)

### 1.3 ✅ 包内 `tests/helper.py` 提供测试辅助
- **是什么：** 包内有 `lindsey_learn_open_source_101/tests/helper.py`，给外部 `tests/test_*.py` 复用。
- **为什么：** 跑覆盖率、找 root_dir 等逻辑很烦，集中在一处。
- **状态：** ✅ 见 [lindsey_learn_open_source_101/tests/helper.py](lindsey_learn_open_source_101/tests/helper.py)

### 1.4 ✅ `vendor/` 存放第三方代码副本
- **是什么：** `pytest_cov_helper.py` 是从外部库抄过来的（带 `__version__ = "0.2.1"`）。
- **为什么：** 避免为了一个小工具引入整个外部依赖；可控、可审计。
- **状态：** ✅ 见 [lindsey_learn_open_source_101/vendor/pytest_cov_helper.py](lindsey_learn_open_source_101/vendor/pytest_cov_helper.py)

### 1.5 ✅ `paths.py` 集中管理路径
- **是什么：** 用 `PathEnum` 类把项目所有目录路径用 `pathlib.Path` 集中管理。
- **为什么：** 避免代码里到处出现 `os.path.join("..", "..", "tests")`，IDE 还能自动补全。
- **状态：** ✅ 见 [lindsey_learn_open_source_101/paths.py](lindsey_learn_open_source_101/paths.py)

---

## 2. 包元数据 / pyproject.toml

### 2.1 ✅ 用 `pyproject.toml` 而不是 `setup.py`
- **是什么：** 现代 Python 包的统一配置文件 (PEP 621)。
- **为什么：** `setup.py` 是历史遗留，社区已迁移到声明式的 toml。
- **状态：** ✅

### 2.2 ✅ 明确指定 `requires-python`
- **是什么：** `requires-python = ">=3.10,<4.0"`
- **为什么：** 防止用户在 Python 3.8 装你的库后跑出奇怪 bug（你只测了 3.10+）。
- **状态：** ✅

### 2.3 ✅ 使用 `classifiers` 标记 Python 版本/平台
- **是什么：** PyPI 用这些标签做筛选过滤；没设置就显示 "unclassified"。
- **为什么：** 让用户在 PyPI 上能筛选到你的库。
- **状态：** ✅ 11 个 classifier 见 [pyproject.toml:23-37](pyproject.toml)

### 2.4 ✅ Optional dependencies 分组（dev/test/doc/mise）
- **是什么：** `pip install lindsey-learn-open-source-101[test]` 只装测试时需要的。
- **为什么：** 普通用户装库不应该被迫下载 Sphinx + Furo（200MB+）。
- **状态：** ✅

### 2.5 ✅ 锁定依赖版本范围（>=X.Y.Z,<W.0.0）
- **是什么：** `pytest>=8.2.2,<9.0.0` 而不是 `pytest`。
- **为什么：** 主版本号变化通常 break API。锁住 major 让你睡得着觉。
- **状态：** ✅

### 2.6 ✅ `project.urls` 提供完整链接
- **是什么：** Homepage / Documentation / Repository / Issues / Changelog / Download。
- **为什么：** PyPI 项目页右侧栏会展示这些链接，提升项目可发现性。
- **状态：** ✅ 见 [pyproject.toml:84-90](pyproject.toml)

### 2.7 ✅ License 声明 + license-files 包含
- **是什么：** `license = "MIT"` + `license-files = ["LICENSE.txt", "AUTHORS.rst"]`
- **为什么：** 没有明确 license 的代码法律上**不可被任何人使用**。打包时也要带上。
- **状态：** ✅

### 2.8 ⚠️ `version` 单点定义（pyproject.toml）vs 双点定义
- **是什么：** 有些项目在 `pkg/_version.py` 也写 version，导致两处不同步。
- **为什么：** Single source of truth。改一处全改。
- **状态：** ⚠️ 你目前只在 pyproject.toml 写了 version，包里没有 `__version__`。建议加 `lindsey_learn_open_source_101/__init__.py: from importlib.metadata import version; __version__ = version(__name__)`

---

## 3. 依赖管理

### 3.1 ✅ 用 `uv` 而不是 `pip` 管理虚拟环境
- **是什么：** uv 是 Rust 写的 pip 替代品，比 pip 快 10-100 倍。
- **为什么：** 大型项目 `uv sync` 30 秒，`pip install -r` 5 分钟。生命太短不能等 pip。
- **状态：** ✅

### 3.2 ✅ `uv.lock` 提交到 git
- **是什么：** 锁文件记录**精确到 hash 的依赖版本**。
- **为什么：** 保证你和 CI 装到一模一样的依赖；防止 supply chain 攻击。
- **状态：** ✅ 见 [uv.lock](uv.lock)

### 3.3 ⚠️ 生产依赖（`dependencies`）越少越好
- **是什么：** 你的 `add_two` 不需要任何库，所以 `dependencies = []`。
- **为什么：** 用户装你的库会顺带装上你声明的所有依赖。每多一个依赖 = 多一个安装失败/版本冲突的风险。
- **状态：** ✅ 完美的 0 依赖

### 3.4 ❌ 添加 Dependabot/Renovate 自动更新依赖
- **是什么：** GitHub 内置工具，自动给过期依赖开 PR。
- **为什么：** 安全漏洞通常在依赖里。手动盯版本累死人。
- **状态：** ❌ 未配置 `.github/dependabot.yml`

### 3.5 ✅ `requirements*.txt` 通过 `uv export` 自动生成
- **是什么：** 不手写 requirements.txt，从 pyproject.toml 导出。
- **为什么：** 单点定义，避免"pyproject 里写了一个版本，requirements 里写了另一个"。
- **状态：** ✅ 见 mise.toml 的 `export` 任务

---

## 4. 测试

### 4.1 ✅ 用 pytest 而非 unittest
- **是什么：** Python 测试的事实标准。
- **为什么：** 写测试不用继承 class，断言直接 `assert`，插件生态完整。
- **状态：** ✅

### 4.2 ✅ 测试函数名以 `test_` 开头
- **是什么：** pytest 自动发现 `test_*.py` 文件里的 `test_*` 函数。
- **为什么：** 约定优于配置，不需要写 test runner 配置。
- **状态：** ✅

### 4.3 ✅ 每个测试可以独立运行（`if __name__ == "__main__":`）
- **是什么：** test_api.py 末尾有 `run_cov_test(...)` 入口。
- **为什么：** 调试单个测试时，PyCharm/VSCode 可以直接 "Run File"，不用先 `cd` 再 `pytest tests/test_xxx.py`。
- **状态：** ✅

### 4.4 ⚠️ 测试覆盖正常路径 + 边界 + 异常
- **是什么：** `add_two(1,2)`、`add_two(0,0)`、`add_two(-1,1)`、`add_two(100,200)`
- **为什么：** 覆盖率 100% 不等于"无 bug"。要测边界值（0, 负数, 极大值, None, type 错误）。
- **状态：** ⚠️ 你测了 4 个 case，但没测 type error 等。学习级别够了，生产代码要更全。

### 4.5 ✅ 覆盖率脚本独立 (`tests/all.py`)
- **是什么：** 单独的入口跑全包覆盖率。
- **为什么：** 你想知道**整个包**的覆盖率，不是单个文件的。
- **状态：** ✅

### 4.6 ❌ 加 doctest 让示例和测试同步
- **是什么：** 在 docstring 里写 `>>> add_two(1, 2)\n3`，pytest 会执行验证。
- **为什么：** 文档示例 = 测试，永远不会过时。
- **状态：** ❌ 你 docstring 写了示例但没启用 doctest。在 pyproject.toml 加 `[tool.pytest.ini_options] addopts = "--doctest-modules"` 即可启用。

### 4.7 ❌ 用 `pytest-xdist` 并行测试
- **是什么：** `pytest -n auto` 用所有 CPU 核并行跑。
- **为什么：** 测试多了之后串行 5 分钟、并行 30 秒。
- **状态：** ❌ 你只有 1 个测试，暂时不需要

---

## 5. 代码覆盖率

### 5.1 ✅ 用 `coverage.py` (通过 pytest-cov 插件)
- **是什么：** 跟踪哪些代码行被测试执行过。
- **为什么：** 没测过的代码 = 用户在生产环境帮你 debug 的代码。
- **状态：** ✅

### 5.2 ✅ `.coveragerc` 排除非业务代码
- **是什么：** `omit = vendor/* tests/* paths.py`
- **为什么：** vendor 是别人的代码、paths.py 是常量，把它们算进覆盖率会拉低数字、掩盖真实问题。
- **状态：** ✅ 见 [.coveragerc:4-10](.coveragerc)

### 5.3 ✅ 同时生成 term + HTML 报告
- **是什么：** `--cov-report term-missing --cov-report html:htmlcov`
- **为什么：** 终端看百分比，浏览器打开 htmlcov 看哪一行没被测。
- **状态：** ✅

### 5.4 📌❌ Codecov 上传 + Badge
- **是什么：** CI 把 coverage.xml 上传到 codecov.io，PR 上自动评论覆盖率变化。
- **为什么：** 防止某次提交悄悄降低覆盖率。
- **状态：** ❌ **mentor 已点名**。需要：(1) codecov.io 注册 (2) 加 CODECOV_TOKEN secret (3) 恢复 CI 上传步骤 (4) README 加 badge

---

## 6. 文档系统

### 6.1 ✅ 使用 Sphinx 而非纯 Markdown
- **是什么：** Python 文档事实标准，支持自动 API 抽取、交叉引用、PDF 输出。
- **为什么：** Markdown 写不了 `:py:func:`my_module.my_func``\` 这种自动链接。
- **状态：** ✅

### 6.2 ✅ 用 reStructuredText (.rst) 而非 Markdown
- **是什么：** rst 比 markdown 表达力强，是 Python 社区主流。
- **为什么：** Sphinx 原生支持 rst；markdown 需要插件。
- **状态：** ✅

### 6.3 ✅ Furo 主题（现代、暗色模式）
- **是什么：** 最流行的 Sphinx 主题。
- **为什么：** 默认 alabaster 主题土，readthedocs 主题陈旧。Furo 现代且响应式。
- **状态：** ✅

### 6.4 ✅ 用 docfly 自动生成 API 文档
- **是什么：** 扫描包，自动生成每个模块的 .rst 文件。
- **为什么：** 手写 200 个模块的 toctree 太累，自动化才是工程师的浪漫。
- **状态：** ✅ 见 [docs/source/conf.py:91-101](docs/source/conf.py)

### 6.5 ✅ README 用 `include` 而非复制粘贴
- **是什么：** docs/source/index.rst 用 `.. include:: ../../README.rst` 引入。
- **为什么：** README 改一处，文档主页同步更新。Single source of truth。
- **状态：** ✅

### 6.6 📌❌ 项目 LOGO（PNG）
- **是什么：** 256x256 或 512x512 PNG，放 `docs/source/_static/lindsey_learn_open_source_101-logo.png`，conf.py 加 `html_logo = "..."`
- **为什么：** 视觉品牌识别。专业项目都有。
- **状态：** ❌ **mentor 已点名**

### 6.7 📌❌ README 顶部 RTD badge
- **是什么：** RTD 提供的"docs passing"绿徽章。
- **为什么：** 一眼看出文档构建状态，点击直达文档站。
- **状态：** ❌ **mentor 已点名**。加这段到 README.rst：
  ```rst
  .. image:: https://readthedocs.org/projects/lindsey-learn-open-source-101-project/badge/?version=latest
      :target: https://lindsey-learn-open-source-101-project.readthedocs.io/en/latest/
  ```

---

## 7. CI/CD

### 7.1 ✅ GitHub Actions 而非 Travis CI / CircleCI
- **是什么：** GitHub 原生 CI，免费额度足够开源项目。
- **为什么：** 不用第三方授权，与 GitHub 集成最深。
- **状态：** ✅

### 7.2 ✅ Matrix testing 跨 Python 版本
- **是什么：** 同一份代码在 3.10/3.11/3.12/3.13 上各跑一遍。
- **为什么：** 防止你用了 3.12 新语法但 requires-python 写的 3.10。
- **状态：** ✅ 见 [.github/workflows/main.yml:18-19](.github/workflows/main.yml)

### 7.3 ✅ 缓存 `.venv` 加速 CI
- **是什么：** `actions/cache` 把 .venv 存起来，下次基于 uv.lock hash 命中复用。
- **为什么：** 装依赖通常占 CI 80% 时间。缓存命中能从 2 分钟降到 10 秒。
- **状态：** ✅

### 7.4 ✅ Push 和 PR 都触发 CI
- **是什么：** `on: push: branches: [main]` + `pull_request: branches: [main]`
- **为什么：** PR 在 merge 前必须先过 CI；push 主要是为了显示 main 当前状态。
- **状态：** ✅

### 7.5 ❌ Branch protection 规则
- **是什么：** GitHub Settings → Branches → Add rule for `main`，要求 PR + CI 必须通过才能 merge。
- **为什么：** 防止你（或队友）半夜手抖直接 push 到 main 把项目搞崩。
- **状态：** ❌ 你目前能直接 push main。

### 7.6 ❌ 多 OS 测试 (ubuntu + macos + windows)
- **是什么：** matrix 加上 `macos-latest`、`windows-latest`。
- **为什么：** 路径分隔符 / vs \\、行结束符 \\n vs \\r\\n 是常见跨平台 bug 源。
- **状态：** ❌ 你目前只测 ubuntu。pure Python 库其实问题不大，但 demo 项目是测三个 OS 的。

---

## 8. 版本控制 / Git

### 8.1 ✅ `.gitignore` 排除 build/cache/secrets
- **是什么：** `__pycache__/`、`.venv/`、`htmlcov/`、`dist/` 不进 git。
- **为什么：** 这些是生成物，进 git 会污染历史、暴露本地信息。
- **状态：** ✅

### 8.2 ⚠️ 提交信息描述 "why" 而非 "what"
- **是什么：** "Fix CI" ❌ vs "Fix CI: remove Codecov upload step that required missing CODECOV_TOKEN" ✅
- **为什么：** "what" 看 diff 就知道；"why" 是几个月后回看的关键。
- **状态：** ⚠️ 你的 commit 一些好（"Fix CI: remove Codecov upload step..."），一些短（"c"）。

### 8.3 ❌ Conventional Commits 规范
- **是什么：** `feat: add X`、`fix: handle Y`、`docs: update Z`、`chore: update deps`
- **为什么：** 工具能自动生成 changelog；团队 commit 风格统一。
- **状态：** ❌ 未采用

### 8.4 ✅ Feature branch + PR 工作流
- **是什么：** 小改动也开分支 → PR → review → merge。
- **为什么：** 留下讨论记录、CI 验证、可 revert。直接 push main 的项目都不专业。
- **状态：** ✅ 你做了 add-readthedocs PR

### 8.5 ⚠️ release-history.rst 详尽记录每个版本
- **是什么：** 按版本号列出 Features / Bugfixes / Breaking changes。
- **为什么：** 用户 upgrade 时第一时间想看变了什么。
- **状态：** ⚠️ 你只有 0.1.1 一行，将来发新版本要继续维护。

### 8.6 ❌ 用 git tag 标记 release
- **是什么：** `git tag -a v0.1.1 -m "..."` + `git push --tags`
- **为什么：** PyPI 版本和 git tag 应该 1:1 对应；GitHub Releases 基于 tag。
- **状态：** ❌ 还没打 tag

---

## 9. 包发布 / PyPI

### 9.1 ✅ 包名遵循 PEP 8（小写 + 下划线 / 横线）
- **是什么：** `lindsey_learn_open_source_101`（pkg）<-> `lindsey-learn-open-source-101`（PyPI 显示名）
- **为什么：** PyPI 把下划线和横线视作同义；社区惯例。
- **状态：** ✅

### 9.2 ✅ 同时构建 wheel + source distribution
- **是什么：** `dist/*.whl` + `dist/*.tar.gz`
- **为什么：** wheel 装得快；sdist 是兜底（用户系统不支持 wheel 时）。
- **状态：** ✅ `uv build` 默认两个都生成

### 9.3 ❌ 先发 TestPyPI 再发正式 PyPI
- **是什么：** test.pypi.org 是 PyPI 的沙箱版本。
- **为什么：** 万一 metadata 有错，TestPyPI 删除项目容易；正式 PyPI 删除后**包名永久占用**。
- **状态：** ❌ 建议第一次发布前先走 TestPyPI

### 9.4 ❌ Trusted Publishing (OIDC) 而非 API Token
- **是什么：** GitHub Actions 通过 OIDC 直接 auth 到 PyPI，不需要 token。
- **为什么：** Token 会泄露/过期。OIDC 是 2024+ PyPI 推荐方式。
- **状态：** ❌ 进阶玩法，先用 token 跑通再升级

### 9.5 ✅ Semantic Versioning (MAJOR.MINOR.PATCH)
- **是什么：** 0.1.1 → bug fix；0.2.0 → new feature；1.0.0 → 第一个稳定版本；2.0.0 → breaking change
- **为什么：** 用户根据版本号就能预判升级风险（patch 安全升、major 谨慎升）。
- **状态：** ✅ 你用了 0.1.1，符合规范

---

## 10. 外部服务集成

### 10.1 ✅ ReadTheDocs (RTD) 托管文档
- **是什么：** 免费给开源项目托管 Sphinx 文档的网站。
- **为什么：** 自己买域名+部署太重；RTD 自动 git pull → 重新构建。
- **状态：** ✅ 已配置

### 10.2 📌❌ Codecov 跟踪覆盖率
- **是什么：** 见 5.4
- **状态：** ❌ **mentor 已点名**

### 10.3 ❌ PyPI（接下来要做）
- **是什么：** Python 官方包索引。
- **状态：** ❌ 你的下一步

### 10.4 ❌ GitHub 仓库 metadata 完善
- **是什么：** Repo 顶部的 description、website、topics 标签。
- **为什么：** GitHub 搜索关键词靠 topics；description 让人快速理解项目。
- **状态：** ❌ Repo description 为空

---

## 11. 代码质量

### 11.1 ⚠️ 给所有公开函数加 type hints
- **是什么：** `def add_two(a: int, b: int) -> int:`
- **为什么：** IDE 补全 + mypy 静态检查 + 自动生成文档。
- **状态：** ⚠️ `add_two` 有 hints，但 `pytest_cov_helper.py` 等内部代码没有。

### 11.2 ❌ 用 ruff 做代码格式化 + lint
- **是什么：** 一个工具替代 black + flake8 + isort + pylint，速度 10x 以上。
- **为什么：** 代码风格统一，PR review 不再讨论缩进。
- **状态：** ❌ 未配置。在 pyproject.toml 加 `[tool.ruff]` + `pre-commit hook`

### 11.3 ❌ 用 mypy 做静态类型检查
- **是什么：** 运行前检查 type hint 是否一致。
- **为什么：** 让 type hint 有约束力，否则 hint 只是注释。
- **状态：** ❌

### 11.4 ✅ 文档字符串（docstring）规范
- **是什么：** Sphinx 风格 `:param x:` `:return:` 或 Google/NumPy 风格。
- **为什么：** docfly 抽出来变成 API 文档。
- **状态：** ✅ `add_two` 用了 Sphinx 风格

### 11.5 ❌ 用 `pre-commit` 框架在本地拦截问题
- **是什么：** Git commit 前自动跑 ruff/mypy/trailing-whitespace 等检查。
- **为什么：** 错误在本地就发现，不要等 CI 红了才知道。
- **状态：** ❌ 未配置 `.pre-commit-config.yaml`

---

## 12. 开源协作规范

### 12.1 ✅ AUTHORS 单独列出
- **是什么：** AUTHORS.rst 写明作者信息。
- **为什么：** 法律 + 致谢 + 联系方式。
- **状态：** ✅

### 12.2 ❌ CONTRIBUTING.md
- **是什么：** 告诉别人怎么贡献：怎么搭环境、怎么提 PR、commit 规范。
- **为什么：** 降低新贡献者门槛；很多潜在贡献者因为不知道怎么开始就放弃了。
- **状态：** ❌

### 12.3 ❌ CODE_OF_CONDUCT.md
- **是什么：** 行为准则（Contributor Covenant 是事实标准）。
- **为什么：** 大型项目必备，让贡献者环境健康。
- **状态：** ❌

### 12.4 ❌ Issue / PR 模板
- **是什么：** `.github/ISSUE_TEMPLATE/*.yml`、`.github/PULL_REQUEST_TEMPLATE.md`
- **为什么：** 新人开 issue 总是缺关键信息（Python 版本、复现步骤），模板强制填。
- **状态：** ❌

### 12.5 ❌ SECURITY.md
- **是什么：** 描述如何报告安全漏洞（不要在 public issue）。
- **为什么：** 防止 0day 公开。
- **状态：** ❌

---

## 13. 进阶实践

### 13.1 ❌ Performance benchmark + tracking
- **是什么：** `tests/benchmarks/`，用 `pytest-benchmark` 跟踪性能。
- **为什么：** 防止某次重构让函数变慢 10 倍。
- **状态：** ❌

### 13.2 ❌ 多语言 README (英文 + 中文)
- **是什么：** README.rst + README_zh.rst
- **为什么：** 中文用户多，文档双语扩大用户群。
- **状态：** ❌

### 13.3 ❌ 性能 / API doc 用 examples 文件夹
- **是什么：** `examples/` 放可运行的示例脚本。
- **为什么：** 用户 copy-paste 能跑的例子比文档更有说服力。
- **状态：** ❌

### 13.4 ❌ GitHub Actions 自动发 release notes
- **是什么：** 用 `release-drafter` 或 `gh release create` 自动从 PR 标题生成 release notes。
- **为什么：** Release notes 永远懒得写，自动化救命。
- **状态：** ❌

### 13.5 ❌ Stargazers / Downloads badge 等社交证明
- **是什么：** README 加 `![Downloads](https://pepy.tech/badge/lindsey-learn-open-source-101)` 等。
- **为什么：** 社交证明 → 增加信任度 → 更多人用。
- **状态：** ❌

---

## 总结：当前状态打分

| 类别 | 已完成 | 总数 | 完成度 |
|------|--------|------|--------|
| 1. 项目结构 | 5 | 5 | 100% ✅ |
| 2. 包元数据 | 7 | 8 | 88% |
| 3. 依赖管理 | 4 | 5 | 80% |
| 4. 测试 | 4 | 7 | 57% |
| 5. 代码覆盖率 | 3 | 4 | 75% |
| 6. 文档系统 | 5 | 7 | 71% |
| 7. CI/CD | 4 | 6 | 67% |
| 8. 版本控制 | 2 | 6 | 33% |
| 9. 包发布 | 3 | 5 | 60% |
| 10. 外部服务 | 1 | 4 | 25% |
| 11. 代码质量 | 1 | 5 | 20% |
| 12. 开源协作 | 1 | 5 | 20% |
| 13. 进阶实践 | 0 | 5 | 0% |
| **总计** | **40** | **72** | **56%** |

---

## 我建议的下一步学习顺序

按"投入产出比"排序：

1. **本周补 mentor 点名的三个**（LOGO + RTD badge + Codecov）→ 最关键
2. **补 8.6 git tag + 9.x PyPI 发布** → 完成"开源闭环"
3. **补 12.2 CONTRIBUTING.md + 12.4 issue template** → 一上午搞定
4. **补 11.2 ruff + 11.5 pre-commit** → 提升代码质量基线
5. **补 7.5 branch protection + 8.3 conventional commits** → 团队协作准备

学完一轮再回头看 13. 进阶实践。

---

## 附：扩展阅读

- [Python Packaging User Guide](https://packaging.python.org/)
- [PEP 621: Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Choose a License](https://choosealicense.com/)
- [Open Source Guides (GitHub)](https://opensource.guide/)
