import numpy as np

class EfficiencyMonitor:
    def __init__(self, config):
        self.thresholds = config.get('efficiency_thresholds', {
            'cpu': {'min': 60, 'max': 80},
            'memory': {'min': 60, 'max': 80}
        })
        self.window_size = config.get('monitoring_window', 300)  # 5分钟
        
    def monitor_efficiency(self, resource_usage):
        """监控资源使用效率"""
        efficiency_metrics = {}
        
        for resource, usage in resource_usage.items():
            if resource in self.thresholds:
                efficiency_metrics[resource] = self._calculate_efficiency(
                    usage,
                    self.thresholds[resource]
                )
                
        return efficiency_metrics
        
    def _calculate_efficiency(self, usage_data, thresholds):
        """计算资源效率"""
        recent_usage = usage_data[-self.window_size:]
        avg_usage = np.mean(recent_usage)
        
        # 计算效率得分
        if thresholds['min'] <= avg_usage <= thresholds['max']:
            efficiency_score = 100
        else:
            # 根据偏离理想范围的程度减分
            deviation = min(
                abs(avg_usage - thresholds['min']),
                abs(avg_usage - thresholds['max'])
            )
            efficiency_score = max(0, 100 - (deviation * 2))
            
        return {
            'score': efficiency_score,
            'average_usage': avg_usage,
            'stability': np.std(recent_usage),
            'status': 'optimal' if efficiency_score >= 80 else 'suboptimal'
        }
# 将测试代码移到类定义外部
if __name__ == "__main__":
    # 创建测试配置
    test_config = {
        'efficiency_thresholds': {
            'cpu': {'min': 60, 'max': 80},
            'memory': {'min': 60, 'max': 80}
        },
        'monitoring_window': 5  # 简化为5个数据点用于测试
    }
    
    # 创建测试数据
    test_resource_usage = {
        'cpu': [65, 70, 75, 72, 68],
        'memory': [85, 82, 78, 80, 83]
    }
    
    # 创建监控器实例
    monitor = EfficiencyMonitor(test_config)
    
    # 运行监控
    results = monitor.monitor_efficiency(test_resource_usage)
    
    # 打印结果
    print("\n资源使用效率监控结果:")
    print("=" * 50)
    for resource, metrics in results.items():
        print(f"\n{resource.upper()} 效率指标:")
        print("-" * 30)
        for key, value in metrics.items():
            print(f"{key}: {value}")