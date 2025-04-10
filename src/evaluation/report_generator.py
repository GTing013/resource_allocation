import pandas as pd
import numpy as np

class ReportGenerator:
    def __init__(self, results):
        self.results = results
        
    def generate_summary(self):
        summary = {}
        for metric in self.results.columns:
            summary[metric] = {
                'best_algorithm': self._find_best_algorithm(metric),
                'improvement': self._calculate_improvement(metric),
                'statistics': self._calculate_statistics(metric)
            }
        return summary
    
    def save_report(self, output_path):
        summary = self.generate_summary()
        
        with open(output_path, 'w') as f:
            f.write("# 资源分配算法性能评估报告\n\n")
            
            for metric, data in summary.items():
                f.write(f"## {metric} 分析\n")
                f.write(f"- 最佳算法: {data['best_algorithm']}\n")
                f.write(f"- 相对基准的改进: {data['improvement']:.2f}%\n")
                f.write("- 详细统计:\n")
                for stat, value in data['statistics'].items():
                    f.write(f"  - {stat}: {value:.2f}\n")
                f.write("\n")