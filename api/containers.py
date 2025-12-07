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