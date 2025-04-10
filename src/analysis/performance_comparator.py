import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class PerformanceComparator:
    def __init__(self):
        self.baseline_metrics = {
            'traditional': {
                'cpu_efficiency': 65,
                'memory_efficiency': 70,
                'response_time': 150,  # ms
                'resource_waste': 25,  # %
                'adaptation_speed': 300  # s
            },
            'static_allocation': {
                'cpu_efficiency': 55,
                'memory_efficiency': 60,
                'response_time': 180,
                'resource_waste': 35,
                'adaptation_speed': 0
            },
            'dynamic_allocation': {
                'cpu_efficiency': 75,
                'memory_efficiency': 78,
                'response_time': 120,
                'resource_waste': 15,
                'adaptation_speed': 180
            }
        }
        
    def compare_performance(self, current_metrics):
        """比较性能指标"""
        comparison = {
            'metrics_comparison': self._compare_metrics(current_metrics),
            'advantages': self._analyze_advantages(current_metrics),
            'disadvantages': self._analyze_disadvantages(current_metrics),
            'tradeoffs': self._analyze_tradeoffs(current_metrics)
        }
        
        # 生成可视化比较
        self._generate_comparison_charts(current_metrics)
        
        return comparison
        
    def _compare_metrics(self, current):
        """对比各项指标"""
        comparison_df = pd.DataFrame(columns=['Current', 'Traditional', 'Static', 'Dynamic'])
        
        metrics = ['cpu_efficiency', 'memory_efficiency', 'response_time', 
                  'resource_waste', 'adaptation_speed']
                  
        for metric in metrics:
            comparison_df.loc[metric] = [
                current.get(metric, 0),
                self.baseline_metrics['traditional'][metric],
                self.baseline_metrics['static_allocation'][metric],
                self.baseline_metrics['dynamic_allocation'][metric]
            ]
            
        return comparison_df
        
    def _analyze_advantages(self, current):
        """分析优势"""
        advantages = []
        
        # CPU效率分析
        if current['cpu_efficiency'] > self.baseline_metrics['traditional']['cpu_efficiency']:
            advantages.append({
                'aspect': 'CPU效率',
                'improvement': f"{(current['cpu_efficiency'] - self.baseline_metrics['traditional']['cpu_efficiency']):.1f}%",
                'impact': '提高资源利用率，降低成本'
            })
            
        # 内存效率分析
        if current['memory_efficiency'] > self.baseline_metrics['traditional']['memory_efficiency']:
            advantages.append({
                'aspect': '内存效率',
                'improvement': f"{(current['memory_efficiency'] - self.baseline_metrics['traditional']['memory_efficiency']):.1f}%",
                'impact': '更好的内存管理，减少浪费'
            })
            
        # 响应时间分析
        if current['response_time'] < self.baseline_metrics['traditional']['response_time']:
            advantages.append({
                'aspect': '响应时间',
                'improvement': f"{(self.baseline_metrics['traditional']['response_time'] - current['response_time']):.1f}ms",
                'impact': '提升用户体验和系统性能'
            })
            
        return advantages
        
    def _analyze_disadvantages(self, current):
        """分析劣势"""
        disadvantages = []
        
        # 分析各项指标的不足
        if current['adaptation_speed'] > self.baseline_metrics['dynamic_allocation']['adaptation_speed']:
            disadvantages.append({
                'aspect': '适应速度',
                'gap': f"{(current['adaptation_speed'] - self.baseline_metrics['dynamic_allocation']['adaptation_speed']):.1f}s",
                'impact': '资源调整响应较慢'
            })
            
        return disadvantages
        
    def _analyze_tradeoffs(self, current):
        """分析权衡"""
        return {
            'efficiency_vs_stability': {
                'description': '高效率与稳定性的权衡',
                'current_balance': '偏向效率' if current['cpu_efficiency'] > 75 else '偏向稳定性',
                'recommendation': self._get_balance_recommendation(current)
            },
            'adaptation_vs_overhead': {
                'description': '适应性与系统开销的权衡',
                'current_balance': self._evaluate_adaptation_balance(current),
                'impact': '需要在资源调整频率和系统开销之间找到平衡点'
            }
        }
        
    def _get_balance_recommendation(self, metrics):
        """获取平衡建议"""
        if metrics['cpu_efficiency'] > 80 and metrics['stability'] < 5:
            return "当前平衡良好，建议保持"
        elif metrics['cpu_efficiency'] > 80:
            return "建议适当降低资源利用率，提高稳定性"
        else:
            return "可以适当提高资源利用率，当前过于保守"
            
    def _evaluate_adaptation_balance(self, metrics):
        """评估适应性平衡"""
        adaptation_score = (metrics['adaptation_speed'] / self.baseline_metrics['traditional']['adaptation_speed']) * 100
        
        if adaptation_score < 80:
            return "快速适应，较高系统开销"
        elif adaptation_score > 120:
            return "低系统开销，适应较慢"
        else:
            return "适应性和开销平衡良好"
    
    def _generate_comparison_charts(self, current_metrics):
        """生成比较图表"""
        plt.figure(figsize=(15, 10))
        
        # 性能指标雷达图
        metrics = ['cpu_efficiency', 'memory_efficiency', 'response_time', 
                  'resource_waste', 'adaptation_speed']
        
        values_current = [current_metrics[m] for m in metrics]
        values_traditional = [self.baseline_metrics['traditional'][m] for m in metrics]
        values_dynamic = [self.baseline_metrics['dynamic_allocation'][m] for m in metrics]
        
        angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False)
        
        ax = plt.subplot(111, polar=True)
        ax.plot(angles, values_current, 'o-', linewidth=2, label='Current')
        ax.plot(angles, values_traditional, 'o-', linewidth=2, label='Traditional')
        ax.plot(angles, values_dynamic, 'o-', linewidth=2, label='Dynamic')
        
        ax.set_xticks(angles)
        ax.set_xticklabels(metrics)
        ax.legend(loc='upper right')
        
        plt.title('Performance Metrics Comparison')
        plt.savefig(f'performance_comparison_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        plt.close()

# 将主函数移到类定义外部
if __name__ == "__main__":
    # 创建测试数据
    current_metrics = {
        'cpu_efficiency': 70,
        'memory_efficiency': 81.6,
        'response_time': 110,
        'resource_waste': 18,
        'adaptation_speed': 200,
        'stability': 3.41
    }
    
    # 创建比较器实例
    comparator = PerformanceComparator()
    
    # 运行比较分析
    results = comparator.compare_performance(current_metrics)
    
    # 打印分析结果
    print("\n性能比较分析结果:")
    print("=" * 50)
    
    print("\n1. 指标对比:")
    print(results['metrics_comparison'])
    
    print("\n2. 主要优势:")
    for advantage in results['advantages']:
        print(f"\n{advantage['aspect']}:")
        print(f"- 改进: {advantage['improvement']}")
        print(f"- 影响: {advantage['impact']}")
    
    print("\n3. 需要改进:")
    for disadvantage in results['disadvantages']:
        print(f"\n{disadvantage['aspect']}:")
        print(f"- 差距: {disadvantage['gap']}")
        print(f"- 影响: {disadvantage['impact']}")
    
    print("\n4. 权衡分析:")
    for aspect, analysis in results['tradeoffs'].items():
        print(f"\n{analysis['description']}:")
        print(f"- 当前平衡: {analysis['current_balance']}")
        if 'recommendation' in analysis:
            print(f"- 建议: {analysis['recommendation']}")
        if 'impact' in analysis:
            print(f"- 影响: {analysis['impact']}")