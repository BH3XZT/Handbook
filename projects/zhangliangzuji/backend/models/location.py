from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db

class Location(db.Model):
    """Location model to store visited places"""
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    province = db.Column(db.String(100))  # 省份
    city = db.Column(db.String(100))      # 城市
    district = db.Column(db.String(100))  # 区县
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    coordinate_type = db.Column(db.String(20), default='gps')  # gps, amap, baidu
    visited_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    source = db.Column(db.String(50))  # 数据来源: manual, gpx, csv, geojson等
    description = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'province': self.province,
            'city': self.city,
            'district': self.district,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'coordinate_type': self.coordinate_type,
            'visited_date': self.visited_date.isoformat() if self.visited_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'source': self.source,
            'description': self.description
        }
    
    def __repr__(self):
        return f'<Location {self.name} ({self.province}/{self.city}/{self.district})>'