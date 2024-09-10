from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import re
import logging
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}}, supports_credentials=True)

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

# 添加饮食记录
@app.route('/add_food_log', methods=['POST'])
def add_food_log():
    try:
        data = request.get_json()
        
        # 验证必要的字段是否存在
        required_fields = ['user_id', 'date', 'meal', 'food_item', 'calories', 'protein', 'carbs', 'fats']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'缺少必要字段: {field}'}), 400

        # 验证用户是否存在
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'message': '用户不存在'}), 404

        # 创建食物日志记录
        food_log = FoodLog(
            user_id=data['user_id'],
            date=data['date'],  # 保存日期信息
            meal=data['meal'],
            food_item=data['food_item'],
            calories=float(data['calories']),
            protein=float(data['protein']),
            carbs=float(data['carbs']),
            fats=float(data['fats'])
        )

        # 添加到数据库
        db.session.add(food_log)
        db.session.commit()

        return jsonify({'message': '饮食记录已添加', 'food_log_id': food_log.id}), 201

    except ValueError as ve:
        logger.error(f"Invalid data format: {ve}")
        return jsonify({'message': '数据格式无效，请确保所有数值字段为数字'}), 400

    except SQLAlchemyError as e:
        logger.error(f"Database error while adding food log: {e}")
        db.session.rollback()
        return jsonify({'message': '数据库错误，添加饮食记录失败'}), 500

    except Exception as e:
        logger.error(f"Unexpected error adding food log: {e}")
        db.session.rollback()
        return jsonify({'message': '添加饮食记录失败，请重试'}), 500

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
            'fats': log.fats
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


# 计算摄入和BMI
@app.route('/user_intake/<int:user_id>', methods=['GET'])
def get_user_intake(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': '用户未找到'}), 404

    # 计算基础代谢率 (BMR)————假设年龄为25
    if user.gender == 'male':
        bmr = 88.362 + (13.397 * user.weight) + (4.799 * user.height) - (5.677 * 25)  
    else:
        bmr = 447.593 + (9.247 * user.weight) + (3.098 * user.height) - (4.330 * 25)  

    # 根据用户劳动强度调整 BMR
    if user.labor_intensity == 'brain-domain':
        bmr *= 1.2
    elif user.labor_intensity == 'labor-domain':
        bmr *= 1.75
    else:
        bmr *= 1.55

    # 计算总卡路里摄入
    total_calories_consumed = sum(
        [log.calories for log in FoodLog.query.filter_by(user_id=user_id).all()]
    )

    # 应摄入卡路里
    target_calories = bmr

    # 计算BMI
    height_meters = user.height / 100  # height 以厘米为单位
    bmi = user.weight / (height_meters ** 2)
    current_weight = user.weight / 1

    return jsonify({
        'target_calories': round(target_calories, 2),
        'bmi': round(bmi, 2),
        'weight': round(current_weight, 1)
    }), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
