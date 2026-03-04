#!/bin/bash

# This script creates all remaining RuralGuard AI files

echo "Creating remaining RuralGuard AI project files..."

# Create LICENSE
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 RuralGuard AI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

echo "✓ Created LICENSE"
echo "✓ All files created successfully!"
echo ""
echo "Next steps:"
echo "1. Review and customize the generated files"
echo "2. Add your AWS credentials to backend/.env"
echo "3. Run: cd backend && pip install -r requirements.txt"
echo "4. Run: python api.py"
echo "5. Open frontend/index.html in your browser"

