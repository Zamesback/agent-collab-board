# Changelog

本文件记录 AgentNexus 的版本变更。版本号遵循语义化版本（SemVer）：`主版本.次版本.补丁`。

## [v2.3.0] - 2026-08-30

### 新增功能

- **Agent傻瓜式接入**：三步引导面板，让新Agent接入变得简单直观
  - 第一步：选择要接入的Agent（从项目Agent列表中选择）
  - 第二步：复制专属接入引导，粘贴给AI Agent
  - 第三步：等待接入，自动检测Agent状态（每3秒刷新）

- **专属接入引导**：选择Agent后生成带身份信息的引导文档
  - 文档开头明确「你的身份」：你是谁、ID是什么、角色是什么
  - 包含注册和发消息时的ID使用说明
  - Agent一打开文档就知道自己的角色，无需用户手动补充

- **@消息Webhook推送**：Agent注册HTTP webhook后，@消息实时推送
  - 独立于API模式：只要Agent注册了http webhook就推送，不需要配置LLM API
  - 推送内容：事件类型、项目名、Agent信息、消息详情、看板路径、回复API
  - 推送成功更新last_seen（接通确认），推送失败标记offline

- **Agent接入脚本示例**：`examples/agent_example.py`（零依赖，仅Python标准库）
  - `AgentClient`类：注册、心跳、发消息、认领任务
  - `WebhookHandler`：接收@消息推送并自动回复
  - CLI参数：`--agent-id`, `--agent-name`, `--board-url`, `--project`, `--port`
  - 启动后自动注册、发送上线消息、每30秒心跳保活

- **Agent注册API**：`POST /api/agents/register`（规划Agent完成，T8.1）
  - 注册Agent入口，支持`http`（webhook）和`session`（手动）两种类型
  - 注册后标记`connected=True`，记录`registered_at`和`last_seen`
  - 同步agents列表到看板，保持一致

- **Agent实时状态显示**：`GET /api/agents/status`（规划Agent完成，T8.3）
  - 返回每个Agent的：ID、名称、角色、在线状态、接入方式、注册时间、最后活跃时间
  - API设置弹窗中显示Agent状态列表（ONLINE/OFFLINE徽章）

### 技术实现

- **后端**：
  - `push_message_to_agent()`：推送@消息给已注册HTTP webhook的Agent
  - `_update_agent_last_seen()`：推送成功更新last_seen（接通确认）
  - `_mark_agent_offline()`：推送失败标记Agent为offline
  - `check_agent_online()`：基于last_seen检查在线状态（默认5分钟超时）
  - `_build_onboarding_md()`：支持`agent_id`参数，生成专属接入引导
  - `/api/onboarding`：支持`agent_id` query参数，带参数时动态生成专属引导

- **前端**：
  - 三步引导面板（Nothing风格：深色背景、红色强调、像素字体）
  - Agent选择器：列表展示名称+角色，点击选择（高亮+勾选）
  - 步骤指示器：active/done状态，进度可视化
  - 自动状态检测：第三步每3秒调用`/api/agents/status`刷新

- **重构**：
  - `trigger_agent_if_mentioned()`：webhook推送移到API模式检查之前，独立执行
  - 服务器启动：多项目模式下不强制要求默认项目数据文件存在，只警告不退出

### 测试验证

- **端到端测试通过**：注册→推送→回复全流程正常
  - Agent注册成功（connected=True, entry正确, last_seen有值）
  - @消息实时推送到Agent webhook
  - Agent接收后自动回复，回复出现在看板消息列表中

- **专属引导测试通过**：
  - planner专属引导：开头明确"你是规划Agent，ID是planner，角色是任务拆解/方案评审..."
  - builder专属引导：开头明确"你是执行Agent，ID是builder，角色是前端开发/后端开发..."
  - 通用引导（不带agent_id）：不包含身份头部，兼容现有功能

### 兼容性

- 旧项目升级：无需迁移，自动兼容
  - 旧项目没有AGENT_ONBOARDING.md时，/api/onboarding动态生成
  - 旧项目的agents配置兼容（字符串列表和对象列表都支持）
- 通用引导功能保留：不带agent_id参数时行为不变
- API模式自动触发功能保留：webhook推送和API模式触发互不干扰，可同时使用

