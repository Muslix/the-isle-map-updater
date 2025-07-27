"""
Coordinate parsing for Isle Map Updater
Handles extraction and validation of coordinates from clipboard
"""

import re


class CoordinateParser:
    def __init__(self):
        self.test_coordinates = [
            "88,879.526, -288,696.11, 21,112.882",
            "89,123.456, -289,123.45, 22,456.789",
            "87,654.321, -287,987.65, 20,789.123",
            "90,111.222, -290,333.44, 23,555.666",
            "86,999.888, -286,777.99, 19,444.333"
        ]
        self.test_index = 0
    
    def parse_coordinates(self, text):
        """Extract raw Isle coordinates from clipboard text"""
        # Skip debug output and other non-coordinate text
        if any(keyword in text for keyword in ['[DEBUG]', '[MAP]', '[OK]', '[ERROR]', '[WARNING]', '[INFO]', 'DevTools listening', 'USB:', 'WARNING:', 'Created TensorFlow']):
            return None
        
        # Skip if text is too long (likely debug output)
        if len(text) > 200:
            return None
        
        print(f"[DEBUG] Parsing clipboard text: '{text[:50]}...'")
        
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
        
        return None
    
    def get_test_coordinates(self):
        """Get next test coordinates for demo purposes"""
        coords = self.test_coordinates[self.test_index]
        self.test_index = (self.test_index + 1) % len(self.test_coordinates)
        return coords