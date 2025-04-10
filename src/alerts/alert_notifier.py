import smtplib
import requests
import logging
from email.message import EmailMessage
from datetime import datetime

class AlertNotifier:
    def __init__(self, config):
        self.config = config['alerts']
        self.logger = logging.getLogger(__name__)
        
    def send_alert(self, alert_data):
        """发送告警通知"""
        if not self.config['enabled']:
            return True
            
        success = True
        for channel in self.config['channels']:
            if channel['type'] == 'email':
                success &= self._send_email_alert(channel, alert_data)
            elif channel['type'] == 'webhook':
                success &= self._send_webhook_alert(channel, alert_data)
                
        return success
        
    def _send_email_alert(self, channel, alert_data):
        """发送邮件告警"""
        try:
            msg = EmailMessage()
            msg.set_content(self._format_alert_message(alert_data))
            msg['Subject'] = f"系统告警: {alert_data['level']}"
            msg['From'] = "resource_monitor@system.com"
            msg['To'] = channel['recipients']
            
            # TODO: 配置SMTP服务器
            with smtplib.SMTP('localhost') as server:
                server.send_message(msg)
                
            return True
            
        except Exception as e:
            self.logger.error(f"发送邮件告警失败: {e}")
            return False
            
    def _send_webhook_alert(self, channel, alert_data):
        """发送webhook告警"""
        try:
            response = requests.post(
                channel['url'],
                json={
                    'alert': alert_data,
                    'timestamp': datetime.now().isoformat()
                }
            )
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"发送webhook告警失败: {e}")
            return False
            
    def _format_alert_message(self, alert_data):
        """格式化告警消息"""
        return f"""
告警级别: {alert_data['level']}
告警类型: {alert_data['type']}
告警信息: {alert_data['message']}
触发时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""