# 📍 丈量足迹 - 解锁中国

一个记录你去过的省市区，并自动解锁成就的地理轨迹应用。支持多种坐标和轨迹格式。

## ✨ 功能特点

- 📍 **多格式支持**：GPS坐标、高德/百度地图坐标、GPX轨迹、GeoJSON、CSV批量数据
- 🗺️ **省市区展示**：自动识别并统计去过的省份、城市、区县
- 🏆 **成就系统**：解锁各类成就徽章（如"中国漫游者"、"华东探险家"等）
- 📊 **数据统计**：完整覆盖率展示，省市区详细统计
- 🐳 **Docker部署**：一键启动，无需配置

## 🚀 快速开始

### 前置要求
- Docker & Docker Compose

### 安装与运行

```bash
# 进入项目目录
cd projects/zhangliangzuji

# 启动服务
docker-compose up -d

# 等待容器启动（约30秒）
# 前端访问: http://localhost:3000
# 后端API: http://localhost:5000
```

### 停止服务

```bash
docker-compose down
```

### 查看日志

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 📁 项目结构

```
projects/zhangliangzuji/
├── backend/                    # Python Flask 后端
│   ├── app.py                 # 主应用程序
│   ├── requirements.txt        # Python依赖
│   ├── core/
│   │   ├── coordinate_converter.py    # 坐标转换器(GPS/高德/百度)
│   │   ├── trajectory_parser.py       # 轨迹格式解析
│   │   └── achievement_system.py      # 成就系统
│   ├── apis/
│   │   ├── location_api.py     # 位置管理API
│   │   ├── achievement_api.py   # 成就API
│   │   └── upload_api.py        # 数据上传API
│   ├── models/
│   │   ├── location.py         # 位置模型
│   │   └── achievement.py      # 成就模型
│   └── data/
│
├── frontend/                   # React 前端
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   └── package.json
│
├── data/                       # 数据持久化
├── uploads/                    # 上传文件
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🎯 支持的数据格式

### 单个坐标
```json
{
  "lat": 39.9042,
  "lng": 116.4074,
  "name": "北京",
  "type": "gps"  // 或 "amap", "baidu"
}
```

### GPX轨迹
```xml
<?xml version="1.0"?>
<gpx version="1.1">
  <trk>
    <trkseg>
      <trkpt lat="39.9042" lon="116.4074">...</trkpt>
    </trkseg>
  </trk>
</gpx>
```

### CSV批量导入
```csv
name,lat,lng,type,date
北京,39.9042,116.4074,gps,2024-01-01
上海,31.2304,121.4737,gps,2024-01-02
```

### GeoJSON
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [116.4074, 39.9042]
      },
      "properties": {"name": "北京"}
    }
  ]
}
```

## 🌐 API 端点

- `GET /api/health` - 健康检查
- `GET /api/info` - 应用信息
- `GET /api/locations` - 获取所有地点
- `POST /api/upload` - 上传轨迹文件
- `GET /api/statistics` - 获取统计数据
- `GET /api/achievements` - 获取成就列表

## 🏆 成就系统

| 成就 | 条件 | 难度 |
|------|------|------|
| 🌟 初出茅庐 | 去过5个省 | ⭐ |
| 🚀 中国漫游者 | 去过20个省 | ⭐⭐ |
| 👑 大陆行者 | 去过31个省 | ⭐⭐⭐ |
| 🏙️ 城市探险家 | 去过50个城市 | ⭐⭐ |
| 🎯 区县收藏家 | 去过100个区县 | ⭐⭐⭐ |

## 📊 坐标系支持

- ✅ GPS (WGS84)
- ✅ 高德地图 (GCJ02)
- ✅ 百度地图 (BD09)

系统会自动转换所有坐标到标准GPS格式进行处理。

## 🛠️ 开发

### 本地开发（无Docker）

**后端**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**前端**
```bash
cd frontend
npm install
npm start
```

## 📝 许可证

MIT License

---

**🎉 开始记录你的足迹，解锁属于你的中国吧！**