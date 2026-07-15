from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(basedir, '..', 'data')
os.makedirs(data_dir, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(data_dir, "zhangliangzuji.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Initialize database
db = SQLAlchemy(app)

# Import models
from models.location import Location
from models.achievement import Achievement, UserAchievement

# Import blueprints
from apis.location_api import location_bp
from apis.achievement_api import achievement_bp
from apis.upload_api import upload_bp

# Register blueprints
app.register_blueprint(location_bp, url_prefix='/api')
app.register_blueprint(achievement_bp, url_prefix='/api')
app.register_blueprint(upload_bp, url_prefix='/api')

# Create tables
with app.app_context():
    db.create_all()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'zhangliangzuji-backend'
    }), 200

@app.route('/api/info', methods=['GET'])
def app_info():
    """Application information"""
    return jsonify({
        'name': '丈量足迹',
        'version': '1.0.0',
        'description': '记录去过的省市区，解锁成就',
        'features': [
            'GPS坐标支持',
            '高德地图坐标支持',
            '百度地图坐标支持',
            'GPX轨迹导入',
            'GeoJSON导入',
            'CSV批量导入',
            '省市区统计',
            '成就系统'
        ]
    }), 200

if __name__ == '__main__':
    print("🚀 Starting 丈量足迹 Backend...")
    print(f"📊 Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.run(host='0.0.0.0', port=5000, debug=False)