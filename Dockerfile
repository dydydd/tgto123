# 使用Python 3.13作为基础镜像
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 设置Python不缓冲输出
ENV PYTHONUNBUFFERED=1

# 【关键优化1】先复制依赖清单，单独安装（利用缓存）
COPY requirements.txt .
# 安装依赖（可选：使用国内镜像源加速下载）
RUN pip install -r requirements.txt
# 【关键优化2】再复制其他文件（代码变动不影响依赖层缓存）
COPY . /app

# 清理所有缓存文件
RUN find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true && \
    find . -type f -name "*.pyc" -delete

# 安装构建工具和本地包
RUN pip install --upgrade pip setuptools wheel && \
    pip install ./p123client && \
    pip install ./p115client

# 编译Python文件为.pyc
RUN python -m compileall -b .

# 删除原始的.py文件
RUN rm *.py

# 运行Python脚本
CMD ["python", "-O", "tgto123.pyc"]