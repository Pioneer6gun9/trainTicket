from app import db, Train, Station

# 创建所有表
db.create_all()

# 清空现有数据
Train.query.delete()
Station.query.delete()
db.session.commit()

# 添加测试站点数据
stations = [
    Station(name='上海', code='SHH', city='上海', province='上海'),
    Station(name='杭州', code='HGH', city='杭州', province='浙江'),
    Station(name='南京', code='NJH', city='南京', province='江苏'),
    Station(name='苏州', code='SZH', city='苏州', province='江苏')
]

# 添加测试车次数据
trains = [
    Train(
        train_no='K1805',
        train_type='K',
        departure='上海',
        arrival='杭州',
        departure_time='04:22',
        arrival_time='06:07',
        duration='1小时45分',
        price_yz=55.5,
        price_yw=120.0,
        price_rw=180.0,
        seats_yz=20,
        seats_yw=5,
        seats_rw=3
    ),
    Train(
        train_no='K1511',
        train_type='K',
        departure='上海',
        arrival='杭州',
        departure_time='04:56',
        arrival_time='07:23',
        duration='2小时27分',
        price_yz=55.5,
        price_yw=120.0,
        price_rw=180.0,
        seats_yz=14,
        seats_yw=2,
        seats_rw=0
    )
]

# 添加数据到数据库
try:
    db.session.add_all(stations)
    db.session.add_all(trains)
    db.session.commit()
    print("数据库���始化成功！")
except Exception as e:
    print(f"初始化数据库时出错：{e}")
    db.session.rollback() 