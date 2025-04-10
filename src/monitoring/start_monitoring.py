from monitoring.collectors.metrics_collector import MetricsCollector
from monitoring.system_monitor import SystemMonitor
from monitoring.alert.alert_manager import AlertManager
import logging
import os

def setup_logging():
    """设置日志"""
    log_dir = '/Users/huanghaoting/resource_allocation/monitoring/logs'
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'{log_dir}/monitoring.log'),
            logging.StreamHandler()
        ]
    )

def main():
    # 设置日志
    setup_logging()
    logger = logging.getLogger('MonitoringSystem')
    
    try:
        # 初始化组件
        metrics_collector = MetricsCollector()
        monitor = SystemMonitor(metrics_collector)
        
        # 开始监控
        logger.info("启动监控系统...")
        monitor.start_monitoring()
        
    except Exception as e:
        logger.error(f"监控系统启动失败: {e}")
        raise

if __name__ == "__main__":
    main()