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