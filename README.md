# oocl-cargo-tracking
珠海课程demo，用于git教学

## 项目介绍

### 项目概述
`oocl-cargo-tracking` 是一个内部的集装箱追踪与管理系统，用于演示 Git 工作流和团队协作开发。

### 核心功能
1. **集装箱数据管理**：存储和查询集装箱基本信息
2. **危险品标识**：标记集装箱是否为危险品，便于特殊处理
3. **航运计算**：计算集装箱的预计到港时间（ETA），已修复夏令时问题

### 技术栈
- Python 3.6+
- Flask：用于构建 RESTful API
- pytz：用于处理时区和夏令时

## 项目使用指南

### 1. 环境准备

#### 1.1 安装依赖
确保你的系统已安装 Python 3.6+，然后使用 `pip` 安装项目依赖：

```bash
# 在项目根目录执行
pip install -r requirements.txt
```

这将安装项目所需的依赖包：
- `flask`：用于构建 RESTful API
- `pytz`：用于处理时区和夏令时

### 2. 运行项目

#### 2.1 启动 API 服务
运行以下命令启动 Flask 开发服务器：

```bash
# 在项目根目录执行
python -m api.containers
```

服务器将在 `http://localhost:5000` 启动。

### 3. 测试功能

#### 3.1 测试 API 接口
使用浏览器或 `curl` 命令访问 API 接口，获取集装箱详细信息：

```bash
# 示例：获取集装箱 OOCL123 的信息
curl http://localhost:5000/containers/OOCL123
```

预期响应：
```json
{
  "container_id": "OOCL123",
  "weight": 25000,
  "port_of_origin": "Shanghai",
  "is_dangerous_goods": false
}
```

#### 3.2 测试航运计算器
你可以在 Python 脚本中使用 `shipping_calculator` 模块来计算 ETA：

```python
# 创建一个测试脚本 test_eta.py
from utils.shipping_calculator import calculate_eta
from datetime import datetime
import pytz

# 模拟端口对象，包含 timezone 属性
class Port:
    def __init__(self, name, timezone):
        self.name = name
        self.timezone = timezone

# 创建测试数据
origin_port = Port("Shanghai", "Asia/Shanghai")
destination_port = Port("Los Angeles", "America/Los_Angeles")

# 获取当前时间并添加时区信息
now = datetime.now(pytz.timezone(origin_port.timezone))

# 计算 ETA
eta = calculate_eta(origin_port, destination_port, now)
print(f"预计到港时间：{eta}")
```

运行测试脚本：
```bash
python test_eta.py
```

### 4. 项目结构说明

#### 4.1 核心模块

##### `models/container.py`
定义了 `Container` 类，包含以下属性：
- `container_id`：集装箱ID
- `weight`：重量（单位：千克）
- `port_of_origin`：出发港
- `is_dangerous_goods`：是否为危险品（布尔值）

##### `api/containers.py`
实现了 Flask API 接口：
- GET `/containers/<container_id>`：获取指定集装箱的详细信息

##### `utils/shipping_calculator.py`
提供了航运计算功能：
- `calculate_eta()`：计算预计到港时间，修复了夏令时问题
- `get_voyage_duration_in_days()`：模拟获取航行天数

### 5. 扩展项目

#### 5.1 添加新的 API 接口
在 `api/containers.py` 中添加新的路由和处理函数：

```python
@app.route('/containers', methods=['POST'])
def create_container():
    # 实现创建集装箱的逻辑
    pass
```

#### 5.2 扩展 Container 类
在 `models/container.py` 中添加新的属性和方法：

```python
class Container:
    def __init__(self, container_id, weight, port_of_origin, destination_port=None):
        # 现有属性...
        self.destination_port = destination_port
        self.is_dangerous_goods = False
    
    def mark_as_dangerous(self):
        """标记为危险品"""
        self.is_dangerous_goods = True
```

### 6. 注意事项

1. 本项目使用 Flask 开发服务器，仅用于开发和测试环境
2. 在生产环境中，建议使用 Gunicorn 或 uWSGI 等 WSGI 服务器
3. 时区处理使用 `pytz` 库，确保正确设置各端口的时区信息
4. 危险品标识默认为 `False`，可通过代码修改为 `True`

### 7. Git 工作流回顾

项目演示了完整的 Git 工作流：
1. 使用 `feature/` 分支开发新功能
2. 使用 `hotfix/` 分支修复紧急 bug
3. 使用 `rebase` 操作同步代码
4. 遵循了约定式提交规范

这个项目可以作为 Git 教学案例，展示了团队协作中的分支管理和代码合并流程。