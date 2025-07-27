#!/usr/bin/env python3
"""
Isle Map Updater - Simple coordinate tracker for The Isle
Monitors clipboard for coordinates and updates vulnona map automatically.
"""

import time
import re
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import psutil
import os


class IsleMapUpdater:
    def __init__(self):
        self.driver = None
        self.running = False
        self.last_coordinates = ""
        self.vulnova_url = "https://vulnona.com/game/map/"
        self.test_mode = False
        self.test_coordinates = [
            "88,879.526, -288,696.11, 21,112.882",
            "89,123.456, -289,123.45, 22,456.789",
            "87,654.321, -287,987.65, 20,789.123",
            "90,111.222, -290,333.44, 23,555.666",
            "86,999.888, -286,777.99, 19,444.333"
        ]
        self.test_index = 0
        self.gui = None
        self.status_text = None
        
    def setup_browser(self):
        """Initialize Chrome browser with vulnona map"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--new-window")
            chrome_options.add_argument("--start-maximized")
            
            # Try to start Chrome with bundled ChromeDriver
            chromedriver_path = "chromedriver.exe"
            
            # Check if bundled ChromeDriver exists
            if os.path.exists(chromedriver_path):
                print("[INFO] Using bundled ChromeDriver")
                service = Service(chromedriver_path)
            else:
                print("[INFO] Using WebDriver-Manager fallback")
                service = Service(ChromeDriverManager().install())
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.get(self.vulnova_url)
            
            print("[OK] Browser opened successfully!")
            print("[WAIT] Waiting 5 seconds for page to load...")
            time.sleep(5)
            
            # Select Gateway v0.20 map
            print("[MAP] Selecting Gateway v0.20 map...")
            try:
                # First try to click the label (this is often the correct way for radio buttons)
                gateway_label = self.driver.find_element(By.CSS_SELECTOR, "label[for='map_list_Gateway_v0.20']")
                self.driver.execute_script("arguments[0].click();", gateway_label)
                print("[OK] Gateway v0.20 label clicked via JavaScript")
                time.sleep(3)
                
                # Check if the radio button is now selected
                gateway_radio = self.driver.find_element(By.ID, "map_list_Gateway_v0.20")
                if gateway_radio.is_selected():
                    print("[OK] Gateway v0.20 is now selected!")
                else:
                    print("[WARNING] Gateway v0.20 not selected, trying radio button directly...")
                    self.driver.execute_script("arguments[0].checked = true;", gateway_radio)
                    self.driver.execute_script("arguments[0].click();", gateway_radio)
                
                time.sleep(2)
            except Exception as e:
                print(f"[WARNING] Could not select Gateway map: {e}")
            
            # Close the readme/info popup
            print("[CLOSE] Closing info popup...")
            try:
                close_button = self.driver.find_element(By.ID, "readme_close")
                close_button.click()
                print("[OK] Info popup closed")
                time.sleep(2)
            except Exception as e:
                print(f"[WARNING] Could not close popup: {e}")
            
            print("[OK] Vulnona map ready for coordinates!")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to setup browser: {e}")
            print("[INFO] Make sure ChromeDriver is installed")
            return False
    
    def parse_coordinates(self, text):
        """Extract raw Isle coordinates from clipboard text"""
        print(f"[DEBUG] Parsing clipboard text: '{text}'")
        
        # Skip if coordinates are 0.0, 0.0 (invalid)
        if "0.0, 0.0" in text or "0,0" in text:
            print("[DEBUG] Skipping 0,0 coordinates")
            return None
        
        # Look for Isle coordinate pattern: 88,879.526, -288,696.11, 21,112.882
        # This is the raw format that vulnova.com can process directly
        pattern = r'(-?\d+,\d+\.?\d*)\s*,\s*(-?\d+,\d+\.?\d*)\s*,\s*(-?\d+,\d+\.?\d*)'
        
        match = re.search(pattern, text)
        if match:
            # Return the raw coordinate string that vulnova can process
            raw_coords = f"{match.group(1)}, {match.group(2)}, {match.group(3)}"
            print(f"[DEBUG] Isle coordinates found: {raw_coords}")
            return raw_coords
        
        print("[DEBUG] No valid Isle coordinates found")
        return None
    
    def is_the_isle_running(self):
        """Check if The Isle game is currently running"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and 'isle' in proc.info['name'].lower():
                    return True
            return False
        except Exception:
            return False
    
    def get_test_coordinates(self):
        """Get next test coordinates for demo purposes"""
        coords = self.test_coordinates[self.test_index]
        self.test_index = (self.test_index + 1) % len(self.test_coordinates)
        return coords
    
    def update_map_position(self, raw_coordinates):
        """Update position on vulnova map with raw Isle coordinates"""
        try:
            # Find the coordinate input field
            coordinate_input = self.driver.find_element(By.ID, "current_pos")
            
            # Clear and enter raw coordinates (vulnova.com handles the format directly)
            coordinate_input.clear()
            coordinate_input.send_keys(raw_coordinates)
            
            # Find and click the submit button
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Show']")
            submit_button.click()
            
            print(f"[MAP] Updated position: {raw_coordinates}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to update map: {e}")
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
                    raw_coords = self.parse_coordinates(current_clipboard)
                    
                    if raw_coords is not None:
                        msg = f"[FOUND] Isle coordinates: {raw_coords}"
                        print(msg)
                        self.log_to_gui(msg)
                        
                        if self.driver:
                            success = self.update_map_position(raw_coords)
                            if success:
                                success_msg = "[OK] Map updated successfully!"
                                print(success_msg)
                                self.log_to_gui(success_msg)
                            else:
                                error_msg = "[WARNING] Map update failed"
                                print(error_msg)
                                self.log_to_gui(error_msg)
                        
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
    
    def create_gui(self):
        """Create simple GUI with close button"""
        self.gui = tk.Tk()
        self.gui.title("Isle Map Updater")
        self.gui.geometry("400x300")
        self.gui.resizable(False, False)
        
        # Status display
        status_frame = tk.Frame(self.gui)
        status_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        tk.Label(status_frame, text="Isle Map Updater", font=("Arial", 16, "bold")).pack()
        tk.Label(status_frame, text="Monitoring clipboard for coordinates...").pack(pady=5)
        
        # Status text area
        self.status_text = tk.Text(status_frame, height=10, width=45, font=("Consolas", 9))
        self.status_text.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.gui)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Stop & Close", command=self.stop_gui, 
                 bg="#ff6b6b", fg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Center window
        self.gui.update_idletasks()
        width = self.gui.winfo_width()
        height = self.gui.winfo_height()
        x = (self.gui.winfo_screenwidth() // 2) - (width // 2)
        y = (self.gui.winfo_screenheight() // 2) - (height // 2)
        self.gui.geometry(f"{width}x{height}+{x}+{y}")
        
        # Handle window close
        self.gui.protocol("WM_DELETE_WINDOW", self.stop_gui)
    
    def log_to_gui(self, message):
        """Add message to GUI status"""
        if self.status_text:
            self.status_text.insert(tk.END, message + "\n")
            self.status_text.see(tk.END)
            self.gui.update_idletasks()
    
    def stop_gui(self):
        """Stop everything and close GUI"""
        self.running = False
        if self.gui:
            self.gui.destroy()
        self.stop()
    
    def start(self):
        """Start the map updater with GUI"""
        # Create GUI first
        self.create_gui()
        
        # Start browser setup in background
        def setup_and_monitor():
            self.log_to_gui("Isle Map Updater Starting...")
            self.log_to_gui("Setting up browser...")
            
            if not self.setup_browser():
                self.log_to_gui("ERROR: Failed to setup browser!")
                return
            
            self.log_to_gui("Browser ready! Monitoring clipboard...")
            self.running = True
            self.monitor_clipboard()
        
        # Start monitoring in background thread
        monitor_thread = threading.Thread(target=setup_and_monitor, daemon=True)
        monitor_thread.start()
        
        # Start GUI (blocks until closed)
        try:
            self.gui.mainloop()
        except Exception as e:
            print(f"GUI error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the map updater"""
        self.running = False
        
        # Proper cleanup of browser resources
        if self.driver:
            try:
                self.driver.close()  # Close current window
                self.driver.quit()   # Quit entire browser session
            except Exception as e:
                print(f"Error closing browser: {e}")
                # Force kill chrome processes if needed
                try:
                    import subprocess
                    subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], capture_output=True)
                    subprocess.run(['taskkill', '/f', '/im', 'chromedriver.exe'], capture_output=True)
                except Exception:
                    pass
            finally:
                self.driver = None
        
        print("Isle Map Updater stopped")


def main():
    """Main entry point"""
    updater = IsleMapUpdater()
    
    try:
        updater.start()
    except KeyboardInterrupt:
        print("\n[STOP] Interrupted by user")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    finally:
        # Ensure cleanup always happens
        try:
            updater.stop()
        except Exception as cleanup_error:
            print(f"Cleanup error: {cleanup_error}")
        
        # Force exit to prevent hanging
        import sys
        import os
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    main()