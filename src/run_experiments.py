import argparse
import pandas as pd
from workload.generator import WorkloadGenerator
from evaluation.benchmark import Benchmark
import os

def main():
    parser = argparse.ArgumentParser(description='运行资源分配实验')
    parser.add_argument('--mode', choices=['baseline', 'ml', 'all'], 
                      default='all', help='实验模式')
    parser.add_argument('--duration', type=int, default=3600,
                      help='实验持续时间(秒)')
    parser.add_argument('--interval', type=int, default=60,
                      help='采样间隔(秒)')
    args = parser.parse_args()

    # 创建输出目录
    output_dir = '/Users/huanghaoting/resource_allocation/experiments/results'
    os.makedirs(output_dir, exist_ok=True)

    # 初始化组件
    workload_generator = WorkloadGenerator()
    benchmark = Benchmark()

    # 运行实验
    if args.mode in ['baseline', 'all']:
        print("运行基准测试...")
        benchmark.run_baseline_tests(workload_generator, args.duration, args.interval)

    if args.mode in ['ml', 'all']:
        print("运行机器学习测试...")
        benchmark.run_ml_tests(workload_generator, args.duration, args.interval)

    # 保存结果
    results_file = benchmark.save_results(output_dir)
    print(f"结果已保存到: {results_file}")

def run_experiments():
    # 创建输出目录
    output_dir = '/Users/huanghaoting/resource_allocation/experiments/results'
    os.makedirs(output_dir, exist_ok=True)
    
    # 初始化组件
    workload_gen = WorkloadGenerator()
    benchmark = Benchmark()
    
    # 运行实验并收集数据
    results = {
        'latency': {},
        'throughput': {},
        'resource_utilization': {},
        'recovery_time': {}
    }
    
    # 运行基准测试
    print("运行基准测试...")
    baseline_results = benchmark.run_baseline_tests(workload_gen, duration=3600, interval=60)
    if baseline_results:  # 添加检查
        for metric in results:
            results[metric].update(baseline_results.get(metric, {}))
    
    # 运行ML测试
    print("运行ML测试...")
    ml_results = benchmark.run_ml_tests(workload_gen, duration=3600, interval=60)
    if ml_results:  # 添加检查
        for metric in results:
            results[metric].update(ml_results.get(metric, {}))
    
    # 保存原始数据
    results_df = pd.DataFrame(results)
    output_file = os.path.join(output_dir, 'experiment_results.csv')
    results_df.to_csv(output_file, index=False)
    print(f"实验结果已保存到: {output_file}")
    
    return output_file

if __name__ == "__main__":
    run_experiments()