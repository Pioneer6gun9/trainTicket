import sqlite3

# 连接到数据库
conn = sqlite3.connect('train.db')
cursor = conn.cursor()

# 示例火车数据
train_data = [
    ('G1001', '北京', '上海', '06:00', '12:00', '6:00', 1000, 800, 600, 200, 150, 100),
    ('D2002', '广州', '深圳', '08:00', '10:00', '2:00', 500, 400, 300, 50, 30, 20),
    # 添加更多数据...
]

# 插入数据
cursor.executemany('''
INSERT INTO train (train_no, departure, arrival, departure_time, arrival_time, duration, 
               price_yz, price_yw, price_rw, seats_yz, seats_yw, seats_rw)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', train_data)

# 提交更改并关闭连接
conn.commit()
conn.close()

print("火车数据已更新！") 