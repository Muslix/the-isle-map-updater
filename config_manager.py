"""
Configuration management for Isle Map Updater
Handles saving and loading of user preferences
"""

import json
import os
import time


class ConfigManager:
    def __init__(self, config_file="map_config.json"):
        self.config_file = config_file
        self.selected_map = None
        self.load_config()
    
    def load_config(self):
        """Load map configuration from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.selected_map = config.get('selected_map', None)
                    print(f"[CONFIG] Loaded saved map: {self.selected_map}")
            else:
                print("[CONFIG] No config file found, will create on first save")
        except Exception as e:
            print(f"[ERROR] Failed to load config: {e}")
    
    def save_config(self):
        """Save map configuration to JSON file"""
        try:
            config = {
                'selected_map': self.selected_map,
                'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"[CONFIG] Saved map selection: {self.selected_map}")
        except Exception as e:
            print(f"[ERROR] Failed to save config: {e}")
    
    def set_selected_map(self, map_value):
        """Set the selected map and save it"""
        self.selected_map = map_value
        self.save_config()
    
    def get_selected_map(self):
        """Get the currently selected map"""
        return self.selected_map