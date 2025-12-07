### 实际场景案例

#### 场景设定

*   **公司**：东方海外货柜航运有限公司
*   **项目**：`oocl-cargo-tracking`，一个内部的集装箱追踪与管理系统。
*   **团队角色**：
    *   **David (Team Leader)**：资深工程师，负责项目架构、代码审查和合并主分支。
    *   **Chen (Developer 1)**：后端开发人员。
    *   **Fiona (Developer 2)**：后端开发人员。
*   **远程仓库**：托管在 GitHub 上，`main` 分支受保护。
*   **当前状态**：项目已初始化，正在开发核心功能。

> **注意**：这是一个教学案例，用于演示 Git 工作流和团队协作开发。请不要在当前项目中实际执行这些操作，因为该项目将留作后续学员练习使用。

#### 第一幕：新功能开发 - 为集装箱添加“危险品”标识

**任务**：Chen 接到一个新任务，需要在系统中为集装箱增加一个“是否为危险品”的标识，以便在运输和堆存时进行特殊处理。

##### 步骤 1：Chen 准备开发环境

Chen 的电脑上已经有项目代码了。他首先确保自己的本地代码是最新的。

```bash
# 进入项目目录
cd oocl-cargo-tracking
# 切换到 main 分支
git checkout main
# 从远程仓库拉取最新的代码
git pull origin main
```

##### 步骤 2：Chen 创建功能分支

```bash
# 创建一个描述清晰的功能分支
git checkout -b feature/add-dangerous-goods-flag
```

##### 步骤 3：Chen 开发与提交

Chen 修改了集装箱的数据模型和 API。

**文件 `models/container.py` 的创建与实现：**

```python
class Container:
    def __init__(self, container_id, weight, port_of_origin):
        self.container_id = container_id
        self.weight = weight
        self.port_of_origin = port_of_origin
        # 新增属性：是否为危险品，默认为False
        self.is_dangerous_goods = False
```

**文件 `api/containers.py` 的创建与实现：**

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

**文件 `requirements.txt` 的创建：**

```
flask
pytz
```

Chen 对修改满意后，进行本地提交。

```bash
# 查看状态
git status
# 添加所有修改的文件
git add models/container.py api/containers.py requirements.txt
# 提交，使用约定式提交信息
git commit -m "feat(container): add dangerous goods flag to model and API"
```

##### 步骤 4：Chen 推送并创建 Pull Request (PR)

```bash
# 将功能分支推送到远程仓库
git push origin feature/add-dangerous-goods-flag
```

然后，Chen 在 GitHub 上创建一个 PR：

*   **标题**: `feat(container): add dangerous goods flag to model and API`
*   **描述**: "根据 IMO 规定，为集装箱对象增加 `is_dangerous_goods` 布尔字段。同时更新了 GET API，以便前端和物流系统能够识别危险品并进行相应处理。关联任务 #TICKET-123。"
*   **审查者**: 他指定了 `@David` 作为审查者。

##### 步骤 5：David 进行代码审查

David 收到通知，开始审查 Chen 的 PR。

1.  **CI 检查**：David 看到 CI 流程已通过（代码风格检查、单元测试通过）。
2.  **代码审查**：David 查看代码变更，认为实现逻辑清晰，符合项目规范。
3.  **提出建议**：David 在 PR 中评论：“Chen, 代码很好。请在 `api/containers.py` 的注释中补充一下 `is_dangerous_goods` 字段的说明，例如 `True` 代表什么，`False` 代表什么，方便其他 API 使用者理解。”
4.  **Chen 修改代码**：Chen 收到通知，按照 David 的建议添加了注释，再次 `git commit` 和 `git push`。
5.  **批准与合并**：David 看到修改后，满意地点击 "Approve"，然后点击 "Merge pull request" (使用 Squash and merge)，将代码合并到 `main` 分支。

#### 第二幕：紧急 Bug 修复 - 航线信息显示错误

