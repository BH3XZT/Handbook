# 丈量足迹 - 快速开始指南

## 📦 使用 Docker 启动

### 前置要求
- Docker 和 Docker Compose

### 一键启动

```bash
# 进入项目目录
cd projects/zhangliangzuji

# 启动所有服务
docker-compose up -d

# 检查服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 访问应用
- **前端**: http://localhost:3000
- **后端API**: http://localhost:5000
- **健康检查**: http://localhost:5000/api/health

### 停止服务
```bash
docker-compose down
```

## 🔄 工作流程

1. **上传数据** - 支持 GPX, GeoJSON, CSV, JSON 格式
2. **自动转换** - 支持 GPS, 高德, 百度三种坐标系
3. **地点管理** - 自动去重，存储省市区信息
4. **统计展示** - 实时统计覆盖率和地点数量
5. **成就解锁** - 根据探索进度自动解锁成就

## 📋 API 示例

### 获取健康状态
```bash
curl http://localhost:5000/api/health
```

### 获取应用信息
```bash
curl http://localhost:5000/api/info
```

### 获取所有地点
```bash
curl http://localhost:5000/api/locations
```

### 获取统计数据
```bash
curl http://localhost:5000/api/statistics
```

### 获取成就列表
```bash
curl http://localhost:5000/api/achievements
```

### 上传轨迹文件
```bash
curl -X POST -F "file=@track.gpx" http://localhost:5000/api/upload
```

## 🐛 故障排除

### 前端无法连接后端
- 检查 Docker 容器是否运行: `docker-compose ps`
- 查看后端日志: `docker-compose logs backend`
- 确保防火墙允许 5000 端口

### 数据库错误
- 删除旧数据库: `rm -rf data/`
- 重启服务: `docker-compose restart backend`

### 文件上传失败
- 检查文件格式是否支持
- 确保文件编码为 UTF-8
- 查看上传日志了解具体错误

## 📊 支持的坐标格式示例

### GPS 坐标 JSON
```json
{
  "lat": 39.9042,
  "lng": 116.4074,
  "name": "北京",
  "type": "gps"
}
```

### CSV 格式
```csv
name,lat,lng,type
北京,39.9042,116.4074,gps
上海,31.2304,121.4737,gps
```

### GeoJSON
```json
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [116.4074, 39.9042]
    },
    "properties": {"name": "北京"}
  }]
}
```

## 💾 数据备份

```bash
# 备份数据库
docker-compose exec backend sqlite3 /app/data/zhangliangzuji.db .dump > backup.sql

# 恢复数据库
docker-compose exec backend sqlite3 /app/data/zhangliangzuji.db < backup.sql
```

---

更多信息请查看 [README.md](./README.md)