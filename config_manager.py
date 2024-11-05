# config_manager.py
import json
import os

class ConfigManager:
    def __init__(self):
        self.config_path = os.getenv('CONFIG_PATH', 'config.json')
        self.config = self._load_config()

    def _load_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"data": {}, "headers": {}, "cookies": {}}
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {"data": {}, "headers": {}, "cookies": {}}

    @property
    def data(self):
        return self.config.get('data', {})

    @property
    def headers(self):
        return self.config.get('headers', {})

    @property
    def cookies(self):
        return self.config.get('cookies', {})
