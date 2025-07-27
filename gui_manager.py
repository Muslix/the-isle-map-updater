"""
GUI management for Isle Map Updater
Handles the tkinter interface and user interactions
"""

import tkinter as tk
from tkinter import ttk
import threading


class GUIManager:
    def __init__(self, app_instance):
        self.app = app_instance  # Reference to main app
        self.gui = None
        self.status_text = None
        self.map_var = None
        self.map_dropdown = None
        self.save_map_button = None
        self.setup_button = None
        self.refresh_button = None
    
    def create_gui(self):
        """Create GUI with map selection and monitoring"""
        self.gui = tk.Tk()
        self.gui.title("Isle Map Updater")
        self.gui.geometry("500x400")
        self.gui.resizable(False, False)
        
        # Header
        header_frame = tk.Frame(self.gui)
        header_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(header_frame, text="Isle Map Updater", font=("Arial", 16, "bold")).pack()
        tk.Label(header_frame, text="Select your map and monitor coordinates", font=("Arial", 10)).pack(pady=2)
        
        # Map selection frame
        map_frame = tk.Frame(self.gui)
        map_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(map_frame, text="Selected Map:", font=("Arial", 11, "bold")).pack(anchor=tk.W)
        
        # Map dropdown and save button on same line
        dropdown_frame = tk.Frame(map_frame)
        dropdown_frame.pack(pady=5, fill=tk.X)
        
        self.map_var = tk.StringVar()
        self.map_dropdown = ttk.Combobox(dropdown_frame, textvariable=self.map_var, state="readonly", width=45)
        self.map_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.map_dropdown.set("Load browser first to see available maps...")
        self.map_dropdown.bind('<<ComboboxSelected>>', self.on_map_selected)
        
        self.save_map_button = tk.Button(dropdown_frame, text="Save as Default", command=self.save_current_map,
                                       bg="#4CAF50", fg="white", font=("Arial", 10), state=tk.DISABLED)
        self.save_map_button.pack(side=tk.RIGHT)
        
        # Setup button
        setup_frame = tk.Frame(self.gui)
        setup_frame.pack(pady=5, padx=10, fill=tk.X)
        
        self.setup_button = tk.Button(setup_frame, text="Setup Browser & Load Maps", command=self.setup_browser_gui,
                                    bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
        self.setup_button.pack(side=tk.LEFT, padx=5)
        
        self.refresh_button = tk.Button(setup_frame, text="Refresh Maps", command=self.refresh_maps_gui,
                                       bg="#2196F3", fg="white", font=("Arial", 11), state=tk.DISABLED)
        self.refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Status display
        status_frame = tk.Frame(self.gui)
        status_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        tk.Label(status_frame, text="Status:", font=("Arial", 11, "bold")).pack(anchor=tk.W)
        
        # Status text area
        self.status_text = tk.Text(status_frame, height=12, width=55, font=("Consolas", 9))
        self.status_text.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # Control buttons
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
        
        # Initialize map dropdown if we have saved config
        if self.app.config_manager.get_selected_map():
            self.log_to_gui(f"Saved map: {self.app.config_manager.get_selected_map()}")
    
    def setup_browser_gui(self):
        """Setup browser from GUI button"""
        self.setup_button.config(state=tk.DISABLED, text="Setting up...")
        self.log_to_gui("Setting up browser...")
        
        def setup_thread():
            try:
                self.log_to_gui("Opening Chrome browser...")
                self.log_to_gui(f"Loading: {self.app.browser_manager.vulnova_url}")
                
                success = self.app.browser_manager.setup_browser()
                if success:
                    self.log_to_gui("✅ Browser opened successfully!")
                    self.log_to_gui("🔍 Scanning available maps...")
                    
                    # Now load the maps
                    maps = self.app.browser_manager.get_available_maps()
                    if maps:
                        self.update_map_dropdown()
                        self.log_to_gui(f"✅ Found {len(maps)} available maps!")
                        self.save_map_button.config(state=tk.NORMAL)
                        
                        # Try to restore saved map
                        if self.app.config_manager.get_selected_map():
                            self.log_to_gui(f"🔄 Restoring saved map: {self.app.config_manager.get_selected_map()}")
                            self.apply_saved_map()
                    else:
                        self.log_to_gui("❌ No maps found!")
                    
                    self.refresh_button.config(state=tk.NORMAL)
                    self.setup_button.config(text="Browser Ready", bg="#45a049")
                else:
                    self.log_to_gui("❌ Browser setup failed!")
                    self.log_to_gui("Check if Chrome is installed and ChromeDriver is working")
                    self.setup_button.config(state=tk.NORMAL, text="Retry Setup")
            except Exception as e:
                self.log_to_gui(f"❌ Setup error: {str(e)}")
                self.setup_button.config(state=tk.NORMAL, text="Retry Setup")
        
        threading.Thread(target=setup_thread, daemon=True).start()
    
    def refresh_maps_gui(self):
        """Refresh available maps from GUI button"""
        self.refresh_button.config(state=tk.DISABLED, text="Refreshing...")
        self.log_to_gui("Refreshing available maps...")
        
        def refresh_thread():
            self.app.browser_manager.get_available_maps()
            self.update_map_dropdown()
            self.log_to_gui("Maps refreshed!")
            self.refresh_button.config(state=tk.NORMAL, text="Refresh Maps")
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def update_map_dropdown(self):
        """Update the map dropdown with available maps"""
        available_maps = self.app.browser_manager.available_maps
        
        if not available_maps:
            self.map_dropdown['values'] = ["No maps available"]
            self.map_dropdown.set("No maps available")
            return
        
        # Show all maps (no filtering)
        all_maps = available_maps
        
        # Create list of map labels for dropdown
        map_labels = [f"{map_info['label']}" for map_info in all_maps]
        self.map_dropdown['values'] = map_labels
        
        # Set current selection if we have a saved map
        current_selection = None
        selected_map = self.app.config_manager.get_selected_map()
        if selected_map:
            for i, map_info in enumerate(all_maps):
                if map_info['value'] == selected_map:
                    current_selection = map_labels[i]
                    break
        
        if current_selection:
            self.map_dropdown.set(current_selection)
        else:
            self.map_dropdown.set("Select a map...")
        
        # Store maps for functions (no filtering)
        self.filtered_maps = all_maps
    
    def on_map_selected(self, event):
        """Handle map selection from dropdown - auto-select immediately"""
        selected_label = self.map_var.get()
        if not selected_label or selected_label in ["No maps available", "Load browser first to see available maps..."]:
            return
        
        # Find the map value from the label
        selected_map_value = None
        maps_to_search = getattr(self, 'filtered_maps', self.app.browser_manager.available_maps)
        for map_info in maps_to_search:
            if map_info['label'] == selected_label:
                selected_map_value = map_info['value']
                break
        
        if selected_map_value:
            self.log_to_gui(f"🗺️ Switching to: {selected_label}")
            
            def select_thread():
                success = self.app.browser_manager.select_map(selected_map_value)
                if success:
                    self.app.config_manager.set_selected_map(selected_map_value)
                    self.log_to_gui(f"✅ Map active: {selected_label}")
                    # Start monitoring if not already running
                    if not self.app.running:
                        self.app.start_monitoring()
                else:
                    self.log_to_gui(f"❌ Failed to switch to: {selected_label}")
            
            threading.Thread(target=select_thread, daemon=True).start()
    
    def save_current_map(self):
        """Save the currently selected map as default"""
        selected_map = self.app.config_manager.get_selected_map()
        if selected_map:
            self.app.config_manager.save_config()
            self.log_to_gui(f"💾 Saved '{selected_map}' as default map!")
        else:
            self.log_to_gui("No map selected to save!")
    
    def apply_saved_map(self):
        """Apply the saved map selection"""
        selected_map = self.app.config_manager.get_selected_map()
        available_maps = self.app.browser_manager.available_maps
        
        if not selected_map or not available_maps:
            print(f"[DEBUG] Cannot apply saved map: selected_map={selected_map}, available_maps={len(available_maps) if available_maps else 0}")
            return
        
        print(f"[MAP] Attempting to restore saved map: {selected_map}")
        
        # Get the filtered maps that are actually in the dropdown
        filtered_maps = getattr(self, 'filtered_maps', available_maps)
        
        # Find the saved map in the filtered list
        for i, map_info in enumerate(filtered_maps):
            if map_info['value'] == selected_map:
                print(f"[MAP] Found saved map at index {i}: {map_info['label']}")
                self.map_dropdown.current(i)
                # Auto-select this map (trigger the selection event)
                self.map_dropdown.event_generate('<<ComboboxSelected>>')
                return
        
        print(f"[WARNING] Saved map '{selected_map}' not found in available maps")
        # Show which maps are available
        print(f"[DEBUG] Available maps: {[m['value'] for m in filtered_maps]}")
    
    def log_to_gui(self, message):
        """Add message to GUI status"""
        if self.status_text:
            self.status_text.insert(tk.END, message + "\n")
            self.status_text.see(tk.END)
            self.gui.update_idletasks()
    
    def stop_gui(self):
        """Stop everything and close GUI"""
        self.app.running = False
        if self.gui:
            self.gui.destroy()
        self.app.stop()
    
    def start_mainloop(self):
        """Start the GUI main loop"""
        if self.gui:
            try:
                self.gui.mainloop()
            except Exception as e:
                print(f"GUI error: {e}")
            finally:
                self.app.stop()