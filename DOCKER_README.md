# 123bot - Telegram 云盘自动转存机器人

[![Docker Pulls](https://img.shields.io/docker/pulls/dydydd/123bot)](https://hub.docker.com/r/dydydd/123bot)
[![Docker Image Size](https://img.shields.io/docker/image-size/dydydd/123bot/latest)](https://hub.docker.com/r/dydydd/123bot)
[![GitHub](https://img.shields.io/github/license/dydydd/123bot)](https://github.com/dydydd/123bot)

一个功能强大的 Telegram 云盘自动化转存工具，支持 123云盘、115云盘、天翼云盘的自动转存、离线下载、秒传和 302 播放功能。

## ✨ 主要特性

- 🔄 **多平台云盘支持** - 支持 123云盘、115云盘、天翼云盘
- 📡 **Telegram Bot 交互** - 完整的机器人命令支持
- 📢 **频道监控** - 自动监控 Telegram 频道的分享链接
- 🎬 **302 播放** - 直接生成视频在线播放链接
- ⚡ **秒传功能** - 支持 JSON 格式秒传
- 🧲 **磁力下载** - 123云盘离线下载磁力链接
- 🛡️ **AI 内容检测** - 避免违规内容导致账号封禁
- 🌐 **Web 管理界面** - 现代化的在线配置管理

## 🚀 快速开始

### 使用 Docker Compose（推荐）

1. 创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  bot123:
    image: dydydd/123bot:latest
    container_name: bot123
    restart: always
    network_mode: host
    ports:
      - "12366:12366"
    volumes:
      - ./db:/app/db
      - ./upload:/app/upload
      - ./transfer:/app/transfer
    environment:
      - TZ=Asia/Shanghai
      - ENV_TG_BOT_TOKEN=your_bot_token
      - ENV_TG_ADMIN_USER_ID=your_user_id
      - ENV_WEB_PASSPORT=admin
      - ENV_WEB_PASSWORD=your_password
      - ENV_123_CLIENT_ID=your_client_id
      - ENV_123_CLIENT_SECRET=your_client_secret
```

2. 启动容器：

```bash
docker-compose up -d
```

### 使用 Docker Run

```bash
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
  -v $(pwd)/db:/app/db \
  -v $(pwd)/upload:/app/upload \
  -v $(pwd)/transfer:/app/transfer \
  --restart always \
  dydydd/123bot:latest
```

## ⚙️ 环境变量配置

### 必填配置

| 变量名 | 说明 | 获取方式 |
|--------|------|----------|
| `ENV_TG_BOT_TOKEN` | Telegram Bot Token | [@BotFather](https://t.me/BotFather) |
| `ENV_TG_ADMIN_USER_ID` | 管理员 User ID | [@userinfobot](https://t.me/userinfobot) |
| `ENV_123_CLIENT_ID` | 123云盘 Client ID | [123云盘开放平台](https://open.123pan.com/) |
| `ENV_123_CLIENT_SECRET` | 123云盘 Client Secret | [123云盘开放平台](https://open.123pan.com/) |
| `ENV_WEB_PASSPORT` | Web 界面用户名 | 自定义 |
| `ENV_WEB_PASSWORD` | Web 界面密码 | 自定义 |

### 可选配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `ENV_115_COOKIES` | 115云盘 Cookie | - |
| `ENV_189_CLIENT_ID` | 天翼云盘 Client ID | - |
| `ENV_189_CLIENT_SECRET` | 天翼云盘 Client Secret | - |
| `ENV_TG_CHANNEL` | 监控的频道链接（多个用\|分隔）| - |
| `ENV_FILTER` | 关键词过滤（保留）| - |
| `ENV_EXCLUDE_FILTER` | 关键词排除 | - |
| `ENV_CHECK_INTERVAL` | 检查间隔（分钟）| 5 |
| `ENV_123_LINK_UPLOAD_PID` | 链接转存目标目录 ID | 0 |
| `ENV_123_MAGNET_UPLOAD_PID` | 磁力下载目标目录 ID | 0 |

完整配置列表请参考 [GitHub 仓库](https://github.com/dydydd/123bot)。

## 📖 使用说明

### 访问服务

- **Web 管理界面**: `http://your-server-ip:12366`
- **302 播放接口**: `http://your-server-ip:12366/d/文件路径`
- **Telegram Bot**: 向 Bot 发送 `/start` 开始使用

### Telegram Bot 命令

| 命令 | 说明 |
|------|------|
| `/start` | 启动机器人，查看使用说明 |
| `/share` | 创建分享链接 |
| `/info` | 查看账号信息 |
| `/add` | 添加转存任务（直接发送分享链接）|
| `/remove` | 删除文件 |

### 302 播放接口

支持 5 条播放线路，适配不同播放器：

```
http://your-server-ip:12366/d/文件路径       # 默认线路
http://your-server-ip:12366/xiaohao1/文件路径  # 线路1
http://your-server-ip:12366/xiaohao2/文件路径  # 线路2
http://your-server-ip:12366/xiaohao3/文件路径  # 线路3
http://your-server-ip:12366/xiaohao4/文件路径  # 线路4
http://your-server-ip:12366/xiaohao5/文件路径  # 线路5
```

## 🔍 查看日志

```bash
# 实时查看日志
docker logs -f bot123

# 查看最近 100 行
docker logs --tail 100 bot123
```

## 🔄 更新镜像

```bash
# 停止容器
docker stop bot123

# 删除容器
docker rm bot123

# 拉取最新镜像
docker pull dydydd/123bot:latest

# 重新运行容器（使用之前的 docker run 命令）
```

或使用 Docker Compose：

```bash
docker-compose pull
docker-compose up -d
```

## 🏷️ 镜像标签

| 标签 | 说明 |
|------|------|
| `latest` | 最新稳定版本 |
| `main` | 主分支最新构建 |
| `v1.0.0` | 特定版本号 |

## 🐛 常见问题

### 容器无法启动

- 检查配置是否正确
- 确保端口 12366 未被占用
- 查看日志：`docker logs bot123`

### 无法访问 Web 界面

- 确认端口映射正确
- 检查防火墙设置
- 确认容器正在运行：`docker ps`

### Bot 无法使用

- 确认 Bot Token 正确
- 确认 User ID 正确
- 检查网络连接

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/dydydd/123bot
- **问题反馈**: https://github.com/dydydd/123bot/issues
- **完整文档**: https://github.com/dydydd/123bot#readme

## 📋 支持的架构

- `linux/amd64` - x86_64 架构
- `linux/arm64` - ARM64 架构（如 Raspberry Pi 4）
- `linux/arm/v7` - ARMv7 架构

## ⚠️ 免责声明

- 本项目仅供学习交流使用，请勿用于商业用途
- 使用本工具产生的任何法律责任由使用者自行承担
- 请遵守相关云盘服务条款，合理使用存储资源
- 请勿传播违法违规内容

## 📄 许可证

本项目基于 [MIT License](https://github.com/dydydd/123bot/blob/main/LICENSE) 开源。

---

**Made with ❤️ by [dydydd](https://github.com/dydydd)**

如果这个项目对您有帮助，请在 [GitHub](https://github.com/dydydd/123bot) 给个 ⭐️ Star！

