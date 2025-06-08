"""
Vercel 部署入口点 - 简化版
"""
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# 启用CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 简单的内存存储
volunteer_data = []
usage_data = []

# 根路由
@app.route('/')
def index():
    return jsonify({
        "message": "志愿者积分平台 API",
        "status": "running"
    })

# API信息
@app.route('/api')
@app.route('/api/')
def api_info():
    return jsonify({
        "name": "志愿者积分平台 API",
        "version": "1.0.0",
        "status": "running"
    })

# 健康检查
@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "API 服务正常运行"
    })

# 获取汇总数据
@app.route('/api/get_summary')
def get_summary():
    try:
        summary = {}
        for record in volunteer_data:
            if len(record) >= 5:
                name = record[3]
                score = int(record[4]) if str(record[4]).isdigit() else 0
                summary[name] = summary.get(name, 0) + score

        result = [{"name": name, "total_score": score} for name, score in summary.items()]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取使用情况
@app.route('/api/get_usage_summary')
def get_usage_summary():
    try:
        usage_summary = {}
        for record in usage_data:
            if len(record) >= 3:
                name = record[0]
                used_points = int(record[1]) if str(record[1]).isdigit() else 0
                course_count = int(record[2]) if str(record[2]).isdigit() else 0

                if name in usage_summary:
                    usage_summary[name]['used_points'] += used_points
                    usage_summary[name]['course_count'] += course_count
                else:
                    usage_summary[name] = {
                        'used_points': used_points,
                        'course_count': course_count
                    }

        result = [
            {
                "name": name,
                "used_points": data['used_points'],
                "course_count": data['course_count']
            }
            for name, data in usage_summary.items()
        ]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 提交数据
@app.route('/api/submit', methods=['POST'])
def submit_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "无效的数据格式"}), 400

        # 处理活动数据
        if 'activityData' in data and data['activityData']:
            volunteer_data.extend(data['activityData'])

        # 处理使用数据
        if 'usageData' in data and data['usageData']:
            usage_data.extend(data['usageData'])

        return jsonify({
            "success": True,
            "message": "数据提交成功",
            "activity_count": len(data.get('activityData', [])),
            "usage_count": len(data.get('usageData', []))
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500

# 导出活动总览表
@app.route('/api/export_db')
def export_db():
    try:
        csv_content = "活动类型,活动时间与名称,类别,志愿者名字,积分\n"
        for record in volunteer_data:
            if len(record) >= 5:
                csv_content += ",".join(str(field) for field in record) + "\n"

        return csv_content, 200, {
            'Content-Type': 'text/csv; charset=utf-8',
            'Content-Disposition': 'attachment; filename=volunteer_activity_overview.csv'
        }
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 导出志愿者积分总表
@app.route('/api/export_volunteer_summary')
def export_volunteer_summary():
    try:
        # 计算汇总数据
        summary = {}
        for record in volunteer_data:
            if len(record) >= 5:
                name = record[3]
                score = int(record[4]) if str(record[4]).isdigit() else 0
                summary[name] = summary.get(name, 0) + score

        # 计算使用情况
        usage_summary = {}
        for record in usage_data:
            if len(record) >= 3:
                name = record[0]
                used_points = int(record[1]) if str(record[1]).isdigit() else 0
                course_count = int(record[2]) if str(record[2]).isdigit() else 0

                if name in usage_summary:
                    usage_summary[name]['used_points'] += used_points
                    usage_summary[name]['course_count'] += course_count
                else:
                    usage_summary[name] = {
                        'used_points': used_points,
                        'course_count': course_count
                    }

        # 创建CSV内容
        csv_content = "志愿者名字,总积分,已使用积分,已兑换课程数量,剩余积分\n"
        for name, total_score in summary.items():
            used_info = usage_summary.get(name, {'used_points': 0, 'course_count': 0})
            used_points = used_info['used_points']
            course_count = used_info['course_count']
            remaining = total_score - used_points
            csv_content += f"{name},{total_score},{used_points},{course_count},{remaining}\n"

        return csv_content, 200, {
            'Content-Type': 'text/csv; charset=utf-8',
            'Content-Disposition': 'attachment; filename=volunteer_points_summary.csv'
        }
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 用于本地测试
if __name__ == "__main__":
    app.run(debug=True)
