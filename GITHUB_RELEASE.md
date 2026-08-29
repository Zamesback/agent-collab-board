# GitHub 发布指南

本文档指导如何将多Agent协同看板发布到GitHub。

---

## 一、上传到GitHub的步骤

### 方式一：通过命令行（推荐）

```bash
# 1. 进入项目目录
cd /path/to/agent-collab-dev

# 2. 初始化Git仓库
git init

# 3. 添加所有文件（.gitignore会自动忽略不需要的文件）
git add .

# 4. 确认要提交的文件（应该没有collab_board.json等数据文件）
git status

# 5. 首次提交
git commit -m "Initial commit: 多Agent协同看板 v2.0"

# 6. 在GitHub上创建新仓库（不要勾选README、.gitignore、LICENSE，因为我们已经有了）
#    仓库名建议：agent-collab-board 或 collab-board

# 7. 关联远程仓库
git remote add origin https://github.com/你的用户名/仓库名.git

# 8. 推送到GitHub
git branch -M main
git push -u origin main
```

### 方式二：通过GitHub Desktop

1. 打开GitHub Desktop
2. File → Add Local Repository → 选择项目文件夹
3. 点击 "Publish repository"
4. 填写仓库名和描述
5. 取消勾选 "Keep this code private"（如果要开源）
6. 点击 "Publish Repository"

---

## 二、仓库设置建议

### 1. 仓库描述
```
一个轻量级的多Agent协同工作平台，让多个AI Agent和人类在同一个看板上协作完成项目。支持混合模式/API模式/定时模式三种协同方式，零第三方依赖。
```

### 2. 仓库Topics（标签）
建议添加以下标签：
- `agent`
- `ai-agent`
- `collaboration`
- `project-management`
- `kanban`
- `multi-agent`
- `python`
- `zero-dependency`
- `local-first`

### 3. 仓库设置
- **Default branch**: main
- **Features**: 勾选 Issues、Wiki、Discussions（可选）
- **Pull Requests**: 勾选 "Allow squash merging"
- **Security**: 开启 Dependabot alerts（可选）

---

## 三、GitHub Release 发布说明

### v2.0.0 - 多项目管理版本

#### 🎉 新特性

- **多项目管理**：根目录管理多个独立项目，每个项目有独立的数据和配置
- **项目管理器首页**：一目了然所有项目，支持创建新项目向导
- **创建项目向导**：项目名/描述/接入Agent/工作区/交接文件，一站式配置
- **Nothing风格UI**：深色主题 + 红色强调色 + 像素字体 + 网格背景
- **项目数据隔离**：每个项目独立文件夹，数据互不干扰

#### 🔧 三种协同模式

| 模式 | 说明 |
|---|---|
| 混合模式（默认） | 消息@检测 + 一键复制触发指令，手动驱动Agent |
| API模式 | 配置LLM API后，@消息自动触发Agent回复并执行动作 |
| 定时模式 | 定时轮询未处理的@消息，自动触发Agent |

#### ⚡ 技术特点

- **零第三方依赖**：仅使用Python标准库，不需要pip install任何东西
- **文件即数据库**：JSON文件存储，人类可读，Agent可直接读写
- **渐进式增强**：从纯手动开始，按需启用API和定时模式
- **跨平台**：macOS / Linux（Windows需适配文件锁）

#### 📦 文件清单

```
agent-collab-board/
├── server.py                  # 后端服务器
├── index.html                 # 项目管理器首页
├── collab_board_nothing.html  # 看板主界面（Nothing风格）
├── collab_board.html          # 经典版看板
├── launch.html                # 启动定义页
├── start.command              # macOS启动脚本
├── stop.command               # macOS停止脚本
├── examples/                  # 示例项目
│   └── sample-project/        # 示例项目数据
├── docs/
│   └── screenshots/           # 截图目录
├── t5_regression_test.py      # 回归测试
├── .gitignore
├── LICENSE                    # MIT协议
└── README.md
```

#### 🚀 快速开始

```bash
python3 server.py
# 打开 http://localhost:8766
```

#### 📝 完整更新日志

- v2.0.0: 多项目管理 + Nothing风格UI + 项目管理器首页
- v1.0.0: 初始版本，三层渐进式协同模式

---

## 四、发布前检查清单

- [x] .gitignore 已配置，数据文件不会上传
- [x] README.md 已写好，包含项目介绍/功能/快速开始/API文档
- [x] LICENSE 已添加（MIT协议）
- [x] 示例项目已准备（examples/sample-project/）
- [x] 截图目录已创建（docs/screenshots/）
- [ ] 实际运行截图已添加（可选但推荐）
- [ ] 项目描述和Topics已设置
- [ ] 仓库已设为Public（如果要开源）
- [ ] Release已发布

---

## 五、后续维护建议

1. **截图补充**：运行项目，截取实际界面图放到 docs/screenshots/
2. **版本管理**：使用语义化版本号（MAJOR.MINOR.PATCH）
3. **更新日志**：每次发布更新 CHANGELOG.md
4. **Issue模板**：添加Bug报告和功能请求的Issue模板
5. **贡献指南**：添加 CONTRIBUTING.md
6. **Code of Conduct**：添加行为准则文档

---

## 六、常见问题

### Q: 我的项目数据会上传到GitHub吗？
A: 不会。.gitignore已经配置了忽略 collab_board.json、project_config.json 等数据文件。只有代码和模板会上传。

### Q: API Key会泄露吗？
A: 不会。API Key保存在 project_config.json 中，这个文件已经被.gitignore忽略，不会上传到GitHub。

### Q: 可以私有仓库吗？
A: 可以。创建仓库时勾选 "Private" 即可。但如果希望社区贡献和使用，建议设为Public。

### Q: 怎么更新到最新版本？
A: 
```bash
git pull origin main
```
