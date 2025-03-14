from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import re
import logging
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True)
# CORS(app)  # 允许所有请求跨域

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5174"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response

# 配置 MySQL 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://nutrition_user:179100@localhost/nutrition_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 日志设置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    labor_intensity = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 食物日志模型
class FoodLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False) 
    meal = db.Column(db.String(50), nullable=False)
    food_item = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)
    fiber = db.Column(db.Float, nullable=False)
    
# 健康日志模型
class HealthLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    mood = db.Column(db.String(50), nullable=True)
    sleep_start = db.Column(db.Time, nullable=True)
    sleep_end = db.Column(db.Time, nullable=True)
    sleep_hours = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)

# 初始化数据库
with app.app_context():
    db.create_all()

# 添加根URL路由
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': '欢迎来到营养推荐系统API'}), 200

# 用户注册
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    gender = data.get('gender')
    weight = data.get('weight')
    height = data.get('height')
    laborIntensity = data.get('laborIntensity')

    # 注册逻辑
    try:
        # 验证用户名是否为英文
        if not re.match("^[A-Za-z0-9_]*$", username):
            return jsonify({'message': '用户名应为英文字符'}), 400

        # 验证密码是否为数字和字母混合
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
            return jsonify({'message': '密码应为至少8位，且包含数字和字母'}), 400

        # 验证邮箱格式
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({'message': '请输入有效的邮箱地址'}), 400

        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first() is not None:
            return jsonify({'message': '用户名已存在'}), 400

        # 检查邮箱是否已存在
        if User.query.filter_by(email=email).first() is not None:
            return jsonify({'message': '邮箱已被注册'}), 400

        user = User(
            username=username,
            email=email,
            name=name,
            gender=gender,
            weight=weight,
            height=height,
            labor_intensity=laborIntensity
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return jsonify({'message': '注册成功'}), 201
    except Exception as e:
        logger.error(f"Error during registration: {e}")  # 打印错误信息
        db.session.rollback()
        return jsonify({'message': '注册失败，请重试。'}), 500

# 用户登录
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            return jsonify({'message': '用户名或密码错误'}), 401

        return jsonify({'user_id': user.id}), 200
    except Exception as e:
        logger.error(f"Error during login: {e}")  # 打印详细错误信息
        return jsonify({'message': '服务器错误，请重试。'}), 500

# 获取用户信息  
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': '用户未找到'}), 404
        
    return jsonify({
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'gender': user.gender,
        'weight': user.weight,
        'height': user.height,
        'labor_intensity': user.labor_intensity
    }), 200
    
# 添加饮食记录
@app.route('/add_food_log', methods=['POST'])
def add_food_log():
    try:
        data = request.get_json()
        logger.info(f"Received food log data: {data}")  # 添加日志记录
        
        # 验证必要的字段是否存在
        required_fields = ['user_id', 'date', 'meal', 'food_item', 'calories', 'protein', 'carbs', 'fats', 'fiber']
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")  # 添加错误日志
                return jsonify({'message': f'缺少必要字段: {field}'}), 400

        # 创建食物日志记录
        food_log = FoodLog(
            user_id=data['user_id'],
            date=data['date'],
            meal=data['meal'],
            food_item=data['food_item'],
            calories=float(data['calories']),
            protein=float(data['protein']),
            carbs=float(data['carbs']),
            fats=float(data['fats']),
            fiber=float(data['fiber'])
        )

        db.session.add(food_log)
        db.session.commit()
        logger.info("Food log added successfully")  # 添加成功日志

        return jsonify({
            'status': 'success',
            'message': '饮食记录已添加',
            'food_log': {
                'id': food_log.id,
                'meal': food_log.meal,
                'food_item': food_log.food_item,
                'calories': food_log.calories,
                'protein': food_log.protein,
                'carbs': food_log.carbs,
                'fats': food_log.fats,
                'fiber': food_log.fiber
            }
        }), 201

    except Exception as e:
        logger.error(f"Error adding food log: {str(e)}")  # 添加错误日志
        db.session.rollback()
        return jsonify({'message': f'添加饮食记录失败: {str(e)}'}), 500

# 查询饮食记录
@app.route('/query_food_log', methods=['GET'])
def query_food_log():
    try:
        user_id = request.args.get('user_id')
        date = request.args.get('date')

        # 验证用户是否存在
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': '用户不存在'}), 404

        # 查询用户指定日期的食物日志
        food_logs = FoodLog.query.filter_by(user_id=user_id, date=date).all()

        # 将食物日志转换为 JSON 格式
        food_logs_data = [{
            'id': log.id,
            'meal': log.meal,
            'food_item': log.food_item,
            'calories': log.calories,
            'protein': log.protein,
            'carbs': log.carbs,
            'fats': log.fats,
            'fiber': log.fiber
        } for log in food_logs]

        return jsonify({'food_logs': food_logs_data}), 200

    except SQLAlchemyError as e:
        logger.error(f"Database error while querying food log: {e}")
        return jsonify({'message': '数据库错误，查询饮食记录失败'}), 500

    except Exception as e:
        logger.error(f"Unexpected error querying food log: {e}")
        return jsonify({'message': '查询饮食记录失败，请重试'}), 500

# 删除饮食记录
@app.route('/delete_food_log/<int:log_id>', methods=['DELETE'])
def delete_food_log(log_id):
    try:
        food_log = FoodLog.query.get(log_id)

        # 验证食物日志是否存在
        if not food_log:
            return jsonify({'message': '饮食记录未找到'}), 404

        # 从数据库中删除食物日志
        db.session.delete(food_log)
        db.session.commit()

        return jsonify({'message': '饮食记录已删除'}), 200

    except SQLAlchemyError as e:
        logger.error(f"Database error while deleting food log: {e}")
        db.session.rollback()
        return jsonify({'message': '数据库错误，删除饮食记录失败'}), 500

    except Exception as e:
        logger.error(f"Unexpected error deleting food log: {e}")
        db.session.rollback()
        return jsonify({'message': '删除饮食记录失败，请重试'}), 500

# 更新用户信息
@app.route('/update_user_info/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': '用户未找到'}), 404

        data = request.get_json()
        user.name = data.get('name', user.name)
        user.gender = data.get('gender', user.gender)
        user.weight = data.get('weight', user.weight)
        user.height = data.get('height', user.height)
        user.labor_intensity = data.get('laborIntensity', user.labor_intensity)
        logger.info('Received data: %s', data)

        db.session.commit()
        return jsonify({'message': '用户信息更新成功'}), 200

    except SQLAlchemyError as e:
        logger.error(f"Database error while updating user: {e}")
        db.session.rollback()
        return jsonify({'message': '数据库错误，用户信息更新失败'}), 500

    except Exception as e:
        logger.error(f"Unexpected error updating user: {e}")
        db.session.rollback()
        return jsonify({'message': '用户信息更新失败，请重试'}), 500


