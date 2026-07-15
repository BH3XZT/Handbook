"""
坐标系转换模块
支持: GPS (WGS84), 高德地图 (GCJ02), 百度地图 (BD09)
"""

import math

class CoordinateConverter:
    """坐标系转换器"""
    
    @staticmethod
    def gps2gcj(lat, lng):
        """GPS (WGS84) -> 高德坐标 (GCJ02)"""
        if CoordinateConverter._out_of_china(lat, lng):
            return [lat, lng]
        
        dLat = CoordinateConverter._transformLat(lng - 105.0, lat - 35.0)
        dLng = CoordinateConverter._transformLng(lng - 105.0, lat - 35.0)
        radLat = lat / 180.0 * math.pi
        magic = math.sin(radLat)
        magic = 1 - 0.00669342162296594323 * magic * magic
        sqrtMagic = math.sqrt(magic)
        
        dLat = (dLat * 180.0) / ((6370996.81 * (1 - 0.00669342162296594323)) / (magic * sqrtMagic) * math.pi)
        dLng = (dLng * 180.0) / (6370996.81 / sqrtMagic * math.cos(radLat) * math.pi)
        
        mgLat = lat + dLat
        mgLng = lng + dLng
        
        return [mgLat, mgLng]
    
    @staticmethod
    def gcj2gps(lat, lng):
        """高德坐标 (GCJ02) -> GPS (WGS84)"""
        dLat = CoordinateConverter._transformLat(lng - 105.0, lat - 35.0)
        dLng = CoordinateConverter._transformLng(lng - 105.0, lat - 35.0)
        radLat = lat / 180.0 * math.pi
        magic = math.sin(radLat)
        magic = 1 - 0.00669342162296594323 * magic * magic
        sqrtMagic = math.sqrt(magic)
        
        dLat = (dLat * 180.0) / ((6370996.81 * (1 - 0.00669342162296594323)) / (magic * sqrtMagic) * math.pi)
        dLng = (dLng * 180.0) / (6370996.81 / sqrtMagic * math.cos(radLat) * math.pi)
        
        mgLat = lat - dLat
        mgLng = lng - dLng
        
        return [mgLat, mgLng]
    
    @staticmethod
    def gcj2baidu(lat, lng):
        """高德坐标 (GCJ02) -> 百度坐标 (BD09)"""
        z = math.sqrt(lng * lng + lat * lat) + 0.00002419343265649148
        theta = math.atan2(lat, lng) + 0.000003123951936305873
        bdLng = z * math.cos(theta) + 0.0065
        bdLat = z * math.sin(theta) + 0.006
        
        return [bdLat, bdLng]
    
    @staticmethod
    def baidu2gcj(lat, lng):
        """百度坐标 (BD09) -> 高德坐标 (GCJ02)"""
        x = lng - 0.0065
        y = lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002419343265649148
        theta = math.atan2(y, x) - 0.000003123951936305873
        gcjLng = z * math.cos(theta)
        gcjLat = z * math.sin(theta)
        
        return [gcjLat, gcjLng]
    
    @staticmethod
    def gps2baidu(lat, lng):
        """GPS (WGS84) -> 百度坐标 (BD09)"""
        gcj = CoordinateConverter.gps2gcj(lat, lng)
        return CoordinateConverter.gcj2baidu(gcj[0], gcj[1])
    
    @staticmethod
    def baidu2gps(lat, lng):
        """百度坐标 (BD09) -> GPS (WGS84)"""
        gcj = CoordinateConverter.baidu2gcj(lat, lng)
        return CoordinateConverter.gcj2gps(gcj[0], gcj[1])
    
    @staticmethod
    def _transformLat(x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
        return ret
    
    @staticmethod
    def _transformLng(x, y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
        return ret
    
    @staticmethod
    def _out_of_china(lat, lng):
        """判断是否在中国边界外"""
        if lng < 73.66 or lng > 135.05 or lat < 3.86 or lat > 53.55:
            return True
        return False
    
    @staticmethod
    def convert(lat, lng, from_type='gps', to_type='gps'):
        """通用坐标转换"""
        if from_type == to_type:
            return [lat, lng]
        
        # 统一转换到GPS
        if from_type == 'amap':
            lat, lng = CoordinateConverter.gcj2gps(lat, lng)
        elif from_type == 'baidu':
            lat, lng = CoordinateConverter.baidu2gps(lat, lng)
        
        # 从GPS转换到目标
        if to_type == 'gps':
            return [lat, lng]
        elif to_type == 'amap':
            return CoordinateConverter.gps2gcj(lat, lng)
        elif to_type == 'baidu':
            return CoordinateConverter.gps2baidu(lat, lng)
        
        return [lat, lng]