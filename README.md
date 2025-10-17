# TGTO123 - Telegram云盘自动转存工具

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
git clone --recursive https://github.com/dydydd/tgto123.git
cd tgto123
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

```bash
python server.py
```

或使用Docker:

```bash
docker-compose up -d
```

## 主要模块说明

- `server.py` - Web服务主程序
- `tgto123.py` - 123云盘TG频道监控转存
- `tgto115.py` - 115云盘TG频道监控转存
- `tgto189.py` - 天翼云盘TG频道监控转存
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

## 许可证

本项目仅供学习交流使用,请勿用于商业用途。

## 贡献

欢迎提交Issue和Pull Request!

