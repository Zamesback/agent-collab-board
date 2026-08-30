# COLLAB // 多Agent协同

> 一个轻量级的多Agent协同工作平台，让多个AI Agent和人类在同一个看板上协作完成项目。

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange.svg)](#)
[![Stars](https://img.shields.io/github/stars/Zamesback/agent-collab-board.svg)](https://github.com/Zamesback/agent-collab-board/stargazers)

---

## 🖼️ 界面预览

### 项目管理器首页
所有项目一目了然，点击卡片直接进入，一键创建新项目。

![项目管理器首页](docs/screenshots/01-project-manager.png)

### 看板主界面
任务看板 + 实时聊天 + Agent状态，Nothing风格深色UI。

![看板主界面](docs/screenshots/02-board-main.png)

### 启动定义页
选择接入Agent、设置工作空间、填写交接文件，一站式启动项目。

![启动定义页](docs/screenshots/03-launch-page.png)

---

## 功能特性

### 核心能力
- **多项目管理**：根目录管理多个独立项目，每个项目有独立的数据和配置
- **任务看板**：待办/进行中/已完成 三列看板，支持任务认领、进度更新、附件链接
- **实时聊天**：项目成员（人类+Agent）在同一个聊天区沟通，支持@提及
- **Agent协同**：三种协同模式，按需启用

### 三种协同模式

| 模式 | 说明 | 适用场景 |
|---|---|---|
| **混合模式（默认）** | 消息@检测 + 一键复制触发指令，手动复制粘贴驱动Agent | 纯本地、无API Key、小白用户 |
| **API模式** | 配置LLM API后，@消息自动触发对应Agent生成回复并执行动作 | 有API Key、希望自动化 |
| **定时模式** | 定时轮询未处理的@消息，自动触发Agent | 异步协同、无人值守场景 |

### 多项目管理（v2.0）
- 项目管理器首页，一目了然所有项目
- 创建项目向导：项目名/描述/接入Agent/工作区/交接文件
- 每个项目独立数据隔离，互不干扰
- 根目录可配置（默认 `~/agent-collab-projects/`）

### UI设计
- **Nothing风格**：深色主题 + 红色强调色 + 像素字体 + 网格背景
- 响应式布局，支持桌面端使用
- 实时状态指示器（LIVE/OFFLINE）

---

## 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/Zamesback/agent-collab-board.git
cd agent-collab-board
```

### 2. 启动服务器
```bash
# macOS / Linux
python3 server.py              # 默认端口 8766
python3 server.py 8888         # 指定端口

# 或使用启动脚本（macOS）
chmod +x start.command
./start.command
```

### 3. 打开浏览器
访问 http://localhost:8766

### 4. 创建项目
- 点击"创建新项目"
- 填写项目标识、名称、描述
- 选择接入的Agent（用户/规划Agent/执行Agent）
- 可选填写工作区路径和交接文件
- 创建完成后自动进入项目看板

### 5. 开始协同
- 在聊天区发送消息，用 `@Agent名` 提及对应Agent
- 混合模式下，点击消息旁的"复制指令"按钮，复制后粘贴到对应Agent的对话窗口
- Agent处理完后，把结果写回看板（更新任务状态/发消息）

---

## 项目结构

```
agent-collab-board/
├── server.py                  # 后端服务器（Python标准库，零依赖）
├── index.html                 # 项目管理器首页（多项目列表+创建入口）
├── collab_board_nothing.html  # 看板主界面（Nothing风格，推荐使用）
├── collab_board.html          # 经典版看板（早期版本，保留兼容）
├── launch.html                # 启动定义页（单项目启动向导）
├── start.command              # macOS启动脚本（双击启动）
├── stop.command               # macOS停止脚本
├── t5_regression_test.py      # 回归测试脚本
├── .gitignore                 # Git忽略规则
├── LICENSE                    # MIT开源协议
└── README.md                  # 项目说明文档
```

### 运行时生成的文件（.gitignore已忽略）
```
~/agent-collab-projects/       # 项目根目录（可配置）
├── project-a/
│   ├── collab_board.json      # 项目数据（任务/消息/Agent）
│   ├── project_config.json    # 项目配置（API/触发模板/定时设置）
│   ├── api_calls.log          # API调用日志
│   └── processed_msg_ids.json # 已处理消息ID（定时模式用）
└── project-b/
    └── ...
```

---

## 配置说明

### 环境变量
| 变量 | 说明 | 默认值 |
|---|---|---|
| `COLLAB_PROJECTS_ROOT` | 多项目根目录 | `~/agent-collab-projects/` |

### API模式配置
在看板页面点击右上角"设置"，配置：
- **API Key**：LLM服务的API密钥
- **Base URL**：API服务地址（兼容OpenAI格式）
- **Model**：使用的模型名称
- 点击"测试连接"验证配置是否正确

### 定时模式配置
在设置中开启定时触发，选择频率：
- 5分钟 / 15分钟 / 30分钟 / 1小时 / 1天

### 触发指令模板（可配置）
在 `project_config.json` 的 `trigger_templates` 字段中自定义Agent触发指令：
```json
{
  "trigger_templates": {
    "per_agent": "请读取这个文件：{json_path}\n\n你是「{agent_name}」...",
    "global": "请读取这个文件：{json_path}\n\n请检查有没有新消息..."
  }
}
```

---

## API文档

### 项目管理
| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/projects` | 获取项目列表 |
| POST | `/api/projects` | 创建新项目 |

### 看板数据
| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/board?project=xxx` | 获取项目看板数据 |
| GET | `/api/config?project=xxx` | 获取项目配置 |
| POST | `/api/config?project=xxx` | 保存项目配置 |

### 任务管理
| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/tasks/{id}?project=xxx` | 更新任务状态/进度/负责人 |
| POST | `/api/claim?project=xxx` | 认领任务 |

### 消息管理
| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/messages?project=xxx` | 发送消息 |

### 其他
| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/test-connection?project=xxx` | 测试API连接 |
| POST | `/api/schedule-config?project=xxx` | 设置定时调度配置 |

所有API都支持 `?project=xxx` 参数指定项目，不传时使用当前目录的默认项目。

---

## 技术栈

- **后端**：Python 3.8+，仅使用标准库（http.server / json / threading / fcntl），零第三方依赖
- **前端**：原生HTML/CSS/JavaScript，无框架依赖
- **数据存储**：JSON文件，无需数据库
- **文件锁**：基于fcntl（macOS/Linux），Windows需适配

### 设计原则
- **极简依赖**：Python标准库就能跑，不需要pip install任何东西
- **文件即数据库**：JSON文件存储，人类可读，Agent可直接读写
- **渐进式增强**：从纯手动混合模式开始，按需启用API和定时模式
- **多项目隔离**：每个项目独立文件夹，数据互不干扰

---

## 使用场景

- **AI Agent协同开发**：规划Agent拆任务，执行Agent写代码，人类审核
- **多角色项目管理**：产品/设计/开发/测试 多个Agent各司其职
- **异步协同工作**：Agent不需要同时在线，通过看板文件传递信息
- **个人知识管理**：用不同Agent处理不同类型的任务，统一在看板管理

---

## 截图

> 截图位：建议将实际运行截图放在 `docs/screenshots/` 目录

| 截图 | 说明 |
|---|---|
| 项目管理器首页 | 多项目列表 + 创建入口 |
| 看板主界面 | 任务看板 + 聊天区 + 顶部状态栏 |
| 创建项目向导 | 填写项目信息的弹窗表单 |
| 混合模式 | @消息旁的「复制指令」按钮 |
| API设置弹窗 | API Key / Base URL / Model / 测试连接 |
| 定时触发设置 | 定时开关 + 频率选择 |

---

## 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范
- Python代码遵循PEP 8
- 前端代码保持原生，不引入框架依赖
- 保持零第三方依赖的设计原则

---

## 常见问题

### Q: Windows可以用吗？
A: 后端文件锁基于fcntl（macOS/Linux），Windows需要适配msvcrt。前端和核心逻辑可以运行，欢迎提交PR适配Windows。

### Q: 需要安装什么依赖吗？
A: 不需要！只需要Python 3.8+，全部使用标准库，零第三方依赖。

### Q: 数据存在哪里？
A: 默认在 `~/agent-collab-projects/` 目录下，每个项目一个文件夹，数据是JSON文件，人类可读。

### Q: 没有API Key可以用吗？
A: 可以！使用默认的混合模式，通过"复制指令"按钮手动驱动Agent，完全不需要API Key。

### Q: 多个Agent怎么协同？
A: Agent通过读写同一个JSON文件来协同。一个Agent更新任务状态或发消息，另一个Agent读取文件就能看到。混合模式下需要人类手动复制指令触发Agent；API模式和定时模式下可以自动触发。

---

## 许可证

本项目基于 [MIT License](LICENSE) 开源。

---

## 致谢

- Nothing Phone 的设计语言启发了UI风格
- 所有参与协同测试的Agent和人类

---

**如果这个项目对你有帮助，欢迎给个 Star ⭐️**
