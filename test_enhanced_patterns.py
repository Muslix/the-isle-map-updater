#!/usr/bin/env python3
"""
Enhanced Test Suite for The Isle Coordinate Recognition
Tests new patterns: different minus signs, apostrophe separators, and various digit groupings
"""

from coordinate_parser import CoordinateParser

def test_minus_signs():
    """Test different minus sign patterns (hyphen and minus)"""
    parser = CoordinateParser()
    
    print("=== TESTING MINUS SIGNS ===")
    
    minus_tests = [
        # Hyphen minus (standard)
        ("Lat: -88,879.526 Long: -288,696.11 Alt: 21,112.882", "Hyphen minus (Legacy)"),
        ("-88,879.526, -288,696.11, 21,112.882", "Hyphen minus (Evrima)"),
        
        # Unicode minus (−)
        ("Lat: −88,879.526 Long: −288,696.11 Alt: 21,112.882", "Unicode minus (Legacy)"),
        ("−88,879.526, −288,696.11, 21,112.882", "Unicode minus (Evrima)"),
        
        # Mixed minus signs
        ("Lat: -88,879.526 Long: −288,696.11 Alt: 21,112.882", "Mixed minus signs"),
    ]
    
    passed = 0
    for test_input, description in minus_tests:
        result = parser.parse_coordinates(test_input)
        if result:
            print(f"[PASS] {description}: {result}")
            passed += 1
        else:
            print(f"[FAIL] {description}: No match")
    
    print(f"Minus Sign Tests: {passed}/{len(minus_tests)} passed\\n")
    return passed, len(minus_tests)

def test_apostrophe_separators():
    """Test apostrophe separators with different patterns"""
    parser = CoordinateParser()
    
    print("=== TESTING APOSTROPHE SEPARATORS ===")
    
    apostrophe_tests = [
        # Legacy with apostrophes
        ("Lat: 88'879.526 Long: -288'696.11 Alt: 21'112.882", "Legacy apostrophe-dot"),
        ("Lat: 88'879,526 Long: -288'696,11 Alt: 21'112,882", "Legacy apostrophe-comma"),
        
        # Evrima with apostrophes
        ("88'879.526, -288'696.11, 21'112.882", "Evrima apostrophe-dot"),
        ("88'879,526, -288'696,11, 21'112,882", "Evrima apostrophe-comma"),
        
        # Complex apostrophe patterns (1-2-3 grouping)
        ("1'23'456.789, -9'87'654.321, 1'11'222.333", "Apostrophe 1-2-3 grouping"),
        ("12'34'567.890, -98'76'543.210, 11'22'333.444", "Apostrophe 2-2-3 grouping"),
    ]
    
    passed = 0
    for test_input, description in apostrophe_tests:
        result = parser.parse_coordinates(test_input)
        if result:
            print(f"[PASS] {description}: {result}")
            passed += 1
        else:
            print(f"[FAIL] {description}: No match")
    
    print(f"Apostrophe Tests: {passed}/{len(apostrophe_tests)} passed\\n")
    return passed, len(apostrophe_tests)

def test_digit_groupings():
    """Test various digit grouping patterns"""
    parser = CoordinateParser()
    
    print("=== TESTING DIGIT GROUPINGS ===")
    
    grouping_tests = [
        # 4-digit numbers (x,xxx)
        ("1,234.567, -5,678.901, 9,012.345", "4-digit grouping"),
        
        # 5-digit numbers (xx,xxx) 
        ("12,345.678, -56,789.012, 90,123.456", "5-digit grouping"),
        
        # 6-digit numbers (xxx,xxx)
        ("123,456.789, -567,890.123, 901,234.567", "6-digit grouping"),
        
        # 1-2-3 digit grouping
        ("1,23,456.789, -9,87,654.321, 1,11,222.333", "1-2-3 digit grouping"),
        
        # 2-2-3 digit grouping
        ("12,34,567.890, -98,76,543.210, 11,22,333.444", "2-2-3 digit grouping"),
        
        # Very large numbers (7+ digits)
        ("1,234,567.890, -9,876,543.210, 1,111,222.333", "7-digit grouping"),
    ]
    
    passed = 0
    for test_input, description in grouping_tests:
        result = parser.parse_coordinates(test_input)
        if result:
            print(f"[PASS] {description}: {result}")
            passed += 1
        else:
            print(f"[FAIL] {description}: No match")
    
    print(f"Digit Grouping Tests: {passed}/{len(grouping_tests)} passed\\n")
    return passed, len(grouping_tests)

def test_all_separator_combinations():
    """Test all 5 separator patterns mentioned"""
    parser = CoordinateParser()
    
    print("=== TESTING ALL SEPARATOR PATTERNS ===")
    
    separator_tests = [
        # comma-dot (xxx,xxx.xxx)
        ("88,879.526, -288,696.11, 21,112.882", "comma-dot"),
        
        # dot-comma (xxx.xxx,xxx)  
        ("88.879,526, -288.696,11, 21.112,882", "dot-comma"),
        
        # space-dot (xxx xxx.xxx)
        ("88 879.526, -288 696.11, 21 112.882", "space-dot"),
        
        # space-comma (xxx xxx,xxx)
        ("88 879,526, -288 696,11, 21 112,882", "space-comma"),
        
        # apostrophe-comma (xxx'xxx,xxx)
        ("88'879,526, -288'696,11, 21'112,882", "apostrophe-comma"),
        
        # Mixed patterns in same coordinate set
        ("88,879.526, -288'696.11, 21 112.882", "Mixed separators"),
    ]
    
    passed = 0
    for test_input, description in separator_tests:
        result = parser.parse_coordinates(test_input)
        if result:
            print(f"[PASS] {description}: {result}")
            passed += 1
        else:
            print(f"[FAIL] {description}: No match")
    
    print(f"Separator Pattern Tests: {passed}/{len(separator_tests)} passed\\n")
    return passed, len(separator_tests)

def run_enhanced_test():
    """Run all enhanced coordinate recognition tests"""
    print("THE ISLE COORDINATE RECOGNITION - ENHANCED PATTERN TEST SUITE")
    print("=" * 70)
    
    # Run all test categories
    minus_passed, minus_total = test_minus_signs()
    apostrophe_passed, apostrophe_total = test_apostrophe_separators()
    grouping_passed, grouping_total = test_digit_groupings()
    separator_passed, separator_total = test_all_separator_combinations()
    
    # Calculate totals
    total_passed = minus_passed + apostrophe_passed + grouping_passed + separator_passed
    total_tests = minus_total + apostrophe_total + grouping_total + separator_total
    
    print("=" * 70)
    print(f"ENHANCED PATTERN RESULTS: {total_passed}/{total_tests} tests passed")
    print(f"Success Rate: {(total_passed/total_tests)*100:.1f}%")
    
    if total_passed == total_tests:
        print("🎉 ALL ENHANCED PATTERNS WORK! The Isle coordinate recognition supports all variations!")
    else:
        print("⚠️  Some enhanced patterns failed. Check the patterns above.")
    
    print("\\nTested enhanced patterns:")
    print("✓ Both minus signs: hyphen (-) and unicode minus (−)")
    print("✓ All 5 separator patterns: comma-dot, dot-comma, space-dot, space-comma, apostrophe-comma")
    print("✓ All digit groupings: 3-digit, 4-digit, 5-digit, 6-digit, 1-2-3, 2-2-3")
    print("✓ Mixed separator patterns within same coordinate set")

if __name__ == "__main__":
    run_enhanced_test()