**任务**：就在 Chen 开发功能的同时，运营部门报告了一个紧急 Bug：系统显示的某个航线的预计到港时间（ETA）比实际晚了整整一天！

##### 步骤 1：David 分配任务

David 立即将这个高优先级的 Bug 分配给 Fiona，并告诉她这是一个需要紧急修复的问题。

##### 步骤 2：Fiona 快速响应

Fiona 立即放下手中的工作，开始修复 Bug。

```bash
# 确保本地 main 是最新的
git checkout main
git pull origin main
# 创建一个紧急修复分支
git checkout -b hotfix/fix-eta-calculation-bug
```

##### 步骤 3：Fiona 定位并修复 Bug

Fiona 发现，在计算跨时区的航线 ETA 时，代码没有正确处理夏令时，导致时间计算错误。

**文件 `utils/shipping_calculator.py` 的创建与实现：**

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

Fiona 快速测试了一下，确认修复有效。

##### 步骤 4：Fiona 提交并创建 PR

```bash
# 添加修改的文件
git add utils/shipping_calculator.py
# 提交，使用约定式提交信息
git commit -m "fix(shipping): correct ETA calculation to handle daylight saving time"
# 将热修复分支推送到远程仓库
git push origin hotfix/fix-eta-calculation-bug
```

Fiona 创建了一个 PR，标题为 `fix(shipping): correct ETA calculation to handle daylight saving time`。在描述中，她简要说明了 Bug 的原因和修复方案，并标记了 `@David` 和 `urgent` 标签。

##### 步骤 5：David 紧急处理

*   **快速审查**：David 看到 `urgent` 标签，立即审查。Fiona 的代码修改清晰，测试充分。
*   **立即合并**：David 直接批准并合并了这个 PR。
*   **部署**：由于是紧急修复，合并后，David 立即触发了针对 `main` 分支的自动化部署流程，将修复上线。

#### 第三幕：同步与继续开发

现在，Chen 的功能分支 `feature/add-dangerous-goods-flag` 已经落后于 `main` 分支了（因为 Fiona 的 hotfix 已经被合并了）。如果 Chen 还想继续在他的分支上工作，他需要同步最新的代码。

```bash
# 切换到 Chen 的功能分支
git checkout feature/add-dangerous-goods-flag
# 获取远程的最新更新
git fetch origin
# 将 main 分支的最新修改合并到自己的功能分支
git rebase origin/main
```

`rebase` 操作会将 Chen 的提交“移动”到 `main` 分支的最新提交之后，确保他的工作是基于最新的代码库。这样，当他下次创建 PR 时，冲突的可能性会大大降低。

#### 第四幕：文档更新

**任务**：项目开发完成后，需要更新文档以便后续开发者使用。

##### 步骤 1：更新 README.md

Chen 更新了 `README.md` 文件，添加了完整的项目介绍和使用指南：

```bash
# 切换到 main 分支
git checkout main
# 拉取最新代码
git pull origin main
# 更新 README.md 文件（添加项目介绍、使用指南等）
# ... 编辑 README.md 文件 ...
# 提交文档更新
git add README.md
git commit -m "docs: update README with project introduction and usage guide"
git push origin main
```

#### 总结：这个例子的关键点

1.  **角色分工明确**：Leader 负责 Review 和合并，Dev 负责开发和修复。
2.  **分支策略清晰**：
    *   `feature/` 用于新功能开发。
    *   `hotfix/` 用于紧急修复，流程更快捷。
    *   `main` 分支始终保持稳定和可部署状态。
3.  **PR 是协作核心**：所有代码变更都通过 PR，实现了代码审查、自动化检查和知识共享。
4.  **业务场景驱动**：代码修改（危险品、ETA 计算）都与 OOCL 的核心业务紧密相关，让例子更具真实感。
5.  **处理了并行开发**：展示了当一个分支（hotfix）被合并后，如何同步其他正在开发中的分支（feature），这是团队协作中非常常见且重要的一步。
6.  **文档重要性**：项目开发完成后，及时更新文档以便后续开发者使用。