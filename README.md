# 123BOT - Telegram云盘自动转存工具

这是一个功能强大的云盘自动化转存工具,支持监控Telegram频道并自动转存资源到多个云盘平台。

## 主要功能

- 🔄 **多平台支持**: 支持123云盘、115云盘、天翼云盘
- 📡 **Telegram频道监控**: 自动监控指定TG频道的分享链接
- 🔗 **链接转存**: 支持多种分享链接格式的自动转存
- 🧲 **磁力下载**: 支持123云盘离线下载磁力链接
- ⚡ **秒传功能**: 支持JSON秒传到123和115
- 🎬 **302播放**: 内置302播放功能,支持视频在线播放
- 🛡️ **AI内容检测**: 集成AI辅助色情内容检测,避免账号风险
- 📝 **弹幕支持**: 自动下载视频弹幕文件

## 环境要求

- Python 3.8+
- Docker (可选)

## 快速开始

### 1. 克隆项目

```bash
git clone --recursive https://github.com/dydydd/123bot.git
cd 123bot
```

### 2. 配置环境变量

复制 `templete.env` 为 `.env` 并根据需要填写配置:

```bash
cp templete.env .env
```

然后编辑 `.env` 文件,填入你的云盘账号密码等信息。

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行服务

#### 方式一：直接运行

```bash
python 123bot.py
```

#### 方式二：使用 Docker Compose（推荐）

**第一步：修改配置**

编辑 `docker-compose.yml` 文件，填入必要的环境变量：

```yaml
environment:
  # Web管理界面登录配置（必填）
  - ENV_WEB_PASSPORT=admin        # 修改为您的用户名
  - ENV_WEB_PASSWORD=123456       # 修改为您的密码
  
  # Telegram Bot配置（必填）
  - ENV_TG_BOT_TOKEN=your_bot_token          # 您的TG Bot Token
  - ENV_TG_ADMIN_USER_ID=your_user_id        # 您的TG用户ID
  
  # 123云盘配置（必填）
  - ENV_123_CLIENT_ID=your_client_id         # 123云盘Client ID
  - ENV_123_CLIENT_SECRET=your_client_secret # 123云盘Client Secret
```

**第二步：构建并启动容器**

```bash
# 构建镜像并启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f bot123

# 停止容器
docker-compose down

# 重启容器
docker-compose restart
```

#### 方式三：使用 Docker Hub 镜像

您也可以直接从 Docker Hub 拉取已构建好的镜像：

```bash
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
  -e ENV_WEB_PASSWORD=123456 \
  -e ENV_123_CLIENT_ID=your_client_id \
  -e ENV_123_CLIENT_SECRET=your_client_secret \
  -v /root/docker/db:/app/db \
  -v $(pwd)/upload:/app/upload \
  -v $(pwd)/transfer:/app/transfer \
  --restart always \
  dydydd/123bot:latest
```

**Docker 常用命令**

```bash
# 查看运行状态
docker ps

# 查看日志
docker logs -f bot123

# 进入容器
docker exec -it bot123 /bin/bash

# 停止容器
docker stop bot123

# 启动容器
docker start bot123

# 删除容器
docker rm bot123

# 查看镜像
docker images | grep 123bot
```

### 5. 访问服务

启动成功后，您可以通过以下方式访问：

- **Web管理界面**: http://your-server-ip:12366
- **302播放接口**: http://your-server-ip:12366/d/文件路径
- **Telegram Bot**: 向您的Bot发送 `/start` 开始使用

## 主要模块说明

- `server.py` - Web服务主程序
- `123bot.py` - 123云盘TG频道监控转存
- `115bot.py` - 115云盘TG频道监控转存
- `189bot.py` - 天翼云盘TG频道监控转存
- `ptto123.py` - 本地文件秒传到123
- `ptto115.py` - 本地文件秒传到115
- `quark.py` - 夸克云盘转存到123
- `share.py` - 123分享链接生成
- `content_check.py` - AI内容检测

## 配置说明

详细的配置说明请参考 `templete.env` 文件中的注释。

主要配置项包括:
- 123云盘账号配置
- 115云盘Cookie配置
- 天翼云盘账号配置
- TG频道监控配置
- AI内容检测API配置
- 弹幕API配置

## 注意事项

⚠️ **重要提醒**:
- 请勿滥用,遵守相关云盘服务条款
- 建议使用自己的AI API以获得更好的内容检测效果
- 妥善保管配置文件,避免泄露账号信息
- 定期备份重要数据

## Docker Hub

Docker 镜像托管地址：https://hub.docker.com/r/dydydd/123bot

## 常见问题

### 如何获取 Telegram Bot Token？

1. 在 Telegram 中搜索 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 创建新机器人
3. 按提示设置机器人名称和用户名
4. 获取 Bot Token

### 如何获取 Telegram User ID？

1. 在 Telegram 中搜索 [@userinfobot](https://t.me/userinfobot)
2. 向机器人发送任意消息
3. 获取您的 User ID

### 如何获取 123云盘 Client ID 和 Secret？

1. 访问 [123云盘开放平台](https://open.123pan.com/)
2. 登录并创建应用
3. 获取 Client ID 和 Client Secret

## 贡献

欢迎提交 Issue 和 Pull Request！

如果这个项目对您有帮助，请给个 ⭐️ Star 支持一下！

## 许可证

本项目基于 MIT 许可证开源。

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

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 免责声明

⚠️ **重要声明**：

- 本项目仅供学习交流使用，请勿用于商业用途
- 使用本工具产生的任何法律责任由使用者自行承担
- 请遵守相关云盘服务条款，合理使用存储资源
- 请勿传播违法违规内容

## 联系方式

- GitHub: https://github.com/dydydd/123bot
- Issues: https://github.com/dydydd/123bot/issues

