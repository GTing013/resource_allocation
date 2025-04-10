import sys
import time
import random
import numpy as np
from datetime import datetime
import json  # 添加这行导入

sys.path.append('/Users/huanghaoting/resource_allocation')
from src.resource.traditional_allocators import TraditionalAllocators

class Task:
    def __init__(self, id, priority='low', size='small', weight=1):
        self.id = id
        self.priority = priority
        self.size = size
        self.weight = weight

def quick_performance_test(duration=60):  # 1分钟快速测试
    """快速性能测试"""
    # 创建测试任务
    tasks = [
        Task(1, 'high', 'large', 3),
        Task(2, 'medium', 'medium', 2),
        Task(3, 'low', 'small', 1)
    ]
    
    allocator = TraditionalAllocators()
    methods = {
        '轮询': allocator.round_robin,
        '优先级': allocator.static_priority,
        '固定配额': allocator.fixed_quota,
        '比例分配': allocator.proportional_share
    }
    
    results = {}
    
    for name, method in methods.items():
        print(f"\n测试 {name} 方法...")
        start_time = time.time()
        metrics = {
            'latency': [],
            'throughput': [],
            'recovery_times': []
        }
        
        while time.time() - start_time < duration:
            # 获取分配结果
            allocations = method(tasks)
            
            # 模拟性能指标
            for _, allocation in allocations.items():
                latency = 100 * (1 - allocation/100)  # 模拟延迟
                throughput = allocation * 10  # 模拟吞吐量
                
                metrics['latency'].append(latency)
                metrics['throughput'].append(throughput)
                
                # 模拟故障恢复（5%概率）
                if random.random() < 0.05:
                    recovery_time = random.uniform(0.5, 2.0)
                    metrics['recovery_times'].append(recovery_time)
            
            time.sleep(0.1)  # 降低采样频率
            
        results[name] = {
            'latency': {
                'avg': np.mean(metrics['latency']),
                'max': np.max(metrics['latency'])
            },
            'throughput': {
                'avg': np.mean(metrics['throughput']),
                'peak': np.max(metrics['throughput'])
            },
            'recovery': {
                'avg': np.mean(metrics['recovery_times']) if metrics['recovery_times'] else 0
            }
        }
    
    # 添加时间戳到结果中
    final_results = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'test_duration': duration,
        'methods': results
    }
    
    return final_results

if __name__ == "__main__":
    print("开始快速性能测试...")
    results = quick_performance_test()
    
    # 保存传统方法的测试结果
    save_path = '/Users/huanghaoting/resource_allocation/experiments/baseline/traditional_results_latest.json'
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=4)
    
    print("\n传统方法性能测试结果:")
    print("=" * 50)
    
    for method, metrics in results['methods'].items():
        print(f"\n{method}:")
        print("-" * 30)
        print(f"平均延迟: {metrics['latency']['avg']:.2f}ms")
        print(f"最大延迟: {metrics['latency']['max']:.2f}ms")
        print(f"平均吞吐量: {metrics['throughput']['avg']:.2f}请求/秒")
        print(f"峰值吞吐量: {metrics['throughput']['peak']:.2f}请求/秒")
        print(f"平均恢复时间: {metrics['recovery']['avg']:.2f}秒")