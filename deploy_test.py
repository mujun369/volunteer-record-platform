#!/usr/bin/env python3
"""
本地测试脚本 - 用于在部署到Vercel之前测试API功能
"""

import requests
import json
import sys

def test_api_endpoint(base_url, endpoint, method='GET', data=None):
    """测试API端点"""
    url = f"{base_url}{endpoint}"
    print(f"\n测试 {method} {endpoint}")
    print("-" * 50)
    
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        
        print(f"状态码: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            result = response.json()
            print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        else:
            print(f"响应: {response.text[:200]}...")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

def main():
    # 可以测试本地或Vercel部署的API
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "https://volunteer-record.vercel.app"
    
    print(f"测试API: {base_url}")
    print("=" * 60)
    
    # 测试健康检查
    test_api_endpoint(base_url, "/api/health")
    
    # 测试API信息
    test_api_endpoint(base_url, "/api")
    
    # 测试提交数据
    test_data = {
        "activityData": [
            ["线下活动", "2024年1月志愿活动", "组织者", "张三", "10"],
            ["线下活动", "2024年1月志愿活动", "参与者", "李四", "5"]
        ],
        "usageData": [
            ["张三", "3", "1"]
        ]
    }
    test_api_endpoint(base_url, "/api/submit", "POST", test_data)
    
    # 测试获取汇总数据
    test_api_endpoint(base_url, "/api/get_summary")
    
    # 测试获取使用情况
    test_api_endpoint(base_url, "/api/get_usage_summary")
    
    print("\n" + "=" * 60)
    print("测试完成！")

if __name__ == "__main__":
    main()
