<div align="center">

# 🤖 123bot

### Telegram 云盘自动转存机器人

[![GitHub stars](https://img.shields.io/github/stars/dydydd/123bot?style=social)](https://github.com/dydydd/123bot/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/dydydd/123bot?style=social)](https://github.com/dydydd/123bot/network/members)
[![GitHub issues](https://img.shields.io/github/issues/dydydd/123bot)](https://github.com/dydydd/123bot/issues)
[![GitHub license](https://img.shields.io/github/license/dydydd/123bot)](https://github.com/dydydd/123bot/blob/main/LICENSE)
[![Docker Pulls](https://img.shields.io/docker/pulls/dydydd/123bot)](https://hub.docker.com/r/dydydd/123bot)
[![Docker Build](https://github.com/dydydd/123bot/actions/workflows/docker-build.yml/badge.svg)](https://github.com/dydydd/123bot/actions/workflows/docker-build.yml)
[![Docker Image Size](https://img.shields.io/docker/image-size/dydydd/123bot/latest)](https://hub.docker.com/r/dydydd/123bot)

**一个功能强大的 Telegram 云盘自动化转存工具，支持多平台云盘自动转存、离线下载、秒传和 302 播放**

[功能特性](#-功能特性) •
[快速开始](#-快速开始) •
[使用文档](#-使用文档) •
[配置说明](#-配置说明) •
[常见问题](#-常见问题)

</div>

---

## 📋 目录

- [功能特性](#-功能特性)
- [系统架构](#-系统架构)
- [快速开始](#-快速开始)
  - [使用 Docker Compose（推荐）](#使用-docker-compose推荐)
  - [使用 Docker Hub 镜像](#使用-docker-hub-镜像)
  - [本地开发部署](#本地开发部署)
- [使用文档](#-使用文档)
- [配置说明](#-配置说明)
- [API 接口](#-api-接口)
- [常见问题](#-常见问题)
- [开发指南](#-开发指南)
- [许可证](#-许可证)
- [免责声明](#-免责声明)

---

## ✨ 功能特性

### 🔄 多平台云盘支持
- **123云盘** - 完整支持分享链接转存、离线下载、秒传功能
- **115云盘** - 支持分享链接转存、Cookie 认证
- **天翼云盘** - 支持分享链接转存、账号密码认证

### 📡 Telegram 集成
- 🤖 Telegram Bot 交互界面
- 📢 自动监控频道分享链接
- 💬 支持私聊和群组操作
- 🔔 实时转存状态通知
- 📊 转存统计和报告

### 🎬 媒体功能
- **302 播放** - 直接生成视频在线播放链接
- **弹幕支持** - 自动下载视频弹幕文件（支持 Misaka Danmaku API）
- **多线路播放** - 支持最多 5 个播放线路
- **实时转码** - 兼容各种播放器

### ⚡ 高级功能
- **秒传支持** - JSON 格式秒传到 123 和 115
- **磁力下载** - 123云盘离线下载磁力链接
- **批量转存** - 支持批量链接处理
- **智能过滤** - 支持关键词过滤和排除规则
- **定时任务** - 自动清理和整理功能

### 🛡️ 安全特性
- **AI 内容检测** - 集成 AI 辅助检测敏感内容
- **账号保护** - 避免违规内容导致账号封禁
- **访问控制** - Web 管理界面密码保护
- **Session 管理** - 安全的会话管理机制

### 🎯 Web 管理面板
- 🌐 现代化的 Web 界面
- ⚙️ 在线配置管理
- 📈 实时状态监控
- 🎨 响应式设计，支持移动端

---

## 🏗️ 系统架构

```
123bot/
├── 123bot.py          # 主程序 - 123云盘监控转存
├── 115bot.py          # 115云盘监控转存
├── 189bot.py          # 天翼云盘监控转存
├── server.py          # Web 服务器
├── share.py           # 分享链接生成
├── ptto123.py         # 本地文件秒传到123
├── ptto115.py         # 本地文件秒传到115
├── quark.py           # 夸克云盘转存
├── content_check.py   # AI 内容检测
├── danmu.py           # 弹幕下载
└── docker-compose.yml # Docker 编排配置
```

---

## 🚀 快速开始

### 📋 环境要求

- **Docker** >= 20.10 (推荐)
- **Docker Compose** >= 2.0
- **Python** >= 3.8 (本地运行)

### 使用 Docker Compose（推荐）

#### 1️⃣ 克隆项目

```bash
git clone --recursive https://github.com/dydydd/123bot.git
cd 123bot
```

> 💡 注意：使用 `--recursive` 参数克隆子模块

#### 2️⃣ 配置环境变量

编辑 `docker-compose.yml` 文件，填入必要的配置：

```yaml
environment:
  # Web 管理界面登录（必填）
  - ENV_WEB_PASSPORT=admin              # 修改为您的用户名
  - ENV_WEB_PASSWORD=your_password      # 修改为强密码
  
  # Telegram Bot 配置（必填）
  - ENV_TG_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz  # Bot Token
  - ENV_TG_ADMIN_USER_ID=123456789      # 您的 User ID
  
  # 123云盘配置（必填）
  - ENV_123_CLIENT_ID=your_client_id
  - ENV_123_CLIENT_SECRET=your_client_secret
```

#### 3️⃣ 启动服务

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f bot123

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

#### 4️⃣ 访问服务

- 🌐 **Web 管理界面**: http://your-server-ip:12366
- 🎬 **302 播放**: http://your-server-ip:12366/d/文件路径
- 🤖 **Telegram Bot**: 向 Bot 发送 `/start`

---

### 使用 Docker Hub 镜像

直接从 Docker Hub 拉取预构建镜像：

```bash
# 拉取最新镜像
docker pull dydydd/123bot:latest

# 运行容器
docker run -d \
  --name bot123 \
  --network host \
  -p 12366:12366 \
  -e TZ=Asia/Shanghai \
  -e ENV_TG_BOT_TOKEN=your_bot_token \
  -e ENV_TG_ADMIN_USER_ID=your_user_id \
  -e ENV_WEB_PASSPORT=admin \
  -e ENV_WEB_PASSWORD=your_password \
  -e ENV_123_CLIENT_ID=your_client_id \
  -e ENV_123_CLIENT_SECRET=your_client_secret \
  -v /path/to/db:/app/db \
  -v /path/to/upload:/app/upload \
  -v /path/to/transfer:/app/transfer \
  --restart always \
  dydydd/123bot:latest
```

**Docker 常用命令**

```bash
# 查看容器状态
docker ps

# 查看实时日志
docker logs -f bot123

# 进入容器调试
docker exec -it bot123 /bin/bash

# 停止/启动/重启
docker stop/start/restart bot123

# 删除容器
docker rm -f bot123

# 查看镜像
docker images | grep 123bot
```

---

### 本地开发部署

#### 1️⃣ 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装子模块依赖
pip install ./p123client
pip install ./p115client
```

#### 2️⃣ 配置环境

```bash
# 复制配置模板
cp templete.env db/user.env

# 编辑配置文件
nano db/user.env
```

#### 3️⃣ 启动服务

```bash
# 启动主程序
python 123bot.py

# 或启动 Web 服务器
python server.py
```

---

## 📖 使用文档

### Telegram Bot 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `/start` | 启动机器人，查看使用说明 | `/start` |
| `/share` | 创建分享链接 | `/share` 然后选择文件 |
| `/info` | 查看账号信息 | `/info` |
| `/add` | 添加转存任务 | 直接发送分享链接 |
| `/remove` | 删除文件 | `/remove` 然后选择文件 |

### Web 管理界面

访问 `http://your-server-ip:12366` 进入管理界面：

1. 使用配置的用户名和密码登录
2. 可以在线修改配置参数
3. 保存后自动重启应用新配置

### 302 播放接口

#### 基础用法

```
http://your-server-ip:12366/d/文件路径
```

#### 多线路播放

支持最多 5 个播放线路，适配不同播放器：

```
http://your-server-ip:12366/xiaohao1/文件路径  # 线路1
http://your-server-ip:12366/xiaohao2/文件路径  # 线路2
http://your-server-ip:12366/xiaohao3/文件路径  # 线路3
http://your-server-ip:12366/xiaohao4/文件路径  # 线路4
http://your-server-ip:12366/xiaohao5/文件路径  # 线路5
```

---

## ⚙️ 配置说明

### 必填配置

| 配置项 | 说明 | 获取方式 |
|--------|------|----------|
| `ENV_TG_BOT_TOKEN` | Telegram Bot Token | [@BotFather](https://t.me/BotFather) |
| `ENV_TG_ADMIN_USER_ID` | 管理员 User ID | [@userinfobot](https://t.me/userinfobot) |
| `ENV_123_CLIENT_ID` | 123云盘 Client ID | [123云盘开放平台](https://open.123pan.com/) |
| `ENV_123_CLIENT_SECRET` | 123云盘 Client Secret | [123云盘开放平台](https://open.123pan.com/) |
| `ENV_WEB_PASSPORT` | Web 管理界面用户名 | 自定义 |
| `ENV_WEB_PASSWORD` | Web 管理界面密码 | 自定义（建议强密码）|

### 可选配置

<details>
<summary>点击展开查看更多配置项</summary>

#### 115云盘配置
- `ENV_115_COOKIES` - 115云盘 Cookie

#### 天翼云盘配置
- `ENV_189_CLIENT_ID` - 天翼云盘 Client ID
- `ENV_189_CLIENT_SECRET` - 天翼云盘 Client Secret

#### 监控配置
- `ENV_TG_CHANNEL` - 监控的频道链接（多个用 | 分隔）
- `ENV_FILTER` - 关键词过滤（保留）
- `ENV_EXCLUDE_FILTER` - 关键词排除（过滤）
- `ENV_CHECK_INTERVAL` - 检查间隔（分钟）

#### 123云盘功能配置
- `ENV_123_LINK_UPLOAD_PID` - 链接转存目标目录 ID
- `ENV_123_MAGNET_UPLOAD_PID` - 磁力下载目标目录 ID
- `ENV_123_JSON_UPLOAD_PID` - JSON 秒传目标目录 ID
- `ENV_123_UPLOAD_PID` - 默认上传目录 ID

#### AI 内容检测
- `ENV_AI_API_URL` - AI API 地址
- `ENV_AI_API_KEY` - AI API 密钥

#### 弹幕配置
- `DANMAKU_API_URL` - 弹幕 API 地址
- `DANMAKU_API_KEY` - 弹幕 API 密钥

</details>

详细配置说明请参考 [`templete.env`](templete.env) 文件。

---

## 🔌 API 接口

### Web API

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/login` | POST | 用户登录 |
| `/api/logout` | POST/GET | 退出登录 |
| `/api/env` | GET | 获取配置 |
| `/api/env` | POST | 保存配置 |

### 播放接口

| 接口 | 说明 |
|------|------|
| `/d/<path>` | 302 重定向到下载链接 |
| `/xiaohao1/<path>` | 播放线路 1 |
| `/xiaohao2/<path>` | 播放线路 2 |
| `/xiaohao3/<path>` | 播放线路 3 |
| `/xiaohao4/<path>` | 播放线路 4 |
| `/xiaohao5/<path>` | 播放线路 5 |

---

## ❓ 常见问题

<details>
<summary><b>如何获取 Telegram Bot Token？</b></summary>

1. 在 Telegram 中搜索 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 创建新机器人
3. 按提示设置机器人名称和用户名
4. 获取 Bot Token（格式：`1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`）
5. 发送 `/setcommands` 设置机器人命令菜单

</details>

<details>
<summary><b>如何获取 Telegram User ID？</b></summary>

1. 在 Telegram 中搜索 [@userinfobot](https://t.me/userinfobot)
2. 向机器人发送任意消息
3. 获取您的 User ID（纯数字）

</details>

<details>
<summary><b>如何获取 123云盘凭证？</b></summary>

1. 访问 [123云盘开放平台](https://open.123pan.com/)
2. 使用 123云盘账号登录
3. 创建应用并获取 Client ID 和 Client Secret
4. 注意保管好凭证，不要泄露

</details>

<details>
<summary><b>为什么无法转存 115/天翼云盘？</b></summary>

确保已正确配置对应云盘的凭证：
- **115云盘**: 需要配置 `ENV_115_COOKIES`
- **天翼云盘**: 需要配置 `ENV_189_CLIENT_ID` 和 `ENV_189_CLIENT_SECRET`

如果未配置，相关功能将不可用。

</details>

<details>
<summary><b>如何修改配置？</b></summary>

**方式一：Web 界面**
1. 访问 http://your-server-ip:12366
2. 登录后在线修改配置
3. 点击保存，容器自动重启

**方式二：手动修改**
```bash
# 编辑配置文件
docker exec -it bot123 /bin/bash
nano /app/db/user.env

# 重启容器使配置生效
docker restart bot123
```

</details>

<details>
<summary><b>如何查看日志？</b></summary>

```bash
# 查看实时日志
docker logs -f bot123

# 查看最近 100 行日志
docker logs --tail 100 bot123

# 查看日志文件
docker exec -it bot123 cat /app/db/log/start-log.log
```

</details>

<details>
<summary><b>容器无法启动怎么办？</b></summary>

1. 检查配置是否正确
2. 查看容器日志：`docker logs bot123`
3. 确保端口 12366 未被占用
4. 检查 Docker 和 Docker Compose 版本
5. 尝试重新构建：`docker-compose build --no-cache`

</details>

---

## 👨‍💻 开发指南

### 项目结构

```
123bot/
├── 123bot.py              # 主程序
├── bot115.py              # 115云盘模块
├── bot189.py              # 天翼云盘模块
├── server.py              # Web 服务器
├── share.py               # 分享功能
├── content_check.py       # 内容检测
├── danmu.py               # 弹幕下载
├── templates/             # HTML 模板
│   ├── index.html        # 配置页面
│   └── login.html        # 登录页面
├── static/                # 静态资源
│   ├── styles.css        # 样式表
│   └── script.js         # 脚本
├── p123client/            # 123云盘客户端（子模块）
├── p115client/            # 115云盘客户端（子模块）
├── docker-compose.yml     # Docker 编排
├── Dockerfile             # Docker 镜像构建
├── requirements.txt       # Python 依赖
└── templete.env          # 配置模板
```

### 本地开发

```bash
# 1. 克隆项目
git clone --recursive https://github.com/dydydd/123bot.git
cd 123bot

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt
pip install -e ./p123client
pip install -e ./p115client

# 4. 配置环境
cp templete.env db/user.env
# 编辑 db/user.env

# 5. 运行开发服务器
python server.py  # Web 服务器
python 123bot.py  # 主程序
```

### 贡献代码

我们欢迎任何形式的贡献！

1. Fork 本仓库
2. 创建新分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 代码规范

- 遵循 PEP 8 Python 编码规范
- 添加适当的注释和文档
- 编写测试用例
- 更新 README 文档

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=dydydd/123bot&type=Date)](https://star-history.com/#dydydd/123bot&Date)


## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源。

```
MIT License

Copyright (c) 2025 dydydd

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## ⚠️ 免责声明

**重要声明**：

1. **仅供学习交流使用**
   - 本项目仅供学习和研究使用
   - 请勿用于任何商业用途
   - 使用者需自行承担使用本工具的所有风险

2. **遵守法律法规**
   - 请遵守当地法律法规
   - 请遵守云盘服务条款
   - 请勿传播违法违规内容
   - 请勿侵犯他人知识产权

3. **风险提示**
   - 使用本工具可能违反云盘服务条款
   - 可能导致账号被封禁或限制
   - 开发者不对任何损失负责
   - 使用前请充分了解风险

4. **隐私保护**
   - 妥善保管配置文件和凭证
   - 定期更改密码
   - 不要在公共场合泄露敏感信息

**使用本工具即表示您已阅读、理解并同意以上所有声明。**

---

## 📮 联系方式

- **GitHub**: https://github.com/dydydd/123bot
- **Issues**: https://github.com/dydydd/123bot/issues
- **Docker Hub**: https://hub.docker.com/r/dydydd/123bot

---

<div align="center">

### 如果这个项目对您有帮助，请给个 ⭐️ Star 支持一下！

**Made with ❤️ by [dydydd](https://github.com/dydydd)**

</div>
