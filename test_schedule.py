#!/usr/bin/env python3
"""
调度配置功能测试脚本
演示所有增删改查操作
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def print_section(title):
    """打印分隔符"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_list():
    """测试查询所有配置"""
    print_section("1. 查询所有调度配置")
    
    response = requests.get(f"{BASE_URL}/api/schedule")
    data = response.json()
    
    print(f"✅ 状态: {response.status_code}")
    print(f"📊 总数: {data['count']} 条配置\n")
    
    for config in data['data']:
        print(f"  ID: {config['id']}")
        print(f"  公司: {config['company_short_name']}")
        print(f"  工作流: {config['workflow_name']}")
        print(f"  类型: {config['schedule_config']['type']}")
        print(f"  更新时间: {config['updated_at']}")
        print()

def test_filter_by_company():
    """测试按公司筛选"""
    print_section("2. 按公司筛选 (company=ABC)")
    
    response = requests.get(f"{BASE_URL}/api/schedule?company=ABC")
    data = response.json()
    
    print(f"✅ 状态: {response.status_code}")
    print(f"📊 找到 {data['count']} 条配置\n")
    
    for config in data['data']:
        print(f"  {config['company_short_name']} - {config['workflow_name']}")

def test_filter_by_workflow():
    """测试按工作流筛选"""
    print_section("3. 按工作流筛选 (workflow=数据同步)")
    
    response = requests.get(f"{BASE_URL}/api/schedule?workflow=数据同步")
    data = response.json()
    
    print(f"✅ 状态: {response.status_code}")
    print(f"📊 找到 {data['count']} 条配置\n")
    
    for config in data['data']:
        print(f"  {config['company_short_name']} - {config['workflow_name']}")

def test_add_cron():
    """测试添加 Cron 配置"""
    print_section("4. 添加 Cron 调度配置")
    
    data = {
        'company_short_name': 'TEST1',
        'workflow_name': '测试工作流1',
        'schedule_type': 'cron',
        'cron_expression': '0 10 * * *',
        'timezone': 'Asia/Shanghai'
    }
    
    response = requests.post(f"{BASE_URL}/schedule/add", data=data)
    result = response.json()
    
    print(f"✅ 状态: {response.status_code}")
    print(f"📝 结果: {result['message']}\n")
    print(f"  公司: {data['company_short_name']}")
    print(f"  工作流: {data['workflow_name']}")
    print(f"  类型: Cron")
    print(f"  表达式: {data['cron_expression']}")

def test_add_interval():
    """测试添加 Interval 配置"""
    print_section("5. 添加 Interval 调度配置")
    
    data = {
        'company_short_name': 'TEST2',
        'workflow_name': '测试工作流2',
        'schedule_type': 'interval',
        'interval_minutes': '15',
        'start_time': '09:00',
        'end_time': '17:00'
    }
    
    response = requests.post(f"{BASE_URL}/schedule/add", data=data)
    result = response.json()
    
    print(f"✅ 状态: {response.status_code}")
    print(f"📝 结果: {result['message']}\n")
    print(f"  公司: {data['company_short_name']}")
    print(f"  工作流: {data['workflow_name']}")
    print(f"  类型: Interval")
    print(f"  间隔: {data['interval_minutes']} 分钟")
    print(f"  时间: {data['start_time']} - {data['end_time']}")

def test_add_once():
    """测试添加 Once 配置"""
    print_section("6. 添加 Once 调度配置")
    
    future_time = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT10:00')
    
    data = {
        'company_short_name': 'TEST3',
        'workflow_name': '测试工作流3',
        'schedule_type': 'once',
        'execute_time': future_time
    }
    
    response = requests.post(f"{BASE_URL}/schedule/add", data=data)
    result = response.json()
    
    print(f"✅ 状态: {response.status_code}")
    print(f"📝 结果: {result['message']}\n")
    print(f"  公司: {data['company_short_name']}")
    print(f"  工作流: {data['workflow_name']}")
    print(f"  类型: Once")
    print(f"  执行时间: {future_time}")

def test_update():
    """测试更新配置"""
    print_section("7. 更新调度配置")
    
    # 先查询找到 TEST1 的 ID
    response = requests.get(f"{BASE_URL}/api/schedule?company=TEST1")
    configs = response.json()['data']
    
    if configs:
        config_id = configs[0]['id']
        
        data = {
            'company_short_name': 'TEST1_UPDATED',
            'workflow_name': '测试工作流1_已更新',
            'schedule_type': 'cron',
            'cron_expression': '0 11 * * *',
            'timezone': 'Asia/Shanghai'
        }
        
        response = requests.post(f"{BASE_URL}/schedule/{config_id}/edit", data=data)
        result = response.json()
        
        print(f"✅ 状态: {response.status_code}")
        print(f"📝 结果: {result['message']}\n")
        print(f"  ID: {config_id}")
        print(f"  新公司: {data['company_short_name']}")
        print(f"  新工作流: {data['workflow_name']}")
        print(f"  新表达式: {data['cron_expression']}")
    else:
        print("❌ 未找到 TEST1 配置")

def test_delete():
    """测试删除配置"""
    print_section("8. 删除调度配置")
    
    # 先查询找到 TEST2 的 ID
    response = requests.get(f"{BASE_URL}/api/schedule?company=TEST2")
    configs = response.json()['data']
    
    if configs:
        config_id = configs[0]['id']
        
        response = requests.post(f"{BASE_URL}/schedule/{config_id}/delete")
        result = response.json()
        
        print(f"✅ 状态: {response.status_code}")
        print(f"📝 结果: {result['message']}\n")
        print(f"  已删除 ID: {config_id}")
    else:
        print("❌ 未找到 TEST2 配置")

def test_final_list():
    """最后查询所有配置"""
    print_section("9. 最终配置列表")
    
    response = requests.get(f"{BASE_URL}/api/schedule")
    data = response.json()
    
    print(f"✅ 状态: {response.status_code}")
    print(f"📊 总数: {data['count']} 条配置\n")
    
    for config in data['data']:
        print(f"  [{config['id']}] {config['company_short_name']} - {config['workflow_name']}")

def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("  调度配置功能测试")
    print("="*60)
    
    try:
        test_list()
        test_filter_by_company()
        test_filter_by_workflow()
        test_add_cron()
        test_add_interval()
        test_add_once()
        test_update()
        test_delete()
        test_final_list()
        
        print_section("✅ 所有测试完成！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("请确保 Flask 服务正在运行: python3 run.py")

if __name__ == '__main__':
    main()
