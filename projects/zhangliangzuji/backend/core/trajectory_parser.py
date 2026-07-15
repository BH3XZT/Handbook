"""
轨迹格式解析模块
支持: GPX, GeoJSON, CSV, JSON
"""

import json
import csv
import io

class TrajectoryParser:
    """轨迹数据解析器"""
    
    @staticmethod
    def parse_gpx(content):
        """解析GPX文件"""
        try:
            import gpxpy
            gpx = gpxpy.parse(content)
            points = []
            
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        points.append({
                            'lat': point.latitude,
                            'lng': point.longitude,
                            'name': f"GPX Point {len(points)+1}",
                            'type': 'gps',
                            'time': point.time.isoformat() if point.time else None,
                            'elevation': point.elevation
                        })
            
            for waypoint in gpx.waypoints:
                points.append({
                    'lat': waypoint.latitude,
                    'lng': waypoint.longitude,
                    'name': waypoint.name or f"GPX Waypoint {len(points)+1}",
                    'type': 'gps',
                    'time': waypoint.time.isoformat() if waypoint.time else None,
                    'elevation': waypoint.elevation
                })
            
            return points
        except Exception as e:
            raise ValueError(f"GPX解析错误: {str(e)}")
    
    @staticmethod
    def parse_geojson(content):
        """解析GeoJSON文件"""
        try:
            if isinstance(content, str):
                data = json.loads(content)
            else:
                data = content
            
            points = []
            
            if data.get('type') == 'FeatureCollection':
                for feature in data.get('features', []):
                    point = TrajectoryParser._extract_point_from_feature(feature)
                    if point:
                        points.append(point)
            elif data.get('type') == 'Feature':
                point = TrajectoryParser._extract_point_from_feature(data)
                if point:
                    points.append(point)
            
            return points
        except Exception as e:
            raise ValueError(f"GeoJSON解析错误: {str(e)}")
    
    @staticmethod
    def parse_csv(content):
        """解析CSV文件"""
        try:
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            
            points = []
            csv_reader = csv.DictReader(io.StringIO(content))
            
            for row in csv_reader:
                lat = float(row.get('lat') or row.get('latitude') or 0)
                lng = float(row.get('lng') or row.get('longitude') or 0)
                
                if lat == 0 and lng == 0:
                    continue
                
                points.append({
                    'name': row.get('name', f"CSV Point {len(points)+1}"),
                    'lat': lat,
                    'lng': lng,
                    'type': row.get('type', 'gps'),
                    'date': row.get('date') or row.get('time'),
                    'description': row.get('description', '')
                })
            
            return points
        except Exception as e:
            raise ValueError(f"CSV解析错误: {str(e)}")
    
    @staticmethod
    def parse_json(content):
        """解析JSON格式轨迹数据"""
        try:
            if isinstance(content, str):
                data = json.loads(content)
            else:
                data = content
            
            points = []
            
            if isinstance(data, list):
                for item in data:
                    point = TrajectoryParser._normalize_point(item)
                    if point:
                        points.append(point)
            elif isinstance(data, dict):
                if 'points' in data:
                    for item in data.get('points', []):
                        point = TrajectoryParser._normalize_point(item)
                        if point:
                            points.append(point)
                else:
                    point = TrajectoryParser._normalize_point(data)
                    if point:
                        points.append(point)
            
            return points
        except Exception as e:
            raise ValueError(f"JSON解析错误: {str(e)}")
    
    @staticmethod
    def _normalize_point(item):
        """标准化点数据"""
        try:
            lat = float(item.get('lat') or item.get('latitude') or item.get('y') or 0)
            lng = float(item.get('lng') or item.get('longitude') or item.get('x') or 0)
            
            if lat == 0 and lng == 0:
                return None
            
            return {
                'name': item.get('name', 'Point'),
                'lat': lat,
                'lng': lng,
                'type': item.get('type', item.get('coordinate_type', 'gps')),
                'date': item.get('date') or item.get('time') or item.get('visited_date'),
                'description': item.get('description', ''),
                'province': item.get('province'),
                'city': item.get('city'),
                'district': item.get('district')
            }
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def parse(content, file_format):
        """通用解析方法"""
        file_format = file_format.lower().strip('.')
        
        if file_format == 'gpx':
            return TrajectoryParser.parse_gpx(content)
        elif file_format == 'geojson':
            return TrajectoryParser.parse_geojson(content)
        elif file_format == 'csv':
            return TrajectoryParser.parse_csv(content)
        elif file_format == 'json':
            return TrajectoryParser.parse_json(content)
        else:
            raise ValueError(f"不支持的文件格式: {file_format}")
    
    @staticmethod
    def _extract_point_from_feature(feature):
        """从GeoJSON Feature提取点"""
        try:
            geometry = feature.get('geometry', {})
            properties = feature.get('properties', {})
            
            if geometry.get('type') == 'Point':
                coords = geometry.get('coordinates', [])
                if len(coords) >= 2:
                    return {
                        'lat': coords[1],
                        'lng': coords[0],
                        'name': properties.get('name', 'GeoJSON Point'),
                        'type': properties.get('type', 'gps'),
                        'description': properties.get('description', '')
                    }
        except Exception:
            pass
        
        return None