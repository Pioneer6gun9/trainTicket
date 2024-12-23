from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///train.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义数据模型
class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train_no = db.Column(db.String(20), unique=True, nullable=False)
    train_type = db.Column(db.String(10))  # 车次类型：G-高铁，K-快速等
    departure = db.Column(db.String(50), nullable=False)
    arrival = db.Column(db.String(50), nullable=False)
    departure_time = db.Column(db.String(10), nullable=False)
    arrival_time = db.Column(db.String(10), nullable=False)
    duration = db.Column(db.String(20))
    price_yz = db.Column(db.Float)  # 硬座价格
    price_yw = db.Column(db.Float)  # 硬卧价格
    price_rw = db.Column(db.Float)  # 软卧价格
    seats_yz = db.Column(db.Integer)  # 硬座余票
    seats_yw = db.Column(db.Integer)  # 硬卧余票
    seats_rw = db.Column(db.Integer)  # 软卧余票

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(10), unique=True)  # 车站代码
    city = db.Column(db.String(50))
    province = db.Column(db.String(50))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stations', methods=['GET'])
def get_stations():
    stations = Station.query.all()
    return jsonify([{'name': s.name, 'code': s.code} for s in stations])

@app.route('/search', methods=['POST'])
def search():
    departure = request.form.get('departure')
    arrival = request.form.get('arrival')
    date = request.form.get('date')
    
    # 查询数据库获取车次信息
    trains = Train.query.filter_by(
        departure=departure,
        arrival=arrival
    ).all()
    
    return render_template('search_result.html',
                         trains=trains,
                         departure=departure,
                         arrival=arrival,
                         date=date)

@app.route('/api/advanced_search', methods=['POST'])
def advanced_search():
    search_type = request.form.get('type')
    departure = request.form.get('departure')
    arrival = request.form.get('arrival')
    
    if search_type == 'shortest':
        # 查询最短路径
        trains = Train.query.filter_by(
            departure=departure,
            arrival=arrival
        ).order_by(Train.duration).all()
    elif search_type == 'cheapest':
        # 查询最便宜路径
        trains = Train.query.filter_by(
            departure=departure,
            arrival=arrival
        ).order_by(Train.price_yz).all()
    elif search_type == 'transfer':
        # 查询中转站点
        routes = find_transfer_routes(departure, arrival)
        trains = []
        for route in routes:
            trains.append({
                'train_no': f"{route['first_train'].train_no} + {route['second_train'].train_no}",
                'departure': route['first_train'].departure,
                'arrival': route['second_train'].arrival,
                'duration': route['first_train'].duration + route['second_train'].duration
            })
    
    return jsonify({
        "status": "success",
        "data": [{"train_no": t.train_no, 
                 "departure": t.departure,
                 "arrival": t.arrival,
                 "duration": t.duration} for t in trains]
    })

# 在现有代码中添加中转查询逻辑
def find_transfer_routes(departure, arrival):
    """查找中转路线"""
    all_routes = []
    
    # 查找所有可能的中转站
    departure_trains = Train.query.filter_by(departure=departure).all()
    arrival_trains = Train.query.filter_by(arrival=arrival).all()
    
    # 获取所有可能的中转站
    transfer_stations = set()
    for d_train in departure_trains:
        for a_train in arrival_trains:
            if d_train.arrival == a_train.departure:
                transfer_stations.add(d_train.arrival)
    
    # 对每个中转站查路线
    for station in transfer_stations:
        first_leg = Train.query.filter_by(
            departure=departure,
            arrival=station
        ).all()
        
        second_leg = Train.query.filter_by(
            departure=station,
            arrival=arrival
        ).all()
        
        for t1 in first_leg:
            for t2 in second_leg:
                # 检查时间是否合理
                if is_valid_transfer(t1, t2):
                    all_routes.append({
                        'transfer_station': station,
                        'first_train': t1,
                        'second_train': t2
                    })
    
    return all_routes

def is_valid_transfer(train1, train2):
    """检查中转时间是否合理"""
    t1_arrival = datetime.strptime(train1.arrival_time, '%H:%M')
    t2_departure = datetime.strptime(train2.departure_time, '%H:%M')
    
    # 计算中转时间（分钟）
    transfer_time = (t2_departure - t1_arrival).seconds / 60
    
    # 中转时间应该在30分钟到4小时之间
    return 30 <= transfer_time <= 240

@app.route('/api/transfer_search', methods=['POST'])
def transfer_search():
    departure = request.form.get('departure')
    arrival = request.form.get('arrival')
    
    routes = find_transfer_routes(departure, arrival)
    
    return jsonify({
        'status': 'success',
        'data': [{
            'transfer_station': r['transfer_station'],
            'first_train': {
                'train_no': r['first_train'].train_no,
                'departure': r['first_train'].departure,
                'arrival': r['first_train'].arrival,
                'departure_time': r['first_train'].departure_time,
                'arrival_time': r['first_train'].arrival_time
            },
            'second_train': {
                'train_no': r['second_train'].train_no,
                'departure': r['second_train'].departure,
                'arrival': r['second_train'].arrival,
                'departure_time': r['second_train'].departure_time,
                'arrival_time': r['second_train'].arrival_time
            }
        } for r in routes]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001) 