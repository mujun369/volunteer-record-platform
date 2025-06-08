from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# 内存存储
volunteer_data = []
usage_data = []

# CORS支持
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 简单的HTML页面
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>志愿者积分平台</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .btn { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
        .btn:hover { background-color: #45a049; }
        .status { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .success { background-color: #d4edda; color: #155724; }
        .error { background-color: #f8d7da; color: #721c24; }
        .form-group { margin: 10px 0; }
        input, select { width: 100%; padding: 8px; margin: 5px 0; border: 1px solid #ddd; border-radius: 4px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>志愿者积分记录平台</h1>
    
    <div id="status"></div>
    
    <h2>测试API连接</h2>
    <button class="btn" onclick="testAPI()">测试API</button>
    
    <h2>添加活动记录</h2>
    <form id="activity-form">
        <div class="form-group">
            <input type="text" id="activity-name" placeholder="活动名称" required>
            <input type="text" id="volunteer-name" placeholder="志愿者名字" required>
            <input type="number" id="points" placeholder="积分" required>
            <button type="submit" class="btn">添加记录</button>
        </div>
    </form>
    
    <h2>积分汇总</h2>
    <button class="btn" onclick="loadSummary()">刷新数据</button>
    <table id="summary-table">
        <thead>
            <tr><th>志愿者名字</th><th>总积分</th></tr>
        </thead>
        <tbody id="summary-tbody"></tbody>
    </table>

    <script>
        function showStatus(message, isError = false) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + (isError ? 'error' : 'success');
            setTimeout(() => status.textContent = '', 3000);
        }

        async function testAPI() {
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                showStatus('API测试成功: ' + data.message);
            } catch (error) {
                showStatus('API测试失败: ' + error.message, true);
            }
        }

        document.getElementById('activity-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                activityData: [[
                    '线下活动',
                    document.getElementById('activity-name').value,
                    '参与者',
                    document.getElementById('volunteer-name').value,
                    document.getElementById('points').value
                ]]
            };
            
            try {
                const response = await fetch('/api/submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                if (result.success) {
                    showStatus('记录添加成功！');
                    e.target.reset();
                    loadSummary();
                } else {
                    showStatus('添加失败: ' + result.message, true);
                }
            } catch (error) {
                showStatus('网络错误: ' + error.message, true);
            }
        });

        async function loadSummary() {
            try {
                const response = await fetch('/api/get_summary');
                const data = await response.json();
                
                const tbody = document.getElementById('summary-tbody');
                tbody.innerHTML = '';
                
                data.forEach(item => {
                    const row = tbody.insertRow();
                    row.insertCell(0).textContent = item.name;
                    row.insertCell(1).textContent = item.total_score;
                });
                
                showStatus('数据加载成功！');
            } catch (error) {
                showStatus('加载数据失败: ' + error.message, true);
            }
        }

        // 页面加载时测试API
        window.addEventListener('DOMContentLoaded', () => {
            testAPI();
            loadSummary();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

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
