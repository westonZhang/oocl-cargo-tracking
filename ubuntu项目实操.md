# Ubuntu 22.04 项目实操指南

## 1. 环境准备

在 Ubuntu 22.04 系统上，我们需要安装一些必要的软件和依赖，以确保项目能够顺利运行。

### 1.1 安装 Git

Git 是版本控制工具，用于管理项目代码。

```bash
# 更新软件包列表
sudo apt update
# 安装 Git
sudo apt install -y git
# 验证安装
git --version
```

### 1.2 安装 Python 和 pip

项目使用 Python 开发，需要安装 Python 3.6+ 和 pip 包管理器。

```bash
# 安装 Python 3 和 pip
sudo apt install -y python3 python3-pip
# 验证安装
python3 --version
pip3 --version
```

### 1.3 配置 Git 用户名和邮箱

第一次使用 Git 时，需要配置用户名和邮箱，这些信息会出现在你的提交记录中。

```bash
# 配置用户名
git config --global user.name "Your Name"
# 配置邮箱
git config --global user.email "your.email@example.com"
# 查看配置
git config --list
```

## 2. 项目克隆

现在我们可以从 GitHub 克隆项目代码到本地。

### 2.1 克隆项目

```bash
# 方式1：使用 HTTPS 地址（推荐，无需配置 SSH 密钥）
git clone https://github.com/westonZhang/oocl-cargo-tracking.git
# 方式2：使用 SSH 地址（需要配置 SSH 密钥）
# git clone git@github.com:westonZhang/oocl-cargo-tracking.git
```

### 2.2 进入项目目录

```bash
cd oocl-cargo-tracking
```

## 3. 功能分支开发 - 为集装箱添加“危险品”标识

### 3.1 准备开发环境

确保本地代码是最新的。

```bash
# 切换到 main 分支
git checkout main
# 从远程仓库拉取最新的代码
git pull origin main
```

### 3.2 创建功能分支

```bash
# 创建一个描述清晰的功能分支
git checkout -b feature/add-dangerous-goods-flag
```

### 3.3 开发与提交

#### 3.3.1 创建目录结构

首先创建所需的目录结构：

```bash
# 创建必要的目录
mkdir -p models api utils
```

#### 3.3.2 实现集装箱模型

创建并编辑 `models/container.py` 文件：

```bash
# 使用 nano 编辑器创建文件
nano models/container.py
```

在编辑器中输入以下内容：

```python
class Container:
    def __init__(self, container_id, weight, port_of_origin):
        self.container_id = container_id
        self.weight = weight
        self.port_of_origin = port_of_origin
        # 新增属性：是否为危险品，默认为False
        self.is_dangerous_goods = False
```

按 `Ctrl + O` 保存文件，按 `Ctrl + X` 退出编辑器。

#### 3.3.3 实现 API 接口

创建并编辑 `api/containers.py` 文件：

```bash
nano api/containers.py
```

输入以下内容：

```python
from flask import Flask, jsonify
from models.container import Container

app = Flask(__name__)

# 测试数据
containers = {
    "OOCL123": Container("OOCL123", 25000, "Shanghai"),
    "OOCL456": Container("OOCL456", 30000, "Singapore"),
    "OOCL789": Container("OOCL789", 20000, "Rotterdam")
}

# 模拟根据ID查找集装箱的函数
def find_container_by_id(container_id):
    return containers.get(container_id)

@app.route('/containers/<container_id>', methods=['GET'])
def get_container_details(container_id):
    """
    获取集装箱详细信息
    :param container_id: 集装箱ID
    :return: 包含集装箱详细信息的JSON响应
    """
    container = find_container_by_id(container_id)
    if not container:
        return jsonify({"error": "Container not found"}), 404
    
    # 返回的JSON中包含危险品信息
    return jsonify({
        "container_id": container.container_id,
        "weight": container.weight,
        "port_of_origin": container.port_of_origin,
        # is_dangerous_goods 字段说明：True表示危险品，False表示非危险品
        "is_dangerous_goods": container.is_dangerous_goods 
    })

if __name__ == '__main__':
    app.run(debug=True)
```

保存并退出编辑器。

#### 3.3.4 创建依赖文件

创建 `requirements.txt` 文件：

```bash
nano requirements.txt
```

输入以下内容：

```
flask
pytz
```

保存并退出编辑器。

#### 3.3.5 提交代码

```bash
# 查看状态
git status
# 添加所有修改的文件
git add models/container.py api/containers.py requirements.txt
# 提交，使用约定式提交信息
git commit -m "feat(container): add dangerous goods flag to model and API"
```

### 3.4 推送并创建 Pull Request (PR)

```bash
# 将功能分支推送到远程仓库
git push origin feature/add-dangerous-goods-flag
```

然后，在 GitHub 上创建一个 PR：

1. 打开项目 GitHub 页面：`https://github.com/westonZhang/oocl-cargo-tracking`
2. 点击 "Compare & pull request" 按钮
3. 填写 PR 标题和描述
4. 指定审查者
5. 点击 "Create pull request"

