import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

class AlertManager:
    def __init__(self, config=None):
        self.config = config or {
            'email': {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'username': 'your-email@gmail.com',
                'password': 'your-app-password',
                'recipients': ['admin@example.com']
            },
            'alert_levels': {
                'critical': 0.3,
                'warning': 0.2,
                'info': 0.1
            }
        }
        self.logger = logging.getLogger('AlertManager')
        
    def send_alert(self, alert_data):
        """发送告警"""
        severity = self._determine_severity(alert_data)
        message = self._format_alert_message(alert_data, severity)
        
        try:
            self._send_email(message, severity)
            self._log_alert(message, severity)
        except Exception as e:
            self.logger.error(f"发送告警失败: {e}")
            
    def _determine_severity(self, alert_data):
        """确定告警级别"""
        max_change = max(abs(change) for change in alert_data.values())
        
        if max_change >= self.config['alert_levels']['critical']:
            return 'critical'
        elif max_change >= self.config['alert_levels']['warning']:
            return 'warning'
        else:
            return 'info'
            
    def _format_alert_message(self, alert_data, severity):
        """格式化告警消息"""
        message = f"性能告警 [{severity.upper()}]\n\n"
        
        for metric, change in alert_data.items():
            direction = "上升" if change > 0 else "下降"
            percentage = abs(change) * 100
            message += f"{metric}: {direction} {percentage:.1f}%\n"
            
        return message
        
    def _send_email(self, message, severity):
        """发送邮件告警"""
        msg = MIMEMultipart()
        msg['Subject'] = f"[{severity.upper()}] 系统性能告警"
        msg['From'] = self.config['email']['username']
        msg['To'] = ', '.join(self.config['email']['recipients'])
        
        msg.attach(MIMEText(message, 'plain'))
        
        with smtplib.SMTP(self.config['email']['smtp_server'], 
                         self.config['email']['smtp_port']) as server:
            server.starttls()
            server.login(self.config['email']['username'],
                        self.config['email']['password'])
            server.send_message(msg)
            
    def _log_alert(self, message, severity):
        """记录告警日志"""
        self.logger.warning(f"[{severity.upper()}] {message}")