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
        
        # Try Legacy format first: (Lat: xxx,xxx.xxx Long: yyy,yyy.yyy Alt: zzz,zzz.zzz)
        legacy_coords = self._parse_legacy_format(text)
        if legacy_coords:
            return legacy_coords
        
        # Try Evrima format: xxx,xxx.xxx, yyy,yyy.yyy, zzz,zzz.zzz
        evrima_coords = self._parse_evrima_format(text)
        if evrima_coords:
            return evrima_coords
        
        return None
    
    def _create_number_pattern(self):
        """Create regex pattern for a number with various separator formats"""
        # Support different separator patterns:
        # comma-dot: xxx,xxx.xxx
        # dot-comma: xxx.xxx,xxx  
        # space-dot: xxx xxx.xxx
        # space-comma: xxx xxx,xxx
        # apostrophe-comma: xxx'xxx,xxx
        # Also support 1-2-3 digit grouping: x,xx,xxx.xxx
        # Also support numbers without separators: xxxxx.xxx
        
        # Different minus signs: hyphen (-) and minus (−)
        minus_signs = r"[-−]"
        
        # Different separators for thousands
        thousands_seps = r"[,.\s']"  # comma, dot, space, apostrophe
        
        # Different decimal separators
        decimal_seps = r"[,.]"       # comma or dot for decimals
        
        # Pattern for various number formats - more flexible matching
        number_pattern = (
            r"" + minus_signs + r"?"                    # optional minus sign (hyphen or minus)
            r"(?:"                                      # start group for number formats
            r"\d{1,3}(?:" + thousands_seps + r"\d{1,3})*"  # digit groups with separators (1-3 per group)
            r"(?:" + decimal_seps + r"\d{1,6})?"        # optional decimal part
            r"|"                                        # OR
            r"\d{1,6}(?:" + decimal_seps + r"\d{1,6})?" # simple number with optional decimal
            r")"                                        # end group
        )
        
        return number_pattern
    
    def _parse_legacy_format(self, text):
        """Parse Legacy format: (Lat: xxx,xxx.xxx Long: yyy,yyy.yyy Alt: zzz,zzz.zzz)"""
        number_pattern = self._create_number_pattern()
        
        # Legacy pattern with keywords
        legacy_pattern = (
            r"(?:Lat|LAT):\s*(" + number_pattern + r")\s+"
            r"(?:Long|LONG):\s*(" + number_pattern + r")\s+"
            r"(?:Alt|ALT):\s*(" + number_pattern + r")"
        )
        
        match = re.search(legacy_pattern, text, re.IGNORECASE)
        if match:
            lat, lon, alt = match.groups()
            
            # Special check for Legacy format: reject zero coordinates
            if (re.match(r'^0+\.?0*$', lat.replace(' ', '').replace(',', '').replace("'", '')) and
                re.match(r'^0+\.?0*$', lon.replace(' ', '').replace(',', '').replace("'", '')) and
                re.match(r'^0+\.?0*$', alt.replace(' ', '').replace(',', '').replace("'", ''))):
                print("[DEBUG] Skipping Legacy zero coordinates")
                return None
            
            # Normalize to comma-dot format for vulnova
            normalized_coords = self._normalize_coordinates(lat, lon, alt)
            print(f"[DEBUG] Legacy coordinates found: {normalized_coords}")
            return normalized_coords
        
        return None
    
    def _parse_evrima_format(self, text):
        """Parse Evrima format: xxx,xxx.xxx, yyy,yyy.yyy, zzz,zzz.zzz"""
        number_pattern = self._create_number_pattern()
        
        # Evrima pattern - three numbers separated by commas and optional spaces
        # More precise pattern to avoid partial matches
        evrima_pattern = (
            r"(?:^|[^.\d])"  # Start of string or non-digit/non-dot character
            r"(" + number_pattern + r")\s*,\s*"
            r"(" + number_pattern + r")\s*,\s*"
            r"(" + number_pattern + r")"
            r"(?:[^.\d]|$)"  # End of string or non-digit/non-dot character
        )
        
        # First try with boundaries
        match = re.search(evrima_pattern, text)
        if not match:
            # Fallback to simpler pattern for cases where boundary detection fails
            simple_pattern = (
                r"(" + number_pattern + r")\s*,\s*"
                r"(" + number_pattern + r")\s*,\s*"
                r"(" + number_pattern + r")"
            )
            match = re.search(simple_pattern, text)
        
        if match:
            x, y, z = match.groups()
            
            # Special check for Evrima format: only reject if it's specifically "0.0, 0.0" pattern (short invalid coordinates)
            if (("0.0, 0.0" in text and len(text.strip()) < 20) or 
                (text.strip() == "0,0")):
                print("[DEBUG] Skipping 0,0 coordinates")
                return None
            
            # Normalize to comma-dot format for vulnova
            normalized_coords = self._normalize_coordinates(x, y, z)
            print(f"[DEBUG] Evrima coordinates found: {normalized_coords}")
            return normalized_coords
        
        return None
    
    def _normalize_coordinates(self, x, y, z):
        """Normalize coordinates to vulnova-compatible format (comma-dot)"""
        def normalize_number(num_str):
            # Remove all separators except the last decimal separator
            # Convert various formats to standard comma-dot format
            
            # Clean the string first
            clean_str = num_str.strip()
            
            # Handle different minus signs (hyphen - and minus −)
            is_negative = clean_str.startswith('-') or clean_str.startswith('−')
            if is_negative:
                clean_str = clean_str[1:]
            
            # Handle different decimal separators
            if '.' in clean_str and ',' in clean_str:
                # Determine which is the decimal separator (rightmost)
                last_dot = clean_str.rfind('.')
                last_comma = clean_str.rfind(',')
                
                if last_dot > last_comma:
                    # Dot is decimal separator, comma is thousands
                    parts = clean_str.split('.')
                    integer_part = parts[0].replace(',', '').replace(' ', '').replace("'", '')
                    decimal_part = parts[1] if len(parts) > 1 else ''
                    # Format as comma-dot for vulnova
                    if len(integer_part) > 3:
                        # Handle different digit groupings
                        if len(integer_part) == 4:
                            formatted_int = f"{integer_part[0]},{integer_part[1:]}"
                        elif len(integer_part) == 5:
                            formatted_int = f"{integer_part[:2]},{integer_part[2:]}"
                        elif len(integer_part) == 6:
                            formatted_int = f"{integer_part[:3]},{integer_part[3:]}"
                        else:
                            formatted_int = f"{integer_part[:-3]},{integer_part[-3:]}"
                    else:
                        formatted_int = integer_part
                    result = f"{formatted_int}.{decimal_part}" if decimal_part else formatted_int
                else:
                    # Comma is decimal separator, dot is thousands
                    parts = clean_str.split(',')
                    integer_part = parts[0].replace('.', '').replace(' ', '').replace("'", '')
                    decimal_part = parts[1] if len(parts) > 1 else ''
                    # Format as comma-dot for vulnova
                    if len(integer_part) > 3:
                        # Handle different digit groupings
                        if len(integer_part) == 4:
                            formatted_int = f"{integer_part[0]},{integer_part[1:]}"
                        elif len(integer_part) == 5:
                            formatted_int = f"{integer_part[:2]},{integer_part[2:]}"
                        elif len(integer_part) == 6:
                            formatted_int = f"{integer_part[:3]},{integer_part[3:]}"
                        else:
                            formatted_int = f"{integer_part[:-3]},{integer_part[-3:]}"
                    else:
                        formatted_int = integer_part
                    result = f"{formatted_int}.{decimal_part}" if decimal_part else formatted_int
            
            # Single separator type
            elif ',' in clean_str:
                # Could be thousands separator or decimal
                comma_parts = clean_str.split(',')
                
                # Check if last part after comma looks like decimal (1-3 digits)
                if len(comma_parts) == 2 and len(comma_parts[1]) <= 3 and comma_parts[1].isdigit() and len(comma_parts[1]) > 0:
                    # Likely decimal comma, convert to dot
                    integer_part = comma_parts[0].replace(' ', '').replace("'", '')
                    decimal_part = comma_parts[1]
                    if len(integer_part) > 3:
                        # Handle different digit groupings
                        if len(integer_part) == 4:
                            formatted_int = f"{integer_part[0]},{integer_part[1:]}"
                        elif len(integer_part) == 5:
                            formatted_int = f"{integer_part[:2]},{integer_part[2:]}"
                        elif len(integer_part) == 6:
                            formatted_int = f"{integer_part[:3]},{integer_part[3:]}"
                        else:
                            formatted_int = f"{integer_part[:-3]},{integer_part[-3:]}"
                    else:
                        formatted_int = integer_part
                    result = f"{formatted_int}.{decimal_part}"
                else:
                    # Thousands separator or multiple comma separators
                    clean_num = clean_str.replace(' ', '').replace("'", '')
                    # Just return as-is for comma-separated thousands
                    result = clean_num
            
            elif '.' in clean_str:
                dot_parts = clean_str.split('.')
                
                # Check if last part after dot looks like decimal (1-6 digits)
                if len(dot_parts) == 2 and len(dot_parts[1]) <= 6 and dot_parts[1].isdigit():
                    # Decimal dot
                    integer_part = dot_parts[0].replace(' ', '').replace("'", '')
                    decimal_part = dot_parts[1]
                    if len(integer_part) > 3:
                        # Handle different digit groupings
                        if len(integer_part) == 4:
                            formatted_int = f"{integer_part[0]},{integer_part[1:]}"
                        elif len(integer_part) == 5:
                            formatted_int = f"{integer_part[:2]},{integer_part[2:]}"
                        elif len(integer_part) == 6:
                            formatted_int = f"{integer_part[:3]},{integer_part[3:]}"
                        else:
                            formatted_int = f"{integer_part[:-3]},{integer_part[-3:]}"
                    else:
                        formatted_int = integer_part
                    result = f"{formatted_int}.{decimal_part}"
                else:
                    # Thousands separator, convert to comma
                    clean_num = clean_str.replace('.', '').replace(' ', '').replace("'", '')
                    if len(clean_num) > 3:
                        # Handle different digit groupings
                        if len(clean_num) == 4:
                            result = f"{clean_num[0]},{clean_num[1:]}"
                        elif len(clean_num) == 5:
                            result = f"{clean_num[:2]},{clean_num[2:]}"
                        elif len(clean_num) == 6:
                            result = f"{clean_num[:3]},{clean_num[3:]}"
                        else:
                            result = f"{clean_num[:-3]},{clean_num[-3:]}"
                    else:
                        result = clean_num
            
            else:
                # No separators, just clean spaces and apostrophes
                clean_num = clean_str.replace(' ', '').replace("'", '')
                
                # Handle decimal numbers without thousands separators
                if '.' in clean_num:
                    parts = clean_num.split('.')
                    integer_part = parts[0]
                    decimal_part = parts[1]
                    
                    if len(integer_part) > 3:
                        # Handle different digit groupings
                        if len(integer_part) == 4:
                            formatted_int = f"{integer_part[0]},{integer_part[1:]}"
                        elif len(integer_part) == 5:
                            formatted_int = f"{integer_part[:2]},{integer_part[2:]}"
                        elif len(integer_part) == 6:
                            formatted_int = f"{integer_part[:3]},{integer_part[3:]}"
                        else:
                            formatted_int = f"{integer_part[:-3]},{integer_part[-3:]}"
                        result = f"{formatted_int}.{decimal_part}"
                    else:
                        result = clean_num
                else:
                    # Integer without decimal
                    if len(clean_num) > 3:
                        # Handle different digit groupings
                        if len(clean_num) == 4:
                            result = f"{clean_num[0]},{clean_num[1:]}"
                        elif len(clean_num) == 5:
                            result = f"{clean_num[:2]},{clean_num[2:]}"
                        elif len(clean_num) == 6:
                            result = f"{clean_num[:3]},{clean_num[3:]}"
                        else:
                            result = f"{clean_num[:-3]},{clean_num[-3:]}"
                    else:
                        result = clean_num
            
            # Add back negative sign if needed
            if is_negative:
                result = '-' + result
                
            return result
        
        # Normalize each coordinate component
        norm_x = normalize_number(x)
        norm_y = normalize_number(y)
        norm_z = normalize_number(z)
        
        return f"{norm_x}, {norm_y}, {norm_z}"
    
    def get_test_coordinates(self):
        """Get next test coordinates for demo purposes"""
        coords = self.test_coordinates[self.test_index]
        self.test_index = (self.test_index + 1) % len(self.test_coordinates)
        return coords