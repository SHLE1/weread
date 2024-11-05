#push.py
import requests
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PushNotification:
    def __init__(self):
        self.pushplus_url = "https://www.pushplus.plus/send"
        self.telegram_base_url = "https://api.telegram.org/bot{}/sendMessage"
        self.headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
        }

    def push_pushplus(self, content, token):
        """
        Send notification via PushPlus
        """
        try:
            params = {
                "token": token,
                "content": content
            }
            response = requests.get(self.pushplus_url, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info("PushPlus Response: %s", response.text)
            return True
        except Exception as e:
            logger.error("PushPlus通知发送失败: %s", str(e))
            return False

    def push_telegram(self, content, bot_token, chat_id):
        """
        Telegram通知
        """
        try:
            url = self.telegram_base_url.format(bot_token)
            params = {
                "chat_id": chat_id,
                "text": content
            }
            response = requests.post(url, json=params)
            response.raise_for_status()
            logger.info("Telegram Response: %s", response.text)
            return True
        except Exception as e:
            logger.error("Telegram通知发送失败: %s", str(e))
            return False

def push(content):
    """
    统一推送接口
    """
    push_method = os.getenv('PUSH_METHOD', 'none').lower()
    notifier = PushNotification()
    
    if push_method == "pushplus":
        pushplus_token = os.getenv('PUSHPLUS_TOKEN')
        if not pushplus_token:
            logger.error("未设置PUSHPLUS_TOKEN环境变量")
            return False
        return notifier.push_pushplus(content, pushplus_token)
    
    elif push_method == "telegram":
        tg_bot_token = os.getenv('TG_BOT_TOKEN')
        tg_chat_id = os.getenv('TG_CHAT_ID')
        if not all([tg_bot_token, tg_chat_id]):
            logger.error("未设置TG_BOT_TOKEN或TG_CHAT_ID环境变量")
            return False
        return notifier.push_telegram(content, tg_bot_token, tg_chat_id)
    
    elif push_method == "none":
        logger.info("未配置推送方式，跳过推送")
        return True
    
    else:
        logger.error("无效的推送方式: %s", push_method)
        return False