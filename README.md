# ☁️ Cloud-Security-Study

**个人学习与研究总仓库**：云安全研究、算法练习、大模型求职笔记、Python 学习，以及若干项目代码的集合。

> 仓库从云安全研究起步（2026-04-30），现已扩展为个人学习与研究的总收纳地。
> 本地路径：`E:\Cloud-Security-Study`（2026-09-17 从 C 盘迁移而来）

---

## 🖥️ 本机环境

| 项目 | 值 |
| :--- | :--- |
| Python | 3.13.12（Windows） |
| Linux 环境 | WSL2 + Docker（2026-04-30 配置完成，hello-world 跑通） |
| 版本管理 | 便携式 Git，SSH 推送到 GitHub |

---

## 📁 目录说明

### 1. [Graduation-Project](./Graduation-Project/)
*   **内容**：基于 XGBoost 的 DGA 域名检测系统（毕业设计）。
*   **说明**：`bishe/` 为完整代码与实验脚本；PPT / docx、`code/`、`models/` 按 `.gitignore` 规则不入库。

### 2. [Algorithm-Templates](./Algorithm-Templates/)
*   **内容**：算法与数据结构练习。
    *   `OJ-C++`：课程 OJ 的 C++ 解题代码（编号顺序存放）。
    *   `LeetCode-Daily`：每日一题，一题一文件夹（README + C + Python 双语言）。
    *   `Python_study`：**Python 语言学习工作区**（从零开始，11 个主题，每个主题含笔记与可运行示例）。

### 3. [STUDY_FOR_WORK](./STUDY_FOR_WORK/)
*   **内容**：求职向学习笔记。
    *   `LLM-and-Agent-Notes.md`：大模型与 Agent 开发笔记（基础概念、序列建模、序列标注、Agent 原理、求职要求拆解）。

### 4. [crypto-quant](./crypto-quant/)
*   **内容**：加密货币量化交易项目。
    *   `backend/`：FastAPI 后端（策略引擎、风控、执行器、回测）。
    *   `frontend/`：Web 控制台；`client/`：独立桌面客户端。
*   **安全约定**：交易所 / LLM 的 API Key 只保存在本地数据库或前端输入，**绝不写入仓库**。

### 5. [Assignments](./Assignments/)
*   **内容**：课程作业与实验记录（含 opencode 多 Agent 编排配置）。

### 6. [References](./References/)
*   **内容**：参考资料——《云计算数据安全》书籍、比特币挖矿演示脚本等。

### 7. [test](./test/)
*   **内容**：零散测试 / 草稿文件。

---

## 🧪 实验记录

* 2026-04-30：正式开始云安全研究，WSL2 环境配置完成
* 2026-04-30：成功安装 Docker 引擎并跑通 hello-world 容器
* 2026-09-17：仓库整体迁移至 E 盘（校验 195 文件一致后删除源目录）
* 2026-09-17：合并 Transformer / Agent 两份笔记为 `LLM-and-Agent-Notes.md`
* 2026-09-17：新建 Python 学习工作区 `Algorithm-Templates/Python_study/`

---

## 🔒 隐私与安全约定

`.gitignore` 已按「敏感内容一律不入库」原则配置：

*   **密钥 / 证书**：`.pem` `.key` `.pfx` `.p12`、`id_rsa*`、`id_ed25519*`、`.ssh/`、`credentials`、`secret`、`mnemonic`
*   **私密配置**：`.env` 及 `config.local.*`（`.env.example` 例外）
*   **运行时数据**：`*.db` `*.sqlite`（量化项目的本地数据库可能含 API Key）、`*.log`
*   **大文件 / 文档**：`*.pptx` `*.docx`、毕设的 `code/` 与 `models/` 目录
*   **其他**：`__pycache__`、`.venv/`、编辑器与系统垃圾文件
