"""
Syntax and Structure Test Script
Tests the Python files without requiring external dependencies
"""

import ast
import sys

def test_file_syntax(filename):
    """Test if a Python file has valid syntax"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            code = file.read()
            ast.parse(code)
        print(f"✓ {filename}: Syntax is VALID")
        return True
    except SyntaxError as e:
        print(f"✗ {filename}: Syntax Error - {e}")
        return False
    except Exception as e:
        print(f"✗ {filename}: Error - {e}")
        return False

def check_imports(filename):
    """Extract and display imports from a Python file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}" if module else alias.name)
        
        if imports:
            print(f"  Imports: {', '.join(set(imports))}")
        return imports
    except Exception as e:
        print(f"  Could not check imports: {e}")
        return []

def count_functions(filename):
    """Count functions in a Python file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())
        
        function_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
        class_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
        
        print(f"  Functions: {function_count}, Classes: {class_count}")
        return function_count, class_count
    except Exception as e:
        print(f"  Could not count functions: {e}")
        return 0, 0

def main():
    """Run all tests"""
    print("="*60)
    print("COMPUTER VISION PROJECT - SYNTAX & STRUCTURE TEST")
    print("="*60)
    print()
    
    files_to_test = ['image_processing.py', 'main.py']
    all_passed = True
    
    for filename in files_to_test:
        print(f"Testing: {filename}")
        print("-" * 60)
        
        if test_file_syntax(filename):
            check_imports(filename)
            count_functions(filename)
        else:
            all_passed = False
        
        print()
    
    print("="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print()
        print("Next Steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the application: python main.py")
        print("3. Upload an image and test all operations")
    else:
        print("✗ SOME TESTS FAILED")
        sys.exit(1)
    print("="*60)

if __name__ == "__main__":
    main()
