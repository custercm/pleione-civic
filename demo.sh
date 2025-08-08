#!/bin/bash

# Quick test script to demonstrate Pleione's capabilities

echo "🧪 Testing Pleione Auto-Implementation"
echo "====================================="

echo ""
echo "This script will simulate what happens when you:"
echo "1. Ask Pleione to generate code"
echo "2. Let her create and test the code automatically"
echo "3. Use the auto-implement feature"
echo ""

read -p "Press Enter to continue..."

echo ""
echo "📁 Creating sample code in sandbox..."

# Create sandbox directory
mkdir -p backend/sandbox
mkdir -p backend/tests

# Create a sample Python file
cat > backend/sandbox/calculator.py << 'EOF'
# Filename: calculator.py

def add(a, b):
    """Add two numbers together"""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    return a + b

def multiply(a, b):
    """Multiply two numbers"""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    return a * b

def divide(a, b):
    """Divide two numbers"""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
EOF

# Create a sample test file
cat > backend/tests/test_calculator.py << 'EOF'
# Filename: test_calculator.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sandbox'))

from calculator import add, multiply, divide
import pytest

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0.5, 0.3) == pytest.approx(0.8)

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(0, 5) == 0

def test_divide():
    assert divide(6, 2) == 3
    assert divide(5, 2) == 2.5
    
    with pytest.raises(ValueError):
        divide(5, 0)

def test_type_errors():
    with pytest.raises(TypeError):
        add("hello", 5)
    
    with pytest.raises(TypeError):
        multiply("hello", 5)
EOF

echo "✅ Sample files created!"
echo ""
echo "🧪 Now running the auto-implementation process..."
echo ""

# Run the implementation script
./implement.sh

echo ""
echo "🎉 Demo complete!"
echo ""
echo "In a real scenario, Pleione would:"
echo "1. Generate these files automatically from your chat request"
echo "2. Run the tests automatically"
echo "3. Offer you buttons to auto-implement or review first"
echo ""
echo "You can now:"
echo "- Check backend/generated/ for implemented files"
echo "- Try asking Pleione to create real code via the web interface"
echo "- Use ./implement.sh anytime you want to implement sandbox code"
