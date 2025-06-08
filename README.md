# 志愿者积分记录平台

这是一个用于记录和管理志愿者积分的Web平台。

## 最近修复的问题 (2024年1月)

### Vercel部署错误修复

**问题描述：**
- 404错误：API端点无法访问
- JavaScript语法错误：模板字符串在某些环境下不兼容
- Promise处理错误：异步请求失败

**修复内容：**

1. **API路径修复**
   - 将所有API调用路径从 `/submit` 改为 `/api/submit`
   - 将所有API调用路径从 `/get_summary` 改为 `/api/get_summary`
   - 将所有API调用路径从 `/get_usage_summary` 改为 `/api/get_usage_summary`
   - 将所有API调用路径从 `/export_db` 改为 `/api/export_db`
   - 将所有API调用路径从 `/export_volunteer_summary` 改为 `/api/export_volunteer_summary`

2. **JavaScript语法修复**
   - 将模板字符串改为字符串拼接以提高兼容性
   - 修复了第795行和第1061行的语法错误
   - 修复了排序功能中的模板字符串问题

3. **API端点完善**
   - 添加了所有缺失的API端点
   - 添加了根路由 `/api` 显示API信息
   - 添加了全局错误处理和CORS支持

4. **测试页面**
   - 创建了 `/templates/test.html` 用于API功能测试
   - 创建了 `deploy_test.py` 脚本用于自动化测试

## 功能特性

- 志愿者活动记录
- 积分计算和汇总
- 积分使用记录
- 数据导出功能
- 志愿者积分查询

## 技术栈

- 前端：HTML, CSS, JavaScript
- 后端：Python Flask
- 数据库：内存存储 (Vercel部署)
- 部署：Vercel

## 访问地址

- 主平台：https://volunteer-record.vercel.app/templates/volunteer_points_platform.html
- API测试：https://volunteer-record.vercel.app/templates/test.html
- 首页：https://volunteer-record.vercel.app/

## 本地运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
python app_lite.py
```

3. 访问 http://localhost:5000

## 测试API

运行测试脚本：
```bash
python deploy_test.py https://volunteer-record.vercel.app
```
