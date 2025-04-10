import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def analyze_performance_comparison():
    # 传统方法数据
    traditional = {
        '轮询': {
            'latency': {'avg': 66.67, 'max': 66.67},
            'throughput': {'avg': 333.33, 'peak': 333.33},
            'recovery_time': {'avg': 1.21}
        },
        '优先级': {
            'latency': {'avg': 66.67, 'max': 80.00},
            'throughput': {'avg': 333.33, 'peak': 500.00},
            'recovery_time': {'avg': 1.25}
        },
        '固定配额': {
            'latency': {'avg': 66.67, 'max': 80.00},
            'throughput': {'avg': 333.33, 'peak': 500.00},
            'recovery_time': {'avg': 1.20}
        },
        '比例分配': {
            'latency': {'avg': 66.67, 'max': 83.33},
            'throughput': {'avg': 333.33, 'peak': 500.00},
            'recovery_time': {'avg': 1.19}
        }
    }
    
    # 改进后数据
    improved = {
        'Round Robin': {
            'latency': {'avg': 161.14},
            'throughput': {'avg': 694.28},
            'resource_utilization': 0.43,
            'recovery_time': {'avg': 35.50}
        },
        'Priority-based': {
            'latency': {'avg': 161.14},
            'throughput': {'avg': 694.28},
            'resource_utilization': 0.43,
            'recovery_time': {'avg': 35.50}
        },
        'Load-based': {
            'latency': {'avg': 161.14},
            'throughput': {'avg': 694.28},
            'resource_utilization': 0.43,
            'recovery_time': {'avg': 35.50}
        },
        'ML-based': {
            'latency': {'avg': 161.14},
            'throughput': {'avg': 694.28},
            'resource_utilization': 0.43,
            'recovery_time': {'avg': 35.50}
        }
    }
    
    report = """# 资源分配算法性能对比分析报告

## 1. 延迟性能对比
- 传统方法平均延迟: 66.67ms (所有算法一致)
- 改进方法平均延迟: 161.14ms
- 变化: 延迟增加了 141.7%
- 分析: 改进版本的延迟增加，可能是由于更复杂的资源调度策略导致

## 2. 吞吐量对比
- 传统方法平均吞吐量: 333.33 请求/秒
- 改进方法平均吞吐量: 694.28 请求/秒
- 变化: 吞吐量提升了 108.3%
- 分析: 显著的吞吐量提升，表明资源利用效率得到优化

## 3. 恢复时间对比
- 传统方法平均恢复时间: 1.21秒
- 改进方法平均恢复时间: 35.50秒
- 变化: 恢复时间增加了 2833.9%
- 分析: 恢复时间显著增加，需要进一步优化故障恢复机制

## 4. 算法特性对比
### 传统方法:
- 各算法性能表现相近
- 延迟稳定在较低水平
- 快速故障恢复
- 吞吐量相对较低

### 改进方法:
- 引入了负载均衡和机器学习策略
- 显著提高了系统吞吐量
- 增加了资源利用率监控
- 故障恢复机制变得更复杂

## 5. 优化建议
1. 延迟优化:
   - 优化资源调度算法
   - 减少调度开销
   - 引入缓存机制

2. 故障恢复优化:
   - 简化恢复流程
   - 实现快速故障检测
   - 添加故障预防机制

3. 平衡策略:
   - 在高吞吐量和低延迟之间寻找平衡点
   - 根据实际负载动态调整策略
   - 优化资源分配算法

## 6. 结论
改进版本在吞吐量方面取得了显著提升，但延迟和故障恢复时间有所增加。建议下一步重点优化这两个方面，在保持高吞吐量的同时，降低延迟和恢复时间。
"""
    
    # 保存报告
    with open('/Users/huanghaoting/resource_allocation/experiments/results/comparison_analysis.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 绘制对比图表
    plot_comparison(traditional, improved)

def plot_comparison(traditional, improved):
    metrics = ['延迟', '吞吐量', '恢复时间']
    trad_values = [66.67, 333.33, 1.21]
    impr_values = [161.14, 694.28, 35.50]
    
    plt.figure(figsize=(12, 6))
    x = np.arange(len(metrics))
    width = 0.35
    
    plt.bar(x - width/2, trad_values, width, label='传统方法')
    plt.bar(x + width/2, impr_values, width, label='改进方法')
    
    plt.xlabel('性能指标')
    plt.ylabel('数值')
    plt.title('性能对比分析')
    plt.xticks(x, metrics)
    plt.legend()
    
    plt.savefig('/Users/huanghaoting/resource_allocation/experiments/results/performance_comparison.png')

if __name__ == "__main__":
    analyze_performance_comparison()
    print("分析完成！报告和图表已生成。")