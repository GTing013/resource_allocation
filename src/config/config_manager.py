import yaml
import os
import logging.config
from datetime import datetime

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self._load_config()
        self._setup_logging()
        
    def _load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"加载配置文件失败: {e}")
            
    def _setup_logging(self):
        """设置日志配置"""
        log_config = self.config.get('logging', {})
        log_dir = log_config.get('directory', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # 配置日志轮转
        logging.config.dictConfig({
            'version': 1,
            'formatters': {
                'detailed': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                }
            },
            'handlers': {
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': os.path.join(log_dir, 'system.log'),
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 5,
                    'formatter': 'detailed'
                },
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'detailed'
                }
            },
            'root': {
                'level': 'INFO',
                'handlers': ['file', 'console']
            }
        })