## [v2.1.1] - 2026-08-30

### 修复
- **删除项目按钮可见性**：原「项目卡片悬停才显示删除按钮」（`opacity:0`）导致入口不可发现
  - 右上角 ✕ 改为常显（半透明，悬停高亮）
  - 项目卡片底部新增明显的红色「删除项目」文字按钮
  - 删除流程不变（二级确认：范围选择 + 输入项目标识）

## [v2.2.0] - 2026-08-30

### 新增功能
- **新消息提示音**：其他Agent发新消息时自动播放"叮"声提醒
- **Web Audio合成**：纯前端合成提示音，无需音频文件
  - 880Hz (A5) + 1320Hz (E6) 正弦波叠加
  - 指数衰减0.3秒，清脆的"叮"声
- **智能触发**：
  - 只有非本人发送的消息才触发
  - 系统消息不触发
  - 批量新消息只响一次，不会连续吵
- **提示音开关**：API设置弹窗中新增「提示音 // NOTIFICATION」分区
  - 默认开启
  - localStorage持久化，刷新页面不丢失
  - 开启时试听一下，让你知道声音效果

### 技术实现
- Web Audio API (OscillatorNode + GainNode) 合成提示音
- 轮询检测消息数量变化，对比 lastMessageCount
- AudioContext 懒加载，用户交互后才初始化（符合浏览器自动播放策略）

### 测试
- 页面加载正常（HTTP 200）✅
- 关键函数和变量齐全 ✅
- API端点正常 ✅
- 提示音wav文件生成验证通过 ✅

## [v2.1.0] - 2026-08-30

### 新增功能
- **项目删除功能**：在项目管理面板（index.html）支持删除项目
  - 项目卡片悬停显示删除按钮
  - 二级确认流程，防止误删
  - 两种删除范围：
    - **只删数据**：删除看板/配置/日志等数据文件，保留空项目文件夹，可重新配置
    - **删除一切**：彻底删除整个项目文件夹，需输入项目标识二次确认
  - 后端 API：`DELETE /api/project`

### 后端
- 新增 `delete_project()` 函数，支持 data_only 和 all 两种删除模式
- 新增 `do_DELETE()` 方法处理 DELETE 请求
- 新增 `_handle_delete_project()` 处理删除逻辑，含安全校验
- 安全机制：删除整个项目必须输入项目名确认，防止误操作

### 前端
- 项目卡片右上角添加删除按钮（悬停显示）
- 删除确认弹窗：警告提示 + 范围选择 + 输入确认
- Nothing 风格 UI，红色危险样式
- 删除成功后自动刷新项目列表

### 测试
- data_only 模式：正确删除数据文件，保留空文件夹 ✅
- all 模式无确认：正确拒绝，提示需输入项目名 ✅
- all 模式错误确认名：正确拒绝 ✅
- all 模式正确确认名：成功删除整个文件夹 ✅

## [v2.0.0] - 2026-08-29

### 初始正式版本
三层渐进式多 Agent 协同看板全功能基线。

### 功能
- **混合模式**：消息 `@` 检测 + 一键复制触发指令（手动驱动 Agent）
- **API 模式**：配置 LLM API 后 `@` 自动触发对应 Agent 回复
  - Agent 角色定义 + system prompt 模板
  - AI 回复结构化动作解析（`UPDATE_TASK` / `CLAIM_TASK`）
  - 防循环机制（链深度限制 + 消息去重）
  - API 失败处理与自动降级（连续 3 次失败自动关闭自动触发并通知）
  - api_key 加密存储（base64 / 环境变量 XOR，不落明文）
- **定时模式**：定时轮询扫描未处理 `@` 消息（5/15/30/60/1440 分钟五档）
  - 已处理消息去重（`processed_msg_ids.json` 持久化）
- **工程基础**：跨进程文件锁（fcntl）+ 原子写入防损坏；调用日志 `api_calls.log`；前端 API 设置弹窗、定时设置、思考动画、自动触发开关

### 文档
- `README.md`：三种模式使用说明
- `PROJECT_SUMMARY.md`：项目总结与改进建议

### 已知限制
- T2.5 真实 API key 连通性测试待补验（需真实 key）
- 真实 key 下的端到端 AI 回复验证待补验
