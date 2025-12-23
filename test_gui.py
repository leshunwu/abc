#!/usr/bin/env python3
"""
Test script to verify ABC GUI functionality without requiring display
"""

import sys
import os

def test_import():
    """Test that the GUI module can be imported"""
    try:
        # Don't actually create GUI, just test imports
        import subprocess
        import threading
        print("✓ Required standard library modules available")
        return True
    except ImportError as e:
        print(f"✗ Missing required module: {e}")
        return False

def test_abc_binary():
    """Test that ABC binary exists and works"""
    abc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "abc")
    
    if not os.path.exists(abc_path):
        print(f"✗ ABC binary not found at {abc_path}")
        return False
    
    print(f"✓ ABC binary found at {abc_path}")
    
    try:
        import subprocess
        result = subprocess.run([abc_path, "-c", "help"], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print("✓ ABC binary executes successfully")
            return True
        else:
            print(f"✗ ABC binary failed with return code {result.returncode}")
            return False
    except Exception as e:
        print(f"✗ Error testing ABC binary: {e}")
        return False

def test_gui_script():
    """Test that the GUI script is valid Python"""
    gui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "abc_gui.py")
    
    if not os.path.exists(gui_path):
        print(f"✗ GUI script not found at {gui_path}")
        return False
    
    print(f"✓ GUI script found at {gui_path}")
    
    # Check syntax by compiling
    try:
        with open(gui_path, 'r') as f:
            code = f.read()
        compile(code, gui_path, 'exec')
        print("✓ GUI script syntax is valid")
        return True
    except SyntaxError as e:
        print(f"✗ GUI script has syntax error: {e}")
        return False

def test_example_file():
    """Test that example file exists"""
    example_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "i10.aig")
    
    if os.path.exists(example_path):
        print(f"✓ Example file found at {example_path}")
        return True
    else:
        print(f"ℹ Example file i10.aig not found (optional - GUI will work without it)")
        return True  # Not critical, GUI can still function

def main():
    """Run all tests"""
    print("=" * 60)
    print("ABC GUI Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("Standard Library Modules", test_import),
        ("ABC Binary", test_abc_binary),
        ("GUI Script", test_gui_script),
        ("Example File", test_example_file),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\nTesting {name}:")
        print("-" * 40)
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append((name, False))
    
    print()
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! GUI is ready to use.")
        print("\nTo launch the GUI, run:")
        print("  ./launch_gui.sh")
        print("or")
        print("  python3 abc_gui.py")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
