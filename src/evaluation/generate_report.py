import pandas as pd
import numpy as np
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self, results_path):
        self.results_path = results_path
        self.results = self._load_results()
        
    def _load_results(self):
        """加载实验结果"""
        results_files = [f for f in os.listdir(self.results_path) if f.endswith('.csv')]
        if not results_files:
            raise FileNotFoundError("未找到实验结果文件")
        
        # 加载最新的结果文件
        latest_file = max(results_files, key=lambda x: os.path.getctime(os.path.join(self.results_path, x)))
        return pd.read_csv(os.path.join(self.results_path, latest_file))
    
    def generate_report(self):
        """生成性能评估报告"""
        report_path = os.path.join(self.results_path, f'performance_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 资源分配算法性能评估报告\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 添加总体性能概述
            f.write("## 性能概述\n\n")
            self._write_overview(f)
            
            # 添加详细指标分析
            f.write("## 详细指标分析\n\n")
            self._write_metrics_analysis(f)
            
            # 添加算法比较
            f.write("## 算法比较\n\n")
            self._write_algorithm_comparison(f)
            
            # 添加建议
            f.write("## 优化建议\n\n")
            self._write_recommendations(f)
        
        return report_path
    
    def _write_overview(self, f):
        """写入性能概述"""
        f.write("### 测试场景\n")
        f.write("- 测试持续时间: 1小时\n")
        f.write("- 采样间隔: 60秒\n")
        f.write("- 测试算法: Round Robin, Priority-based, Load-based, ML-based\n\n")
    
    def _process_metric_data(self, metric_str):
        """处理指标数据字符串"""
        try:
            # 去除方括号并分割成数值列表
            values = [float(x.strip()) for x in metric_str.strip('[]').split(',')]
            return {
                'mean': np.mean(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values)
            }
        except Exception as e:
            print(f"处理数据时出错: {e}")
            return None

    def _write_metrics_analysis(self, f):
        """写入指标分析"""
        metrics = ['latency', 'throughput', 'resource_utilization', 'recovery_time']
        metric_names = {
            'latency': '延迟 (ms)',
            'throughput': '吞吐量 (请求/秒)',
            'resource_utilization': '资源利用率 (%)',
            'recovery_time': '恢复时间 (秒)'
        }
        
        for metric in metrics:
            f.write(f"### {metric_names[metric]}\n")
            if metric in self.results:
                # 处理每个算法的数据
                data = self._process_metric_data(self.results[metric].iloc[0])
                if data:
                    f.write(f"- 平均值: {data['mean']:.2f}\n")
                    f.write(f"- 标准差: {data['std']:.2f}\n")
                    f.write(f"- 最小值: {data['min']:.2f}\n")
                    f.write(f"- 最大值: {data['max']:.2f}\n")
                    
                    # 添加性能分析
                    if metric == 'latency':
                        f.write(f"\n延迟表现：{'良好' if data['mean'] < 150 else '需要优化'}\n")
                    elif metric == 'throughput':
                        f.write(f"\n吞吐量表现：{'良好' if data['mean'] > 800 else '需要优化'}\n")
                    elif metric == 'resource_utilization':
                        f.write(f"\n资源利用率：{'良好' if 0.6 < data['mean'] < 0.8 else '需要优化'}\n")
                    elif metric == 'recovery_time':
                        f.write(f"\n恢复能力：{'良好' if data['mean'] < 30 else '需要优化'}\n")
            else:
                f.write("未找到相关数据\n")
            f.write("\n")

    def _write_algorithm_comparison(self, f):
        """写入算法比较"""
        algorithms = ['round_robin', 'priority_based', 'load_based', 'ml_allocator']
        algo_names = {
            'round_robin': 'Round Robin算法',
            'priority_based': '优先级算法',
            'load_based': '负载均衡算法',
            'ml_allocator': '机器学习算法'
        }
        
        for algo in algorithms:
            f.write(f"### {algo_names[algo]}\n")
            f.write("性能特点：\n")
            
            # 分析每个指标
            for metric in ['latency', 'throughput', 'resource_utilization', 'recovery_time']:
                if metric in self.results:
                    data = self._process_metric_data(self.results[metric].iloc[0])
                    if data:
                        f.write(f"- {metric}: {data['mean']:.2f} (平均值)\n")
            f.write("\n")
    
    def _write_algorithm_performance(self, f, algo):
        """写入算法性能分析"""
        metrics = ['latency', 'throughput', 'resource_utilization', 'recovery_time']
        for metric in metrics:
            if metric in self.results.columns:
                try:
                    metric_data = eval(self.results[metric].iloc[0])
                    if algo in metric_data:
                        data = metric_data[algo]
                        f.write(f"- {metric}:\n")
                        f.write(f"  - 平均值: {data['mean']:.2f}\n")
                        f.write(f"  - 标准差: {data['std']:.2f}\n")
                except (ValueError, SyntaxError, KeyError) as e:
                    f.write(f"- {metric}: 数据解析错误\n")
    
    def _write_recommendations(self, f):
        """写入优化建议"""
        f.write("基于测试结果，建议如下：\n\n")
        f.write("1. 负载均衡优化\n")
        f.write("2. 资源预留策略调整\n")
        f.write("3. 故障恢复机制改进\n")
        f.write("4. 机器学习模型优化\n")

if __name__ == "__main__":
    results_path = "/Users/huanghaoting/resource_allocation/experiments/results"
    generator = ReportGenerator(results_path)
    report_path = generator.generate_report()
    print(f"报告已生成: {report_path}")