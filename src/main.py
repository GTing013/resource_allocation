from data_collection.metrics_collector import MetricsCollector
from resource_allocator.ml_allocator import MLResourceAllocator
from evaluation.performance_evaluator import PerformanceEvaluator
import time

def run_experiment():
    collector = MetricsCollector('prometheus:9090')
    predictor = WorkloadPredictor(input_shape=(24, 4))  # 24个时间步，4个特征
    allocator = MLResourceAllocator(predictor)
    evaluator = PerformanceEvaluator()

    experiment_duration = 3600  # 1小时
    start_time = time.time()

    while time.time() - start_time < experiment_duration:
        # 收集当前指标
        current_metrics = collector.collect_metrics()
        
        # 做出分配决策
        allocation_plan = allocator.make_allocation_decision(
            current_metrics,
            available_resources=get_available_resources()
        )
        
        # 执行资源分配
        apply_allocation(allocation_plan)
        
        # 记录性能指标
        evaluator.record_metrics(current_metrics)
        
        time.sleep(60)  # 每分钟采样一次

    # 实验结束，生成报告
    results = evaluator.calculate_statistics()
    evaluator.plot_metrics()
    return results