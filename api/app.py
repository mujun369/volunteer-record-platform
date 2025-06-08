from flask import Flask, request, jsonify

app = Flask(__name__)

# 内存存储
volunteer_data = []
usage_data = []

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def index():
    return jsonify({"message": "志愿者积分平台 API", "status": "running"})

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "message": "API 服务正常运行"})

@app.route('/api/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "无效的数据格式"}), 400
        
        if 'activityData' in data and data['activityData']:
            volunteer_data.extend(data['activityData'])
        
        if 'usageData' in data and data['usageData']:
            usage_data.extend(data['usageData'])
        
        return jsonify({
            "success": True,
            "message": "数据提交成功",
            "activity_count": len(data.get('activityData', [])),
            "usage_count": len(data.get('usageData', []))
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

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

if __name__ == "__main__":
    app.run(debug=True)
