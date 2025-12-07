class Container:
    def __init__(self, container_id, weight, port_of_origin):
        self.container_id = container_id
        self.weight = weight
        self.port_of_origin = port_of_origin
        # 新增属性：是否为危险品，默认为False
        self.is_dangerous_goods = False