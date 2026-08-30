# 版本管理与协作约定

本文档约定 AgentNexus 的版本管理方式，所有协作者（人类 + AI Agent）必须遵守。

## 版本号（SemVer）

- 格式：`主版本.次版本.补丁`（如 `v2.1.0`）
- 当前基线：**v2.0.0**
- 增量功能 / 新需求 → 次版本 +1（`2.1.0`、`2.2.0`…）
- 兼容性修复 → 补丁 +1
- 破坏性 / 大改版 → 主版本 +1（`3.0.0`）
- 每个版本在 `main` 上打对应 tag

## 分支策略

- **`main`**：稳定主线，永远可运行，只接受已验收的合并
- 每个新需求：从 `main` 拉出 `feature/<简述>` 分支（如 `feature/template-engine`）
- 完成 + 验收通过后：merge 回 `main`，删除 feature 分支
- 命名用小写连字符，简短达意

## 提交规范（Conventional Commits）

格式：`<type>(<scope>): <描述>`

| type | 用途 |
|---|---|
| `feat` | 新功能 |
| `fix` | 缺陷修复 |
| `docs` | 文档变更 |
| `refactor` | 重构（不改变行为） |
| `test` | 测试相关 |
| `chore` | 构建/工具/杂项 |

示例：`feat(api): 支持通义千问兼容接口`

## 版本发布流程

1. 需求确认 → 从 `main` 拉 `feature/xxx` 分支
2. 开发实现 → 对照任务验收标准验收
3. 更新 `CHANGELOG.md`（新版本条目）
4. merge 到 `main` → 打 tag `vX.Y.Z` → push（`main` + tag）

## 任务分工约定

- 每个需求拆解成任务后，除标注优先级外，**必须同步分配负责人（assignee）**，在看板可查
- 分工原则：规划 Agent 与执行 Agent 各自认领一部分，避免单点积压
- 未实现的任务**不得标记 done**；标记 done 的任务必须能在代码中核对到实现

## 安全约定

- `project_config.json`（含 api_key 加密存储）、`*.lock`、`*.tmp`、`api_calls.log` 已在 `.gitignore`，**禁止**提交
- remote 使用 **SSH**（`git@github.com:Zamesback/agent-nexus.git`），**禁止**在 URL 中内嵌 token
- 代码中禁止出现明文密钥

## 协作数据文件

- `collab_board.json`：多 Agent 协作看板数据（任务/消息/Agent），是协作的单一事实源
- **只做增量修改**（追加消息、更新任务字段），**绝不整体覆盖文件**
