import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def load_and_compare_results():
    """加载并对比测试结果"""
    # 加载传统方法结果
    with open('/Users/huanghaoting/resource_allocation/experiments/baseline/traditional_results_latest.json', 'r') as f:
        traditional = json.load(f)
    
    # 加载改进方法结果
    with open('/Users/huanghaoting/resource_allocation/experiments/results/improved_results_latest.json', 'r') as f:
        improved = json.load(f)
    
    # 计算性能改进
    improvements = {}
    for method in traditional['methods'].keys():
        trad_metrics = traditional['methods'][method]
        impr_metrics = improved['methods'][method]
        
        improvements[method] = {
            '延迟改进': {
                '平均值降低': ((trad_metrics['latency']['avg'] - impr_metrics['latency']['avg']) 
                          / trad_metrics['latency']['avg'] * 100),
                '最大值降低': ((trad_metrics['latency']['max'] - impr_metrics['latency']['max'])
                          / trad_metrics['latency']['max'] * 100)
            },
            '吞吐量改进': {
                '平均值提升': ((impr_metrics['throughput']['avg'] - trad_metrics['throughput']['avg'])
                          / trad_metrics['throughput']['avg'] * 100),
                '峰值提升': ((impr_metrics['throughput']['peak'] - trad_metrics['throughput']['peak'])
                         / trad_metrics['throughput']['peak'] * 100)
            },
            '恢复时间改进': ((trad_metrics['recovery']['avg'] - impr_metrics['recovery']['avg'])
                        / trad_metrics['recovery']['avg'] * 100)
        }
    
    return improvements

def plot_improvements(improvements):
    """绘制性能改进图表"""
    methods = list(improvements.keys())
    metrics = ['延迟改进', '吞吐量改进', '恢复时间改进']
    
    plt.figure(figsize=(12, 6))
    x = np.arange(len(methods))
    width = 0.25
    
    for i, metric in enumerate(metrics):
        values = []
        for method in methods:
            if metric in ['延迟改进', '吞吐量改进']:
                values.append(improvements[method][metric]['平均值降低' if metric == '延迟改进' else '平均值提升'])
            else:
                values.append(improvements[method][metric])
        
        plt.bar(x + i*width, values, width, label=metric)
    
    plt.xlabel('分配方法')
    plt.ylabel('改进百分比 (%)')
    plt.title('各项性能指标改进对比')
    plt.xticks(x + width, methods)
    plt.legend()
    
    plt.savefig('/Users/huanghaoting/resource_allocation/experiments/results/improvements.png')

if __name__ == "__main__":
    print("开始分析性能改进...")
    improvements = load_and_compare_results()
    
    print("\n性能改进分析结果:")
    print("=" * 50)
    
    for method, metrics in improvements.items():
        print(f"\n{method}:")
        print("-" * 30)
        print(f"延迟降低: {metrics['延迟改进']['平均值降低']:.2f}%")
        print(f"吞吐量提升: {metrics['吞吐量改进']['平均值提升']:.2f}%")
        print(f"恢复时间改进: {metrics['恢复时间改进']:.2f}%")
    
    plot_improvements(improvements)
    print("\n性能对比图表已保存到 improvements.png")