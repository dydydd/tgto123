# GitHub Actions 工作流

本目录包含 123bot 项目的 CI/CD 自动化工作流配置。

## 📋 工作流说明

### 1. `docker-build.yml` - Docker 镜像构建

**触发条件：**
- 推送到 `main` 分支
- 推送带有 `v*.*.*` 格式的标签
- Pull Request 到 `main` 分支

**功能：**
- ✅ 自动构建 Docker 镜像
- ✅ 多平台支持（amd64, arm64）
- ✅ 自动推送到 Docker Hub
- ✅ 使用 GitHub Actions 缓存加速构建
- ✅ 自动生成镜像标签

**生成的标签：**
- `latest` - 最新的 main 分支构建
- `main` - main 分支构建
- `v1.0.0` - 版本标签（如果推送标签）
- `1.0` - 主次版本号
- `1` - 主版本号

### 2. `docker-release.yml` - 发布版本构建

**触发条件：**
- 在 GitHub 上创建 Release

**功能：**
- ✅ 构建正式版本镜像
- ✅ 多平台支持（amd64, arm64, arm/v7）
- ✅ 推送到 Docker Hub
- ✅ 自动更新 Docker Hub 描述
- ✅ 同时打上版本标签和 latest 标签

## 🔧 配置步骤

### 1. 设置 Docker Hub Secrets

在 GitHub 仓库中设置以下 Secrets：

1. 进入仓库页面
2. 点击 `Settings` > `Secrets and variables` > `Actions`
3. 点击 `New repository secret` 添加以下 Secrets：

| Secret 名称 | 说明 | 获取方式 |
|-------------|------|----------|
| `DOCKER_USERNAME` | Docker Hub 用户名 | 您的 Docker Hub 账号 |
| `DOCKER_PASSWORD` | Docker Hub 访问令牌 | [创建访问令牌](https://hub.docker.com/settings/security) |

### 2. 创建 Docker Hub 访问令牌

1. 登录 [Docker Hub](https://hub.docker.com/)
2. 点击右上角头像 > `Account Settings`
3. 选择 `Security` > `New Access Token`
4. 输入令牌名称（如：`github-actions`）
5. 选择权限：`Read, Write, Delete`
6. 点击 `Generate` 生成令牌
7. 复制令牌（只会显示一次）
8. 将令牌添加到 GitHub Secrets 的 `DOCKER_PASSWORD`

## 🚀 使用方法

### 自动构建（推送到 main）

```bash
# 提交代码
git add .
git commit -m "feat: add new feature"
git push origin main
```

推送后，GitHub Actions 会自动：
1. ✅ 构建 Docker 镜像
2. ✅ 推送到 `dydydd/123bot:main` 和 `dydydd/123bot:latest`

### 发布版本

#### 方法一：通过 GitHub Release（推荐）

1. 在 GitHub 仓库页面点击 `Releases`
2. 点击 `Draft a new release`
3. 选择或创建标签（如 `v1.0.0`）
4. 填写发布说明
5. 点击 `Publish release`

#### 方法二：通过 Git 命令

```bash
# 创建并推送标签
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 然后在 GitHub 上基于此标签创建 Release
```

发布后，GitHub Actions 会自动：
1. ✅ 构建多平台 Docker 镜像
2. ✅ 推送到 `dydydd/123bot:v1.0.0` 和 `dydydd/123bot:latest`
3. ✅ 更新 Docker Hub 仓库描述

## 📊 查看构建状态

### 在 GitHub 上查看

1. 进入仓库页面
2. 点击 `Actions` 标签
3. 查看工作流运行状态

### 徽章

在 README.md 中添加构建状态徽章：

```markdown
[![Docker Build](https://github.com/dydydd/123bot/actions/workflows/docker-build.yml/badge.svg)](https://github.com/dydydd/123bot/actions/workflows/docker-build.yml)
```

## 🐛 故障排查

### 构建失败

1. **Secrets 未配置**
   - 检查 `DOCKER_USERNAME` 和 `DOCKER_PASSWORD` 是否正确设置

2. **Docker Hub 登录失败**
   - 确认访问令牌权限正确
   - 尝试重新生成令牌

3. **构建超时**
   - GitHub Actions 默认超时 6 小时
   - 多平台构建可能需要较长时间

4. **子模块未正确克隆**
   - 确保工作流使用 `submodules: recursive`

### 推送失败

1. **权限不足**
   - 确认 Docker Hub 访问令牌有 Write 权限

2. **仓库不存在**
   - 先在 Docker Hub 创建仓库 `dydydd/123bot`

## 📝 最佳实践

### 版本号规范

遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

- `v1.0.0` - 主版本.次版本.修订号
- `v1.0.0-beta.1` - 预发布版本
- `v1.0.0+20230101` - 构建元数据

### 提交信息规范

使用 [约定式提交](https://www.conventionalcommits.org/zh-hans/)：

- `feat:` - 新功能
- `fix:` - 错误修复
- `docs:` - 文档更新
- `style:` - 代码格式
- `refactor:` - 代码重构
- `perf:` - 性能优化
- `test:` - 测试相关
- `chore:` - 构建/工具链

### 发布流程

1. 更新 `CHANGELOG.md`
2. 更新版本号
3. 提交并推送更改
4. 创建 Git 标签
5. 在 GitHub 创建 Release
6. 等待自动构建完成
7. 验证 Docker Hub 镜像

## 🔗 相关链接

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Docker Build Action](https://github.com/docker/build-push-action)
- [Docker Hub](https://hub.docker.com/r/dydydd/123bot)

