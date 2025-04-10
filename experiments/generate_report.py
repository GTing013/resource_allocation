import json
from datetime import datetime
import sys
sys.path.append('/Users/huanghaoting/resource_allocation/src')

from analysis.performance_analyzer import PerformanceAnalyzer

def generate_performance_report(current_data, template_path, output_path):
    """生成性能报告"""
    # 加载基准数据
    try:
        with open('/Users/huanghaoting/resource_allocation/experiments/baseline/baseline_metrics.json', 'r') as f:
            baseline_data = json.load(f)
    except FileNotFoundError:
        print("错误：未找到基准数据，请先运行 collect_baseline.py")
        return
    
    # 计算改进率
    improvements = calculate_improvements(baseline_data['metrics'], current_data)
    
    # 读取报告模板
    with open(template_path, 'r') as f:
        template = f.read()
    
    # 填充报告数据
    report = template.format(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        baseline_latency=baseline_data['metrics']['latency']['avg'],
        current_latency=current_data['latency']['avg'],
        latency_improvement=improvements['latency'],
        # ... 其他指标类似 ...
    )
    
    # 保存报告
    with open(output_path, 'w') as f:
        f.write(report)

def calculate_improvements(baseline, current):
    """计算各指标的改进率"""
    return {
        'latency': ((baseline['latency']['avg'] - current['latency']['avg']) / baseline['latency']['avg']) * 100,
        'throughput': ((current['throughput']['avg'] - baseline['throughput']['avg']) / baseline['throughput']['avg']) * 100,
        'resource_utilization': ((current['resource_utilization']['avg'] - baseline['resource_utilization']['avg']) / baseline['resource_utilization']['avg']) * 100,
        'recovery_time': ((baseline['recovery_time']['avg'] - current['recovery_time']['avg']) / baseline['recovery_time']['avg']) * 100
    }