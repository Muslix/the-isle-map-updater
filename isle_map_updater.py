#!/usr/bin/env python3
"""
Isle Map Updater - Modular Version
Simple coordinate tracker for The Isle
Monitors clipboard for coordinates and updates vulnova map automatically.
"""

import time
import threading
import pyperclip
import psutil

# Import our modules
from config_manager import ConfigManager
from coordinate_parser import CoordinateParser
from browser_manager import BrowserManager
from gui_manager import GUIManager


class IsleMapUpdater:
    def __init__(self):
        self.running = False
        self.last_coordinates = ""
        self.test_mode = False
        
        # Initialize managers
        self.config_manager = ConfigManager()
        self.coordinate_parser = CoordinateParser()
        self.browser_manager = BrowserManager()
        self.gui_manager = GUIManager(self)
    
    def is_the_isle_running(self):
        """Check if The Isle game is currently running"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and 'isle' in proc.info['name'].lower():
                    return True
            return False
        except Exception:
            return False
    
    def monitor_clipboard(self):
        """Monitor clipboard for coordinate changes"""
        print("[CLIPBOARD] Monitoring clipboard for coordinate changes...")
        print("[INFO] Copy Isle coordinates to clipboard (e.g., 88,879.526, -288,696.11, 21,112.882)")
        print("[INFO] Raw Isle format supported - no conversion needed!")
        print("[INFO] Press Ctrl+C in terminal to stop")
        print("[MONITOR] Waiting for clipboard changes...")
        
        while self.running:
            try:
                # Get current clipboard content
                current_clipboard = pyperclip.paste()
                
                # Check if clipboard changed and contains potential coordinates
                if current_clipboard != self.last_coordinates and current_clipboard.strip():
                    raw_coords = self.coordinate_parser.parse_coordinates(current_clipboard)
                    
                    if raw_coords is not None:
                        msg = f"[FOUND] Isle coordinates: {raw_coords}"
                        print(msg)
                        self.gui_manager.log_to_gui(msg)
                        
                        if self.browser_manager.driver:
                            success = self.browser_manager.update_map_position(raw_coords)
                            if success:
                                success_msg = "[OK] Map updated successfully!"
                                print(success_msg)
                                self.gui_manager.log_to_gui(success_msg)
                            else:
                                error_msg = "[WARNING] Map update failed"
                                print(error_msg)
                                self.gui_manager.log_to_gui(error_msg)
                        
                        self.last_coordinates = current_clipboard
                    else:
                        # Only show this for non-empty clipboard that doesn't match patterns
                        if len(current_clipboard.strip()) > 0 and len(current_clipboard) < 200:
                            info_msg = f"[INFO] Clipboard: '{current_clipboard[:30]}...'"
                            print(info_msg)
                        self.last_coordinates = current_clipboard
                
                time.sleep(0.3)  # Check every 300ms for faster response
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[ERROR] Monitoring error: {e}")
                time.sleep(1)
    
    def start_monitoring(self):
        """Start coordinate monitoring"""
        if not self.running and self.browser_manager.driver and self.config_manager.get_selected_map():
            self.running = True
            self.gui_manager.log_to_gui("Starting coordinate monitoring...")
            self.gui_manager.log_to_gui("Copy Isle coordinates to clipboard!")
            monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
            monitor_thread.start()
    
    def start(self):
        """Start the map updater with GUI"""
        # Create GUI first
        self.gui_manager.create_gui()
        
        # Initial status
        self.gui_manager.log_to_gui("Isle Map Updater Ready!")
        self.gui_manager.log_to_gui("Click 'Setup Browser & Load Maps' to begin")
        selected_map = self.config_manager.get_selected_map()
        if selected_map:
            self.gui_manager.log_to_gui(f"Will restore saved map: {selected_map}")
        
        # Start GUI (blocks until closed)
        self.gui_manager.start_mainloop()
    
    def stop(self):
        """Stop the map updater"""
        self.running = False
        
        # Proper cleanup of browser resources
        self.browser_manager.stop()
        
        print("[STOP] Isle Map Updater stopped")


def main():
    """Main entry point"""
    print("🗺️ Isle Map Updater - Starting...")
    
    try:
        updater = IsleMapUpdater()
        updater.start()
    except KeyboardInterrupt:
        print("\\n[STOP] Interrupted by user")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    finally:
        print("[EXIT] Isle Map Updater terminated")


if __name__ == "__main__":
    main()