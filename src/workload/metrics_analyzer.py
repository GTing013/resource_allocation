import numpy as np
from datetime import datetime, timedelta
import pandas as pd

class MetricsAnalyzer:
    def __init__(self):
        self.metrics_window = 3600  # 1小时的数据窗口
        
    def analyze_metrics(self, metrics_data):
        """分析性能指标"""
        df = pd.DataFrame(metrics_data)
        
        return {
            'basic_stats': self._calculate_basic_stats(df),
            'trends': self._analyze_trends(df),
            'anomalies': self._detect_anomalies(df)
        }
        
    def _calculate_basic_stats(self, df):
        """计算基础统计指标"""
        stats = {}
        for metric in ['cpu_usage', 'memory_usage']:
            stats[metric] = {
                'mean': df[metric].mean(),
                'std': df[metric].std(),
                'min': df[metric].min(),
                'max': df[metric].max(),
                'p95': df[metric].quantile(0.95)
            }
        return stats
        
    def _analyze_trends(self, df):
        """分析指标趋势"""
        trends = {}
        for metric in ['cpu_usage', 'memory_usage']:
            # 计算移动平均
            ma = df[metric].rolling(window=12).mean()  # 1分钟移动平均
            
            # 计算趋势斜率
            slope = np.polyfit(range(len(df)), df[metric], 1)[0]
            
            trends[metric] = {
                'slope': slope,
                'trend': 'increasing' if slope > 0.1 else 'decreasing' if slope < -0.1 else 'stable',
                'moving_average': ma.tolist()
            }
        return trends
        
    def _detect_anomalies(self, df):
        """检测异常值"""
        anomalies = {}
        for metric in ['cpu_usage', 'memory_usage']:
            mean = df[metric].mean()
            std = df[metric].std()
            
            # 使用3个标准差作为异常判断标准
            threshold = mean + 3 * std
            anomalies[metric] = {
                'count': len(df[df[metric] > threshold]),
                'timestamps': df[df[metric] > threshold].index.tolist()
            }
        return anomalies