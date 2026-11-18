# 开发日志

## 2026-11-18 · W10 实验二、实验三：应用上云，密钥本地/云端通用

### 今天做了什么

- 新建 GitHub 公开仓库 `individual-project-multimodal-trip`，首版只放 README 与 .gitignore。
- 写 `app.py`（复利计算器：投资年限、年化收益率两个滑块 + 到期本息）与 `requirements.txt`；本地 `.venv` 跑通后 `pip freeze` 全量冻结为 35 行带版本号的清单。
- 推到 GitHub，并在 Streamlit Community Cloud 创建应用：<https://sirius6657-compound.streamlit.app> 。
- 改造 `app.py`：`load_dotenv` + `get_key()` 兼容写法（本地走 .env、云端走 `st.secrets`），侧栏增加「密钥体检」面板。

### 关键决定

- **密钥双通道**：本地用 .env、云端用 Secrets，代码只用 `get_key()` 一处兼容读取，不维护两个版本。
- **体检面板只报状态与来源通道**（已配置 / 缺失、本地 .env / 云端 Secrets），永不显示密钥本身的值。
- **密钥永不入库**：.env 始终留在 .gitignore 里，`git status` 里看不到它才继续提交。

### 学到的新东西

- 云端只能拿到仓库里的东西，所以 .env 不会跟上去——密钥必须走平台 Secrets 这条独立通道；这也解释了"本地能跑、云端 AI 失效"的根因。
- Python 3.13 的 `os.mkdir(mode=0o700)` 会生成仅属主可访问的 ACL，受限身份下 `tempfile.mkdtemp` 会直接 `PermissionError`，`ensurepip` 也跟着失败。
- git 的进度信息写在 stderr，和 `$ErrorActionPreference='Stop'` 一起用会被当成错误中断整条脚本。

### 卡点

- push 偶发 `fatal: ... Recv failure: Connection was reset`，改用 `git -c http.version=HTTP/1.1 push` 并重试后成功。
- pip 在受限环境里对 HTTPS 反复重试，表现为长时间无输出，需要完整网络权限，并加 `--retries` / `--timeout` 压缩重试。
- 云端 Secrets 暂未配置，云端体检显示「缺失」属预期；等接入 DeepSeek 之前补上并 Reboot 即可。

### 互助记录

无
