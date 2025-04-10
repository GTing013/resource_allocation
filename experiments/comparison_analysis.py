import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def load_results(traditional_path, improved_path):
    """加载测试结果"""
    with open(traditional_path, 'r') as f:
        traditional = json.load(f)
    with open(improved_path, 'r') as f:
        improved = json.load(f)
    return traditional, improved

def analyze_improvements(traditional, improved):
    """分析性能改进"""
    improvements = {}
    
    for method in traditional.keys():
        improvements[method] = {
            'latency': {
                'reduction': ((traditional[method]['latency']['avg'] - improved[method]['latency']['avg']) 
                            / traditional[method]['latency']['avg'] * 100),
                'stability': ((traditional[method]['latency']['max'] - improved[method]['latency']['max'])
                            / traditional[method]['latency']['max'] * 100)
            },
            'throughput': {
                'increase': ((improved[method]['throughput']['avg'] - traditional[method]['throughput']['avg'])
                           / traditional[method]['throughput']['avg'] * 100),
                'peak_improvement': ((improved[method]['throughput']['peak'] - traditional[method]['throughput']['peak'])
                                   / traditional[method]['throughput']['peak'] * 100)
            },
            'recovery': {
                'speedup': ((traditional[method]['recovery']['avg'] - improved[method]['recovery']['avg'])
                          / traditional[method]['recovery']['avg'] * 100)
            }
        }
    return improvements

def generate_comparison_report(traditional, improved, improvements):
    """生成对比报告"""
    report = f"""# 资源分配算法性能对比分析报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 性能对比概述

| 分配方法 | 指标 | 传统方法 | 改进方法 | 提升率 |
|---------|------|----------|----------|--------|
"""
    
    for method in traditional.keys():
        report += f"\n### {method}\n"
        report += f"- 延迟性能：降低了 {improvements[method]['latency']['reduction']:.2f}%\n"
        report += f"- 吞吐量：提升了 {improvements[method]['throughput']['increase']:.2f}%\n"
        report += f"- 恢复能力：提升了 {improvements[method]['recovery']['speedup']:.2f}%\n"
        
    return report

def plot_comparison(traditional, improved):
    """绘制性能对比图表"""
    methods = list(traditional.keys())
    metrics = ['latency', 'throughput', 'recovery']
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for i, metric in enumerate(metrics):
        trad_values = [traditional[m][metric]['avg'] for m in methods]
        impr_values = [improved[m][metric]['avg'] for m in methods]
        
        x = np.arange(len(methods))
        width = 0.35
        
        axes[i].bar(x - width/2, trad_values, width, label='传统方法')
        axes[i].bar(x + width/2, impr_values, width, label='改进方法')
        
        axes[i].set_title(f'{metric} 对比')
        axes[i].set_xticks(x)
        axes[i].set_xticklabels(methods, rotation=45)
        axes[i].legend()
    
    plt.tight_layout()
    plt.savefig('/Users/huanghaoting/resource_allocation/experiments/results/comparison_plot.png')

if __name__ == "__main__":
    # 修改为实际的结果文件路径
    traditional_path = '/Users/huanghaoting/resource_allocation/experiments/baseline/traditional_results_latest.json'
    improved_path = '/Users/huanghaoting/resource_allocation/experiments/results/improved_results_latest.json'
    
    traditional, improved = load_results(traditional_path, improved_path)
    improvements = analyze_improvements(traditional, improved)
    
    # 生成报告
    report = generate_comparison_report(traditional, improved, improvements)
    with open('/Users/huanghaoting/resource_allocation/experiments/results/comparison_report.md', 'w') as f:
        f.write(report)
    
    # 生成可视化对比
    plot_comparison(traditional, improved)
    
    # 打印关键改进点
    print("\n性能改进摘要:")
    print("=" * 50)
    for method, metrics in improvements.items():
        print(f"\n{method}:")
        print(f"延迟降低: {metrics['latency']['reduction']:.2f}%")
        print(f"吞吐量提升: {metrics['throughput']['increase']:.2f}%")
        print(f"恢复时间改进: {metrics['recovery']['speedup']:.2f}%")