@app.route('/user_intake/<int:user_id>', methods=['GET'])
def get_user_intake(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': '用户未找到'}), 404

        # 获取今天的日期
        today = datetime.now().date()
        
        # 计算基础代谢率 (BMR)
        height_meters = user.height / 100  # 转换为米
        if user.gender == 'male':
            bmr = 88.362 + (13.397 * user.weight) + (4.799 * user.height) - (5.677 * 25)
        else:
            bmr = 447.593 + (9.247 * user.weight) + (3.098 * user.height) - (4.330 * 25)

        # 根据劳动强度调整BMR
        activity_factors = {
            'brain-domain': 1.2,  # 脑力劳动
            'labor-domain': 1.75, # 体力劳动
            'normal': 1.55        # 普通活动
        }
        activity_factor = activity_factors.get(user.labor_intensity, 1.55)
        target_calories = bmr * activity_factor

        # 计算今日卡路里摄入
        today_logs = FoodLog.query.filter_by(
            user_id=user_id,
            date=today
        ).all()
        
        consumed_calories = sum(log.calories for log in today_logs)
        logger.info(f"User {user_id} stats: target_calories={target_calories}, consumed_calories={consumed_calories}")

        # 计算BMI
        bmi = user.weight / (height_meters ** 2)

        return jsonify({
            'target_calories': round(target_calories, 2),
            'consumed_calories': round(consumed_calories, 2),
            'bmi': round(bmi, 2),
            'weight': round(user.weight, 1),
            'height': user.height,
            'gender': user.gender,
            'labor_intensity': user.labor_intensity
        }), 200
        
    except Exception as e:
        logger.error(f"Error calculating user intake: {str(e)}")
        return jsonify({'message': f'计算失败: {str(e)}'}), 500

# 添加健康日志
@app.route('/add_health_log', methods=['POST'])
def add_health_log():
    try:
        data = request.get_json()
        logger.info(f"Received health log data: {data}")  # 添加日志
        
        # 验证必要字段
        required_fields = ['user_id', 'date', 'weight']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'缺少必要字段: {field}'}), 400
        
        # 验证用户是否存在
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'message': '用户不存在'}), 404
        
        # 检查是否已有当天记录
        existing_log = HealthLog.query.filter_by(
            user_id=data['user_id'], 
            date=data['date']
        ).first()
        
        try:
            if existing_log:
                # 更新现有记录
                existing_log.weight = float(data['weight'])
                existing_log.mood = data.get('mood')
                existing_log.sleep_start = data.get('sleep_start')
                existing_log.sleep_end = data.get('sleep_end')
                existing_log.sleep_hours = float(data.get('sleep_hours', 0))
                existing_log.notes = data.get('notes')
                health_log_id = existing_log.id
            else:
                # 创建新记录
                health_log = HealthLog(
                    user_id=data['user_id'],
                    date=data['date'],
                    weight=float(data['weight']),
                    mood=data.get('mood'),
                    sleep_start=data.get('sleep_start'),
                    sleep_end=data.get('sleep_end'),
                    sleep_hours=float(data.get('sleep_hours', 0)),
                    notes=data.get('notes')
                )
                db.session.add(health_log)
                health_log_id = health_log.id
            
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '健康日志已保存',
                'health_log_id': health_log_id
            }), 201
            
        except ValueError as ve:
            db.session.rollback()
            return jsonify({'message': f'数据格式无效: {str(ve)}'}), 400
            
    except Exception as e:
        logger.error(f"Error adding health log: {str(e)}")
        db.session.rollback()
        return jsonify({'message': f'添加健康日志失败: {str(e)}'}), 500
    
