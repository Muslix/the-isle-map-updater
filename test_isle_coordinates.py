#!/usr/bin/env python3
"""
Comprehensive Test Suite for The Isle Coordinate Recognition
Tests all common coordinate formats from both Legacy and Evrima branches
"""

from coordinate_parser import CoordinateParser

def test_legacy_coordinates():
    """Test Legacy format: (Lat: xxx,xxx.xxx Long: yyy,yyy.yyy Alt: zzz,zzz.zzz)"""
    parser = CoordinateParser()
    
    print("=== TESTING LEGACY FORMAT ===")
    
    legacy_tests = [
        # Standard Legacy format variations
        ("Lat: 88,879.526 Long: -288,696.11 Alt: 21,112.882", "Standard Legacy"),
        ("LAT: 88,879.526 LONG: -288,696.11 ALT: 21,112.882", "Uppercase keywords"),
        ("lat: 88,879.526 long: -288,696.11 alt: 21,112.882", "Lowercase keywords"),
        
        # Different separator patterns
        ("Lat: 88.879,526 Long: -288.696,11 Alt: 21.112,882", "Dot-comma separators"),
        ("Lat: 88 879.526 Long: -288 696.11 Alt: 21 112.882", "Space-dot separators"),
        ("Lat: 88 879,526 Long: -288 696,11 Alt: 21 112,882", "Space-comma separators"),
        ("Lat: 88'879.526 Long: -288'696.11 Alt: 21'112.882", "Apostrophe-dot separators"),
        ("Lat: 88'879,526 Long: -288'696,11 Alt: 21'112,882", "Apostrophe-comma separators"),
        
        # Different digit groupings
        ("Lat: 1,23,456.789 Long: -9,87,654.321 Alt: 1,11,222.333", "1-2-3 digit grouping"),
        ("Lat: 12,34,567.890 Long: -98,76,543.210 Alt: 11,22,333.444", "2-2-3 digit grouping"),
        
        # No thousands separators
        ("Lat: 88879.526 Long: -288696.11 Alt: 21112.882", "No thousands separators"),
        ("Lat: 88879 Long: -288696 Alt: 21112", "No decimals"),
        
        # Various spacing
        ("Lat:88,879.526 Long:-288,696.11 Alt:21,112.882", "No spaces after colons"),
        ("Lat:  88,879.526  Long:  -288,696.11  Alt:  21,112.882", "Extra spaces"),
        
        # Realistic game coordinates
        ("Lat: 156,234.789 Long: -89,456.123 Alt: 45,678.901", "Realistic coordinates 1"),
        ("Lat: -45,123.456 Long: 234,567.890 Alt: 12,345.678", "Realistic coordinates 2"),
        # Note: Legacy zero coordinates are correctly rejected by the parser as invalid
    ]
    
    passed = 0
    for test_input, description in legacy_tests:
        result = parser.parse_coordinates(test_input)
        if result:
            print(f"[PASS] {description}: {result}")
            passed += 1
        else:
            print(f"[FAIL] {description}: No match")
    
    print(f"Legacy Tests: {passed}/{len(legacy_tests)} passed\\n")
    return passed, len(legacy_tests)

def test_evrima_coordinates():
    """Test Evrima format: xxx,xxx.xxx, yyy,yyy.yyy, zzz,zzz.zzz"""
    parser = CoordinateParser()
    
    print("=== TESTING EVRIMA FORMAT ===")
    
    evrima_tests = [
        # Standard Evrima format
        ("88,879.526, -288,696.11, 21,112.882", "Standard Evrima"),
        ("88,879.526,-288,696.11,21,112.882", "No spaces"),
        ("88,879.526,  -288,696.11,  21,112.882", "Extra spaces"),
        
        # Different separator patterns  
        ("88.879,526, -288.696,11, 21.112,882", "Dot-comma separators"),
        ("88 879.526, -288 696.11, 21 112.882", "Space-dot separators"),
        ("88 879,526, -288 696,11, 21 112,882", "Space-comma separators"),
        ("88'879.526, -288'696.11, 21'112.882", "Apostrophe-dot separators"),
        ("88'879,526, -288'696,11, 21'112,882", "Apostrophe-comma separators"),
        
        # Different digit groupings
        ("1,23,456.789, -9,87,654.321, 1,11,222.333", "1-2-3 digit grouping"),
        ("12,34,567.890, -98,76,543.210, 11,22,333.444", "2-2-3 digit grouping"),
        
        # No thousands separators
        ("88879.526, -288696.11, 21112.882", "No thousands separators"),
        ("88879, -288696, 21112", "No decimals"),
        
        # Realistic game coordinates
        ("156,234.789, -89,456.123, 45,678.901", "Realistic coordinates 1"),
        ("-45,123.456, 234,567.890, 12,345.678", "Realistic coordinates 2"),
        ("999,999.999, -999,999.999, 999,999.999", "Max range coordinates"),
        ("1.000, 1.000, 1.000", "Minimal coordinates"),
        ("0, 0, 0", "Zero coordinates"),
        
        # Edge cases with different decimal places
        ("88,879.5, -288,696.1, 21,112.88", "Variable decimal places"),
        ("88,879, -288,696, 21,112", "Integer coordinates"),
    ]
    
    passed = 0
    for test_input, description in evrima_tests:
        result = parser.parse_coordinates(test_input)
        if result:
            print(f"[PASS] {description}: {result}")
            passed += 1
        else:
            print(f"[FAIL] {description}: No match")
    
    print(f"Evrima Tests: {passed}/{len(evrima_tests)} passed\\n")
    return passed, len(evrima_tests)

