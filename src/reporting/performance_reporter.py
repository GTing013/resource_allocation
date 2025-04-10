import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import logging
import os
import json

class PerformanceReporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_report(self, workload_id, workload_data, metrics_data):
        """生成性能报告"""
        try:
            # 生成报告内容
            report_data = self._analyze_performance(workload_data, metrics_data)
            
            # 生成图表
            self._generate_charts(workload_id, metrics_data)
            
            # 保存报告
            self._save_report(workload_id, report_data)
            
            return True
        except Exception as e:
            self.logger.error(f"生成性能报告失败: {e}")
            return False
    
    def _analyze_performance(self, workload_data, metrics_data):
        """分析性能数据"""
        try:
            # 基础统计信息
            basic_stats = {
                'cpu_usage': {
                    'current': metrics_data['cpu_usage'],
                    'average': sum(workload_data['metrics']['cpu_usage']) / len(workload_data['metrics']['cpu_usage']) if workload_data['metrics']['cpu_usage'] else 0,
                    'peak': max(workload_data['metrics']['cpu_usage']) if workload_data['metrics']['cpu_usage'] else 0
                },
                'memory_usage': {
                    'current': metrics_data['memory_usage'],
                    'average': sum(workload_data['metrics']['memory_usage']) / len(workload_data['metrics']['memory_usage']) if workload_data['metrics']['memory_usage'] else 0,
                    'peak': max(workload_data['metrics']['memory_usage']) if workload_data['metrics']['memory_usage'] else 0
                }
            }
            
            # 性能评估
            performance_rating = self._calculate_performance_rating(basic_stats)
            
            return {
                'basic_stats': basic_stats,
                'performance_rating': performance_rating,
                'workload_status': workload_data['status'],
                'analysis_time': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"分析性能数据失败: {e}")
            return None
            
    def _calculate_performance_rating(self, stats):
        """计算性能评级"""
        try:
            cpu_rating = 100 - stats['cpu_usage']['average']
            memory_rating = 100 - stats['memory_usage']['average']
            
            overall_rating = (cpu_rating + memory_rating) / 2
            
            if overall_rating >= 80:
                return 'Excellent'
            elif overall_rating >= 60:
                return 'Good'
            elif overall_rating >= 40:
                return 'Fair'
            else:
                return 'Poor'
                
        except Exception as e:
            self.logger.error(f"计算性能评级失败: {e}")
            return 'Unknown'
    
    def _generate_charts(self, workload_id, metrics_data):
        """生成性能图表"""
        try:
            plt.figure(figsize=(12, 6))
            
            # CPU使用率图表
            plt.subplot(1, 2, 1)
            plt.plot(metrics_data['cpu_usage'], label='CPU Usage')
            plt.title('CPU Usage Over Time')
            plt.xlabel('Time')
            plt.ylabel('Usage (%)')
            plt.legend()
            
            # 内存使用率图表
            plt.subplot(1, 2, 2)
            plt.plot(metrics_data['memory_usage'], label='Memory Usage')
            plt.title('Memory Usage Over Time')
            plt.xlabel('Time')
            plt.ylabel('Usage (MB)')
            plt.legend()
            
            # 保存图表
            chart_path = os.path.join(self.output_dir, f'{workload_id}_performance.png')
            plt.savefig(chart_path)
            plt.close()
            
            return chart_path
            
        except Exception as e:
            self.logger.error(f"生成图表失败: {e}")
            return None
            
    def _save_report(self, workload_id, report_data):
        """保存性能报告"""
        try:
            report_path = os.path.join(self.output_dir, f'{workload_id}_report.json')
            
            # 转换datetime对象为字符串
            if 'analysis_time' in report_data:
                report_data['analysis_time'] = report_data['analysis_time'].isoformat()
                
            with open(report_path, 'w') as f:
                json.dumps(report_data, f, indent=4)
                
            return True
            
        except Exception as e:
            self.logger.error(f"保存报告失败: {e}")
            return False