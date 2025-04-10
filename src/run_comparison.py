from config.experiment_config import ExperimentConfig
from allocator.algorithms import RoundRobinAllocator, PriorityBasedAllocator
from evaluation.benchmark import Benchmark
from workload.generator import WorkloadGenerator
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
import matplotlib as mpl

def run_comparison():
    config = ExperimentConfig()
    workload_gen = WorkloadGenerator()
    benchmark = Benchmark()
    
    # 运行所有实验
    print("开始运行实验...")
    benchmark.run_baseline_tests(workload_gen)
    benchmark.run_ml_tests(workload_gen)
    
    # 分析结果
    results = benchmark.compare_results()
    
    # 可视化结果
    plot_results(results)
    
def plot_results(results):
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # MacOS 系统默认支持这个字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    
    plt.figure(figsize=(15, 10))
    
    # 创建子图
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    metrics = ['latency', 'throughput', 'resource_utilization', 'recovery_time']
    titles = ['延迟', '吞吐量', '资源利用率', '恢复时间']
    
    for ax, metric, title in zip(axes.flat, metrics, titles):
        sns.boxplot(data=results[metric], ax=ax)
        ax.set_title(title)
        ax.set_ylabel('值')
        ax.set_xlabel('算法')
    
    plt.suptitle('资源分配算法性能比较')
    plt.tight_layout()
    
    # 保存结果
    plt.savefig('/Users/huanghaoting/resource_allocation/experiments/results/comparison_plot.png', dpi=300)
    plt.close()

if __name__ == '__main__':
    run_comparison()