import logging
from datetime import datetime

class AlertManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.alert_thresholds = {
            'cpu_usage': 90,
            'memory_usage': 85,
            'response_time': 1000
        }
        self.alert_history = {}
        
    def check_alerts(self, workload_id, metrics):
        """检查告警条件"""
        alerts = []
        
        if metrics['cpu_usage'] > self.alert_thresholds['cpu_usage']:
            alerts.append({
                'type': 'cpu_usage',
                'level': 'warning',
                'message': f"CPU使用率超过{self.alert_thresholds['cpu_usage']}%"
            })
            
        if metrics['memory_usage'] > self.alert_thresholds['memory_usage']:
            alerts.append({
                'type': 'memory_usage',
                'level': 'warning',
                'message': f"内存使用率超过{self.alert_thresholds['memory_usage']}%"
            })
            
        if alerts:
            self._record_alert(workload_id, alerts)
            self._send_alerts(workload_id, alerts)
            
        return alerts
        
    def _record_alert(self, workload_id, alerts):
        """记录告警历史"""
        if workload_id not in self.alert_history:
            self.alert_history[workload_id] = []
            
        for alert in alerts:
            alert['timestamp'] = datetime.now()
            self.alert_history[workload_id].append(alert)
            
    def _send_alerts(self, workload_id, alerts):
        """发送告警"""
        for alert in alerts:
            self.logger.warning(
                f"工作负载 {workload_id} 告警: {alert['message']}"
            )