## 4. 紧急 Bug 修复 - 航线信息显示错误

### 4.1 快速响应

```bash
# 确保本地 main 是最新的
git checkout main
git pull origin main
# 创建一个紧急修复分支
git checkout -b hotfix/fix-eta-calculation-bug
```

### 4.2 定位并修复 Bug

#### 4.2.1 确保 utils 目录存在

```bash
# 确保utils目录存在
mkdir -p utils
```

#### 4.2.2 实现航运计算器

创建并编辑 `utils/shipping_calculator.py` 文件：

```bash
nano utils/shipping_calculator.py
```

输入以下内容：

```python
import pytz
from datetime import datetime, timedelta

# 模拟获取航行天数的函数
def get_voyage_duration_in_days(origin_port, destination_port):
    """
    模拟获取航行天数
    :param origin_port: 出发港
    :param destination_port: 目的港
    :return: 航行天数
    """
    # 简单模拟，实际应该从数据库或配置中获取
    return 10

def calculate_eta(origin_port, destination_port, departure_time):
    """
    计算集装箱的预计到港时间，已修复夏令时问题。
    :param origin_port: 出发港对象，包含timezone属性
    :param destination_port: 目的港对象，包含timezone属性
    :param departure_time: 出发时间，datetime对象（带时区信息）
    :return: 预计到港时间，datetime对象（带目的港时区信息）
    """
    # 获取目的港的时区
    dest_tz = pytz.timezone(destination_port.timezone)
    
    # 将航行天数转换为时间差
    voyage_duration = timedelta(days=get_voyage_duration_in_days(origin_port, destination_port))
    
    # 计算原始 ETA
    raw_eta = departure_time + voyage_duration
    
    # 关键修复：将时间正确地转换到目的港的时区，并处理夏令时
    localized_eta = raw_eta.astimezone(dest_tz)
    
    return localized_eta
```

保存并退出编辑器。

#### 4.2.3 提交修复

```bash
# 添加修改的文件
git add utils/shipping_calculator.py
# 提交，使用约定式提交信息
git commit -m "fix(shipping): correct ETA calculation to handle daylight saving time"
# 将热修复分支推送到远程仓库
git push origin hotfix/fix-eta-calculation-bug
```

### 4.3 创建 PR 并合并

在 GitHub 上创建一个 PR，标题为 `fix(shipping): correct ETA calculation to handle daylight saving time`，并标记为 `urgent`。

等待团队领导审查并合并 PR。

## 5. 同步与继续开发

当 `main` 分支有新的提交时，需要同步到功能分支。

```bash
# 切换到功能分支
git checkout feature/add-dangerous-goods-flag
# 获取远程的最新更新
git fetch origin
# 将 main 分支的最新修改合并到自己的功能分支
git rebase origin/main
```

## 6. 文档更新

项目开发完成后，需要更新文档以便后续开发者使用。

### 6.1 更新 README.md

```bash
# 切换到 main 分支
git checkout main
# 拉取最新代码
git pull origin main
# 编辑 README.md 文件
nano README.md
# 在编辑器中添加项目介绍、使用指南等内容
# ... 编辑内容 ...
# 保存并退出编辑器
# 提交文档更新
git add README.md
git commit -m "docs: update README with project introduction and usage guide"
git push origin main
```

## 7. 常见问题和解决方案

### 7.1 克隆失败

**问题**：使用 HTTPS 克隆时提示 "fatal: Authentication failed for..."

**解决方案**：
1. 确保 GitHub 用户名和密码正确
2. 如果使用两步验证，需要使用个人访问令牌代替密码
3. 或者使用 SSH 方式克隆

### 7.2 推送失败

**问题**：`git push` 时提示 "Permission denied (publickey)"

**解决方案**：
1. 检查 SSH 密钥是否正确配置
2. 或者切换到 HTTPS 方式推送

### 7.3 Python 依赖安装失败

**问题**：`pip install -r requirements.txt` 时提示权限错误

**解决方案**：
1. 使用 `--user` 选项安装到用户目录
   ```bash
   pip3 install --user -r requirements.txt
   ```
2. 或者使用虚拟环境

### 7.4 端口被占用

**问题**：启动 Flask 服务器时提示 "Address already in use"

**解决方案**：
1. 查找占用端口的进程
   ```bash
   sudo lsof -i :5000
   ```
2. 终止占用端口的进程
   ```bash
   sudo kill -9 <PID>
   ```
3. 或者修改 Flask 服务器端口

## 8. 总结

通过本指南，你已经学会了在 Ubuntu 22.04 系统上完成项目开发的完整流程，包括：

1. 环境准备（安装 Git、Python、配置 Git）
2. 项目克隆
3. 功能分支开发
4. 紧急 Bug 修复
5. 代码同步
6. 文档更新
7. 常见问题解决方案

这些步骤展示了完整的 Git 工作流，包括功能开发、紧急修复、代码同步和文档更新等核心操作。遵循这些步骤，可以确保项目开发的高效性和代码的质量。