# 获取健康日志
@app.route('/get_health_log', methods=['GET'])
def get_health_log():
    try:
        user_id = request.args.get('user_id')
        date = request.args.get('date')
        
        if not user_id:
            return jsonify({'message': '缺少用户ID'}), 400
            
        # 验证用户是否存在
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': '用户不存在'}), 404
            
        query = HealthLog.query.filter_by(user_id=user_id)
        
        if date:
            # 获取特定日期的日志
            log = query.filter_by(date=date).first()
            if not log:
                return jsonify({'health_log': None}), 200
                
            log_data = {
                'id': log.id,
                'date': log.date.isoformat(),
                'weight': log.weight,
                'mood': log.mood,
                'sleep_start': log.sleep_start.isoformat() if log.sleep_start else None,
                'sleep_end': log.sleep_end.isoformat() if log.sleep_end else None,
                'sleep_hours': log.sleep_hours,
                'notes': log.notes
            }
            return jsonify({'health_log': log_data}), 200
        else:
            # 获取所有日志
            logs = query.order_by(HealthLog.date.desc()).all()
            logs_data = [{
                'id': log.id,
                'date': log.date.isoformat(),
                'weight': log.weight,
                'mood': log.mood,
                'sleep_start': log.sleep_start.isoformat() if log.sleep_start else None,
                'sleep_end': log.sleep_end.isoformat() if log.sleep_end else None,
                'sleep_hours': log.sleep_hours,
                'notes': log.notes
            } for log in logs]
            return jsonify({'health_logs': logs_data}), 200
            
    except Exception as e:
        return jsonify({'message': f'获取健康日志失败: {str(e)}'}), 500

# 更新饮食记录
@app.route('/update_food_log/<int:log_id>', methods=['PUT'])
def update_food_log(log_id):
    try:
        food_log = FoodLog.query.get(log_id)
        
        # 验证食物日志是否存在
        if not food_log:
            return jsonify({'message': '饮食记录未找到'}), 404
            
        # 获取更新数据
        data = request.get_json()
        
        # 更新字段
        if 'meal' in data:
            food_log.meal = data['meal']
        if 'food_item' in data:
            food_log.food_item = data['food_item']
        if 'calories' in data:
            food_log.calories = float(data['calories'])
        if 'protein' in data:
            food_log.protein = float(data['protein'])
        if 'carbs' in data:
            food_log.carbs = float(data['carbs'])
        if 'fats' in data:
            food_log.fats = float(data['fats'])
        if 'fiber' in data:
            food_log.fiber = float(data['fiber'])
            
        # 保存更新
        db.session.commit()
        
        return jsonify({'message': '饮食记录已更新'}), 200
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'message': f'数据格式无效: {str(e)}'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'更新饮食记录失败: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