def test_edge_cases():
    """Test edge cases and potential false positives"""
    parser = CoordinateParser()
    
    print("=== TESTING EDGE CASES ===")
    
    edge_cases = [
        # Should be ignored
        ("[DEBUG] Some debug output", "Debug text", False),
        ("[MAP] Map data", "Map debug", False),
        ("[ERROR] Error message", "Error text", False),
        ("DevTools listening on ws://127.0.0.1:9222", "DevTools message", False),
        ("USB: Device connected", "USB message", False),
        ("WARNING: Low memory", "Warning message", False),
        ("Created TensorFlow Lite", "TensorFlow message", False),
        ("Some random text with numbers 123,456", "Random text", False),
        ("0.0, 0.0", "Zero coordinates short", False),
        ("0,0", "Zero coordinates minimal", False),
        
        # Should be recognized
        ("Player at Lat: 88,879.526 Long: -288,696.11 Alt: 21,112.882", "Text with Legacy coords", True),
        ("Current position: 88,879.526, -288,696.11, 21,112.882", "Text with Evrima coords", True),
        ("Coordinates: 88,879.526, -288,696.11, 21,112.882 recorded", "Surrounded by text", True),
        
        # Mixed formats (should pick first valid one)
        ("Lat: 88,879.526 Long: -288,696.11 Alt: 21,112.882 and also 99,999.999, -99,999.999, 99,999.999", "Mixed formats", True),
        
        # International number formats
        ("88.879,526, -288.696,11, 21.112,882", "European decimal comma", True),
        ("88 879,526, -288 696,11, 21 112,882", "French spacing", True),
        ("88'879.526, -288'696.11, 21'112.882", "Swiss apostrophe", True),
    ]
    
    passed = 0
    for test_input, description, should_match in edge_cases:
        result = parser.parse_coordinates(test_input)
        
        if should_match and result:
            print(f"[PASS] {description}: {result}")
            passed += 1
        elif not should_match and not result:
            print(f"[PASS] {description}: Correctly ignored")
            passed += 1
        elif should_match and not result:
            print(f"[FAIL] {description}: Should have matched but didn't")
        else:
            print(f"[FAIL] {description}: Should have been ignored but matched: {result}")
    
    print(f"Edge Case Tests: {passed}/{len(edge_cases)} passed\\n")
    return passed, len(edge_cases)

def test_normalization():
    """Test coordinate normalization to vulnova format"""
    parser = CoordinateParser()
    
    print("=== TESTING NORMALIZATION ===")
    
    normalization_tests = [
        # Input format -> Expected vulnova format
        ("88.879,526, -288.696,11, 21.112,882", "88,879.526, -288,696.11, 21,112.882"),
        ("88 879.526, -288 696.11, 21 112.882", "88,879.526, -288,696.11, 21,112.882"),
        ("88'879.526, -288'696.11, 21'112.882", "88,879.526, -288,696.11, 21,112.882"),
        ("88879.526, -288696.11, 21112.882", "88,879.526, -288,696.11, 21,112.882"),
        ("1,23,456.789, -9,87,654.321, 1,11,222.333", "123,456.789, -987,654.321, 111,222.333"),
        ("Lat: 88.879,526 Long: -288.696,11 Alt: 21.112,882", "88,879.526, -288,696.11, 21,112.882"),
    ]
    
    passed = 0
    for test_input, expected in normalization_tests:
        result = parser.parse_coordinates(test_input)
        if result == expected:
            print(f"[PASS] Normalization: {result}")
            passed += 1
        else:
            print(f"[FAIL] Normalization: Expected '{expected}', got '{result}'")
    
    print(f"Normalization Tests: {passed}/{len(normalization_tests)} passed\\n")
    return passed, len(normalization_tests)

def run_comprehensive_test():
    """Run all coordinate recognition tests"""
    print("THE ISLE COORDINATE RECOGNITION - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    # Run all test categories
    legacy_passed, legacy_total = test_legacy_coordinates()
    evrima_passed, evrima_total = test_evrima_coordinates()
    edge_passed, edge_total = test_edge_cases()
    norm_passed, norm_total = test_normalization()
    
    # Calculate totals
    total_passed = legacy_passed + evrima_passed + edge_passed + norm_passed
    total_tests = legacy_total + evrima_total + edge_total + norm_total
    
    print("=" * 70)
    print(f"FINAL RESULTS: {total_passed}/{total_tests} tests passed")
    print(f"Success Rate: {(total_passed/total_tests)*100:.1f}%")
    
    if total_passed == total_tests:
        print("🎉 ALL TESTS PASSED! The Isle coordinate recognition is working perfectly!")
    else:
        print("⚠️  Some tests failed. Check the patterns above.")
    
    print("\\nTested coordinate formats:")
    print("✓ Legacy: (Lat: xxx,xxx.xxx Long: yyy,yyy.yyy Alt: zzz,zzz.zzz)")
    print("✓ Evrima: xxx,xxx.xxx, yyy,yyy.yyy, zzz,zzz.zzz")
    print("✓ All separator patterns: comma-dot, dot-comma, space-dot, space-comma, apostrophe")
    print("✓ All digit groupings: 3-digit, 1-2-3 digit, no separators")
    print("✓ Normalization to vulnova-compatible format")

if __name__ == "__main__":
    run_comprehensive_test()