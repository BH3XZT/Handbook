"""
成就系统
管理成就的定义、检查和解锁
"""

class AchievementSystem:
    """成就系统"""
    
    ACHIEVEMENTS = {
        'first_step': {
            'code': 'first_step',
            'name': '初出茅庐',
            'description': '去过5个省份',
            'icon': '🌟',
            'difficulty': 1,
            'category': 'province',
            'condition_type': 'province_count',
            'condition_value': 5
        },
        'china_wanderer': {
            'code': 'china_wanderer',
            'name': '中国漫游者',
            'description': '去过20个省份',
            'icon': '🚀',
            'difficulty': 2,
            'category': 'province',
            'condition_type': 'province_count',
            'condition_value': 20
        },
        'continent_explorer': {
            'code': 'continent_explorer',
            'name': '大陆行者',
            'description': '去过31个省份（全覆盖）',
            'icon': '👑',
            'difficulty': 3,
            'category': 'province',
            'condition_type': 'province_count',
            'condition_value': 31
        },
        'city_explorer': {
            'code': 'city_explorer',
            'name': '城市探险家',
            'description': '去过50个城市',
            'icon': '🏙️',
            'difficulty': 2,
            'category': 'city',
            'condition_type': 'city_count',
            'condition_value': 50
        },
        'district_collector': {
            'code': 'district_collector',
            'name': '区县收藏家',
            'description': '去过100个区县',
            'icon': '🎯',
            'difficulty': 2,
            'category': 'district',
            'condition_type': 'district_count',
            'condition_value': 100
        },
    }
    
    REGIONS = {
        'east': ['上海', '江苏', '浙江', '安徽', '福建', '江西', '山东'],
        'central': ['河南', '湖北', '湖南', '广西', '四川', '贵州', '云南'],
        'north': ['北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江'],
        'south': ['广东', '海南'],
        'west': ['陕西', '甘肃', '青海', '宁夏', '新疆', '西藏']
    }
    
    @staticmethod
    def get_all_achievements():
        """获取所有成就定义"""
        return AchievementSystem.ACHIEVEMENTS
    
    @staticmethod
    def check_achievements(locations_data):
        """检查可解锁的成就"""
        unlocked = []
        
        province_count = len(locations_data.get('provinces', []))
        city_count = len(locations_data.get('cities', []))
        district_count = len(locations_data.get('districts', []))
        
        if province_count >= 5:
            unlocked.append('first_step')
        if province_count >= 20:
            unlocked.append('china_wanderer')
        if province_count >= 31:
            unlocked.append('continent_explorer')
        if city_count >= 50:
            unlocked.append('city_explorer')
        if district_count >= 100:
            unlocked.append('district_collector')
        
        return unlocked