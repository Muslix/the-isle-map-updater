"""
Browser management for Isle Map Updater
Handles Chrome/Selenium operations and vulnona.com interaction
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class BrowserManager:
    def __init__(self):
        self.driver = None
        self.vulnova_url = "https://vulnona.com/game/map/"
        self.available_maps = []
    
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
            
            print("[BROWSER] Starting Chrome with ChromeDriver...")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            print(f"[BROWSER] Navigating to: {self.vulnova_url}")
            self.driver.get(self.vulnova_url)
            
            print("[OK] Browser opened successfully!")
            print("[WAIT] Waiting 10 seconds for page to fully load...")
            time.sleep(10)
            
            # Wait for the page to be fully interactive
            print("[DEBUG] Checking for map selection elements...")
            try:
                # First check if the page loaded at all
                print(f"[DEBUG] Current page title: {self.driver.title}")
                print(f"[DEBUG] Current URL: {self.driver.current_url}")
                
                # Try different selectors to see what exists
                print("[DEBUG] Searching for map radio buttons...")
                
                # Try the new selector first
                map_radios_new = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio'][name='map_list']")
                print(f"[DEBUG] Found {len(map_radios_new)} elements with name='map_list'")
                
                # Try the old selector as fallback
                map_radios_old = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio'][name='map']")
                print(f"[DEBUG] Found {len(map_radios_old)} elements with name='map'")
                
                # Try to find any radio buttons
                all_radios = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
                print(f"[DEBUG] Found {len(all_radios)} total radio buttons")
                
                if map_radios_new:
                    print("[OK] Map selection elements found with map_list!")
                elif map_radios_old:
                    print("[OK] Map selection elements found with map!")
                elif all_radios:
                    print("[WARNING] Found radio buttons but not map selectors")
                    for i, radio in enumerate(all_radios[:5]):  # Show first 5
                        name = radio.get_attribute('name')
                        value = radio.get_attribute('value')
                        print(f"[DEBUG] Radio {i}: name='{name}', value='{value}'")
                else:
                    print("[ERROR] No radio buttons found at all!")
                    # Let's see what's actually on the page
                    page_source_snippet = self.driver.page_source[:1000]
                    print(f"[DEBUG] Page source snippet: {page_source_snippet}")
                    return False
                    
            except Exception as e:
                print(f"[ERROR] Failed to check map elements: {e}")
                return False
            
            # Close the readme/info popup if it exists
            print("[CLOSE] Closing info popup...")
            try:
                close_button = self.driver.find_element(By.ID, "readme_close")
                close_button.click()
                print("[OK] Info popup closed")
                time.sleep(2)
            except Exception as e:
                print(f"[INFO] No popup to close: {e}")
            
            print("[OK] Vulnova map ready for coordinates!")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to setup browser: {e}")
            print("[INFO] Make sure ChromeDriver is installed")
            return False
    
    def get_available_maps(self):
        """Get available maps from vulnona.com"""
        if not self.driver:
            print("[ERROR] Browser not initialized")
            return []
        
        try:
            print("[MAP] Detecting available maps...")
            
            # Look for map selection radio buttons - try different selectors
            print("[MAP] Trying different selectors...")
            
            map_radios = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio'][name='map_list']")
            if not map_radios:
                print("[MAP] No map_list elements found, trying name='map'...")
                map_radios = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio'][name='map']")
            
            if not map_radios:
                print("[MAP] No map radio buttons found, trying any radio...")
                map_radios = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
                print(f"[MAP] Found {len(map_radios)} total radio buttons")
            
            print(f"[MAP] Processing {len(map_radios)} radio buttons...")
            maps = []
            
            for radio in map_radios:
                try:
                    # Get the map details
                    map_value = radio.get_attribute('value')
                    map_id = radio.get_attribute('id')
                    
                    print(f"[DEBUG] Processing radio: id='{map_id}', value='{map_value}'")
                    
                    if not map_value or not map_id:
                        print(f"[DEBUG] Skipping radio with missing id or value")
                        continue
                    
                    # Find associated label for display text and game info
                    try:
                        label = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{map_id}']")
                        
                        # Debug: show full label text
                        full_label_text = label.text.strip()
                        print(f"[DEBUG] Full label text for {map_id}: '{full_label_text}'")
                        
                        # Try different ways to get the map name
                        label_text = ""
                        if full_label_text:
                            label_lines = full_label_text.split('\\n')
                            label_text = label_lines[0].strip() if label_lines else ""
                        
                        # If still empty, try getting from value or id
                        if not label_text:
                            label_text = map_value or map_id.replace('map_list_', '') if map_id else "Unknown Map"
                        
                        print(f"[DEBUG] Extracted map name: '{label_text}'")
                        
                        # Get game type from icon
                        game_type = "Unknown"
                        status = "Unknown"
                        status_text = ""
                        
                        try:
                            # Get game icon info
                            game_icon = label.find_element(By.CSS_SELECTOR, "img.game_icon")
                            game_icon_src = game_icon.get_attribute('src')
                            print(f"[DEBUG] Game icon src: {game_icon_src}")
                            
                            if "TI_icon.png" in game_icon_src:
                                game_type = "The Isle"
                            elif "PoT_icon.png" in game_icon_src:
                                game_type = "Path of Titans"
                        except Exception as icon_error:
                            print(f"[DEBUG] Could not get game icon: {icon_error}")
                        
                        try:
                            # Get status indicator (✅, ❌, ⚠️)
                            middle_div = label.find_element(By.CSS_SELECTOR, "div.middle")
                            status_text = middle_div.text.strip()
                            print(f"[DEBUG] Status text: '{status_text}'")
                            
                            if status_text.startswith("✅"):
                                status = "Active"
                            elif status_text.startswith("❌"):
                                status = "Outdated"
                            elif status_text.startswith("⚠️"):
                                status = "Legacy"
                        except Exception as status_error:
                            print(f"[DEBUG] Could not get status: {status_error}")
                        
                        # Create display name with game and status
                        if label_text:
                            display_name = f"{label_text} [{game_type}] ({status})"
                        else:
                            display_name = f"{map_value} [{game_type}] ({status})"
                        
                        maps.append({
                            'value': map_value,
                            'label': display_name,
                            'raw_name': label_text,
                            'game_type': game_type,
                            'status': status,
                            'status_text': status_text,
                            'element': radio
                        })
                        print(f"[MAP] Added: {display_name}")
                    
                    except Exception as label_error:
                        print(f"[DEBUG] Label parsing failed: {label_error}")
                        # Fallback to just the value
                        fallback_name = map_value or map_id.replace('map_list_', '') if map_id else "Unknown Map"
                        maps.append({
                            'value': map_value,
                            'label': fallback_name,
                            'raw_name': fallback_name,
                            'game_type': "Unknown",
                            'status': "Unknown",
                            'status_text': "",
                            'element': radio
                        })
                        print(f"[MAP] Added (fallback): {fallback_name}")
                
                except Exception as e:
                    print(f"[WARNING] Error processing map radio: {e}")
            
            self.available_maps = maps
            print(f"[MAP] Total maps found: {len(maps)}")
            return maps
            
        except Exception as e:
            print(f"[ERROR] Failed to get available maps: {e}")
            return []
    
    def select_map(self, map_value):
        """Select a specific map on vulnona.com"""
        if not self.driver:
            print("[ERROR] Browser not initialized")
            return False
        
        try:
            print(f"[MAP] Selecting map: {map_value}")
            
            # Find and click the radio button for this map - try different selectors
            radio = None
            try:
                radio = self.driver.find_element(By.CSS_SELECTOR, f"input[type='radio'][name='map_list'][value='{map_value}']")
                print(f"[MAP] Found radio with map_list selector")
            except:
                try:
                    radio = self.driver.find_element(By.CSS_SELECTOR, f"input[type='radio'][name='map'][value='{map_value}']")
                    print(f"[MAP] Found radio with map selector")
                except:
                    print(f"[ERROR] Could not find radio button for map: {map_value}")
                    return False
            
            if not radio.is_selected():
                # Try clicking the label instead (often more reliable)
                map_id = radio.get_attribute('id')
                try:
                    label = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{map_id}']")
                    self.driver.execute_script("arguments[0].click();", label)
                    print(f"[OK] Clicked label for map: {map_value}")
                except:
                    # Fallback to radio button
                    self.driver.execute_script("arguments[0].checked = true;", radio)
                    self.driver.execute_script("arguments[0].click();", radio)
                    print(f"[OK] Clicked radio for map: {map_value}")
                
                time.sleep(3)  # Wait for map to load
                
                # Check if selection worked
                if radio.is_selected():
                    print(f"[OK] Successfully selected map: {map_value}")
                    return True
                else:
                    print(f"[WARNING] Map selection may have failed")
                    # Still return true since the click went through
                    return True
            else:
                print(f"[OK] Map {map_value} already selected")
                return True
                
        except Exception as e:
            print(f"[ERROR] Failed to select map {map_value}: {e}")
            return False
    
    def update_map_position(self, raw_coordinates):
        """Update position on vulnona map with raw Isle coordinates"""
        try:
            # Find the coordinate input field
            coordinate_input = self.driver.find_element(By.ID, "current_pos")
            
            # Clear and enter raw coordinates (vulnona.com handles the format directly)
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
    
    def stop(self):
        """Stop the browser"""
        if self.driver:
            try:
                print("[BROWSER] Closing browser...")
                self.driver.quit()
                self.driver = None
                print("[OK] Browser closed successfully")
            except Exception as e:
                print(f"[WARNING] Error closing browser: {e}")