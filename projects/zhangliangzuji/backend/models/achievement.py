from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db

class Achievement(db.Model):
    """Achievement definition model"""
    __tablename__ = 'achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)  # 唯一代码
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # emoji或图标名
    difficulty = db.Column(db.Integer, default=1)  # 难度 1-5
    category = db.Column(db.String(50))  # 成就类别: province, city, region等
    condition_type = db.Column(db.String(50))  # 条件类型
    condition_value = db.Column(db.Integer)  # 条件值
    hidden = db.Column(db.Boolean, default=False)  # 是否隐藏
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'difficulty': self.difficulty,
            'category': self.category,
            'condition_type': self.condition_type,
            'condition_value': self.condition_value,
            'hidden': self.hidden
        }
    
    def __repr__(self):
        return f'<Achievement {self.name}>'


class UserAchievement(db.Model):
    """User achievement unlocked record"""
    __tablename__ = 'user_achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=False)
    user_id = db.Column(db.String(100), default='default_user')
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    achievement = db.relationship('Achievement', backref='user_achievements')
    
    def to_dict(self):
        return {
            'id': self.id,
            'achievement': self.achievement.to_dict() if self.achievement else None,
            'user_id': self.user_id,
            'unlocked_at': self.unlocked_at.isoformat(),
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<UserAchievement user={self.user_id} achievement={self.achievement_id}>'