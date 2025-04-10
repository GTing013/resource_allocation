import sys
import json
import time  # 添加这行
from datetime import datetime, timedelta
import numpy as np

sys.path.append('/Users/huanghaoting/resource_allocation')
from src.resource.traditional_allocators import TraditionalAllocators
from src.analysis.performance_analyzer import PerformanceAnalyzer

class Task:
    def __init__(self, id, priority='low', size='small', weight=1):
        self.id = id
        self.priority = priority
        self.size = size
        self.weight = weight

def run_traditional_benchmark(duration=3600):
    """运行传统分配方式的基准测试"""
    # 创建测试任务
    tasks = [
        Task(1, 'high', 'large', 3),
        Task(2, 'medium', 'medium', 2),
        Task(3, 'low', 'small', 1),
        Task(4, 'medium', 'medium', 2),
        Task(5, 'low', 'small', 1)
    ]
    
    allocator = TraditionalAllocators()
    analyzer = PerformanceAnalyzer()
    
    # 收集各种分配方式的性能指标
    allocation_methods = {
        'round_robin': allocator.round_robin,
        'static_priority': allocator.static_priority,
        'fixed_quota': allocator.fixed_quota,
        'proportional_share': allocator.proportional_share
    }
    
    results = {}
    
    for method_name, method in allocation_methods.items():
        print(f"\n测试 {method_name} 分配方式...")
        
        # 模拟运行并收集指标
        test_data = simulate_workload(method, tasks, duration)
        
        # 分析性能
        analysis = analyzer.analyze_performance(test_data)
        results[method_name] = analysis
        
    # 保存结果
    save_path = f'/Users/huanghaoting/resource_allocation/experiments/baseline/traditional_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=4)
        
    return results

def simulate_workload(allocation_method, tasks, duration):
    """模拟工作负载"""
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=duration)
    
    test_data = {
        'latency_metrics': [],
        'throughput_metrics': [],
        'metrics': {
            'cpu_usage': [],
            'memory_usage': []
        },
        'failure_events': []
    }
    
    # 添加采样间隔，减少数据点数量
    sample_interval = 1  # 每秒采样一次
    last_sample_time = start_time
    
    while datetime.now() < end_time:
        current_time = datetime.now()
        
        # 只在采样间隔时收集数据
        if (current_time - last_sample_time).total_seconds() >= sample_interval:
            # 获取资源分配结果
            allocations = allocation_method(tasks)
            
            # 限制每个列表的最大长度
            max_metrics_length = 3600  # 最多保存1小时的数据点
            
            # 模拟性能指标
            for task_id, allocation in allocations.items():
                # 模拟延迟（分配越多，延迟越低）
                latency = 200 - (allocation * 1.5)
                test_data['latency_metrics'].append(latency)
                
                # 模拟吞吐量（与分配成正比）
                throughput = allocation * 10
                test_data['throughput_metrics'].append(throughput)
                
                # 模拟资源使用率
                cpu_usage = allocation * 0.9
                memory_usage = allocation * 0.85
                
                test_data['metrics']['cpu_usage'].append(cpu_usage)
                test_data['metrics']['memory_usage'].append(memory_usage)
                
                # 限制数据点数量
                if len(test_data['latency_metrics']) > max_metrics_length:
                    test_data['latency_metrics'] = test_data['latency_metrics'][-max_metrics_length:]
                if len(test_data['throughput_metrics']) > max_metrics_length:
                    test_data['throughput_metrics'] = test_data['throughput_metrics'][-max_metrics_length:]
                if len(test_data['metrics']['cpu_usage']) > max_metrics_length:
                    test_data['metrics']['cpu_usage'] = test_data['metrics']['cpu_usage'][-max_metrics_length:]
                if len(test_data['metrics']['memory_usage']) > max_metrics_length:
                    test_data['metrics']['memory_usage'] = test_data['metrics']['memory_usage'][-max_metrics_length:]
            
            last_sample_time = current_time
            
        # 模拟故障事件（降低频率）
        if np.random.random() < 0.001:  # 降低到0.1%的故障概率
            failure_time = datetime.now()
            recovery_time = failure_time + timedelta(seconds=np.random.uniform(30, 40))
            test_data['failure_events'].append({
                'failure_time': failure_time.timestamp(),
                'recovery_time': recovery_time.timestamp()
            })
            
            # 限制故障事件数量
            if len(test_data['failure_events']) > 100:
                test_data['failure_events'] = test_data['failure_events'][-100:]
        
        # 添加短暂休眠，减少CPU使用
        time.sleep(0.1)
            
    return test_data

if __name__ == "__main__":
    print("开始运行传统资源分配方式的基准测试...")
    # 修改为2分钟快速测试
    results = run_traditional_benchmark(duration=120)  # 2分钟测试
    
    print("\n测试完成！结果概览：")
    print("=" * 50)
    
    for method, metrics in results.items():
        print(f"\n{method} 分配方式:")
        print("-" * 30)
        print(f"平均延迟: {metrics['latency']['avg_latency']:.2f}ms")
        print(f"平均吞吐量: {metrics['throughput']['avg_throughput']:.2f}请求/秒")
        print(f"资源利用率: {metrics['resource_efficiency']['resource_utilization']:.2f}%")
        print(f"平均恢复时间: {metrics['recovery_time']['avg_recovery_time']:.2f}秒")