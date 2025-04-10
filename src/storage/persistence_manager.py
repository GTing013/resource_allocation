import sqlite3
import json
from datetime import datetime
import logging

class PersistenceManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        
    def _datetime_handler(self, obj):
        """处理日期序列化"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
    def save_workload(self, workload_id, workload_data):
        """保存工作负载数据"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                now = datetime.now()
                # 使用自定义的JSON编码器
                json_data = json.dumps(workload_data, default=self._datetime_handler)
                cursor.execute(
                    'INSERT OR REPLACE INTO workloads (id, data, created_at, updated_at) VALUES (?, ?, ?, ?)',
                    (workload_id, json_data, now, now)
                )
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"保存工作负载失败: {e}")
            return False
            
    def save_metrics(self, workload_id, metrics):
        """保存指标数据"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                now = datetime.now()
                for metric_type, value in metrics.items():
                    cursor.execute(
                        'INSERT INTO metrics (workload_id, metric_type, value, timestamp) VALUES (?, ?, ?, ?)',
                        (workload_id, metric_type, value, now)
                    )
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"保存指标数据失败: {e}")
            return False