import numpy as np
import matplotlib.pyplot as plt
from ml_resource_allocator import MLResourceAllocator
import time
import logging

def generate_workload_pattern(n_points: int, pattern_type: str = 'sinusoidal'):
    """生成模拟工作负载模式"""
    if pattern_type == 'sinusoidal':
        # 生成周期性负载模式
        t = np.linspace(0, 4*np.pi, n_points)
        cpu_pattern = 0.5 + 0.4 * np.sin(t) + 0.1 * np.random.random(n_points)
        memory_pattern = 0.6 + 0.3 * np.sin(t + np.pi/4) + 0.1 * np.random.random(n_points)
    elif pattern_type == 'spike':
        # 生成突发负载模式
        cpu_pattern = np.random.normal(0.5, 0.1, n_points)
        memory_pattern = np.random.normal(0.6, 0.1, n_points)
        # 添加随机峰值
        spike_points = np.random.choice(n_points, size=int(n_points*0.1), replace=False)
        cpu_pattern[spike_points] *= 2
        memory_pattern[spike_points] *= 1.5
    else:
        # 生成随机负载模式
        cpu_pattern = np.random.normal(0.5, 0.2, n_points)
        memory_pattern = np.random.normal(0.6, 0.2, n_points)
    
    return np.clip(cpu_pattern, 0.1, 1.0), np.clip(memory_pattern, 0.1, 1.0)

def plot_results(actual_cpu, actual_memory, predicted_cpu, predicted_memory, title):
    """绘制实际值与预测值的对比图"""
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(actual_cpu, label='Actual CPU', alpha=0.7)
    plt.plot(predicted_cpu, label='Predicted CPU', linestyle='--')
    plt.title(f'{title} - CPU Usage')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(actual_memory, label='Actual Memory', alpha=0.7)
    plt.plot(predicted_memory, label='Predicted Memory', linestyle='--')
    plt.title('Memory Usage')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(f'resource_allocation_{title.lower()}.png')
    plt.close()

def evaluate_allocator(pattern_type: str, n_points: int = 1000):
    """评估资源分配器的性能"""
    allocator = MLResourceAllocator(history_window=100, prediction_window=10)
    actual_cpu, actual_memory = generate_workload_pattern(n_points, pattern_type)
    
    predicted_cpu_values = []
    predicted_memory_values = []
    allocation_times = []
    prediction_errors = []
    
    # 模拟实时资源分配
    for i in range(n_points):
        start_time = time.time()
        
        # 更新指标并训练模型
        allocator.update_metrics(actual_cpu[i], actual_memory[i])
        if i >= 100 and i % 50 == 0:  # 每50个数据点重新训练一次模型
            allocator.train_model()
        
        # 预测和分配资源
        allocation = allocator.allocate_resources(1.0, 1.0)  # 假设有1.0单位的可用资源
        predicted_cpu_values.append(allocation['cpu'])
        predicted_memory_values.append(allocation['memory'])
        
        # 记录分配时间
        allocation_times.append(time.time() - start_time)
        
        # 评估性能
        if i >= 100:  # 在有足够的历史数据后开始评估
            performance = allocator.evaluate_performance(actual_cpu[i], actual_memory[i])
            prediction_errors.append(performance['average_error'])
    
    # 计算性能指标
    avg_allocation_time = np.mean(allocation_times)
    avg_prediction_error = np.mean(prediction_errors) if prediction_errors else 0
    
    # 绘制结果
    plot_results(
        actual_cpu[100:],
        actual_memory[100:],
        predicted_cpu_values[100:],
        predicted_memory_values[100:],
        pattern_type.capitalize()
    )
    
    return {
        'avg_allocation_time': avg_allocation_time,
        'avg_prediction_error': avg_prediction_error
    }

def main():
    """主函数：运行所有测试场景"""
    patterns = ['sinusoidal', 'spike', 'random']
    results = {}
    
    for pattern in patterns:
        logging.info(f"\nTesting {pattern} workload pattern...")
        results[pattern] = evaluate_allocator(pattern)
        logging.info(f"Results for {pattern}:")
        logging.info(f"Average allocation time: {results[pattern]['avg_allocation_time']*1000:.2f}ms")
        logging.info(f"Average prediction error: {results[pattern]['avg_prediction_error']*100:.2f}%")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()