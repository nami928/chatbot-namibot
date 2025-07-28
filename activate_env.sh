#!/bin/bash
# NamiBot Environment Activation Script

echo "🤖 Activating NamiBot Environment..."
echo "=================================="

# Activate conda environment
conda activate namibot

# Check if activation was successful
if [ $? -eq 0 ]; then
    echo "✅ NamiBot environment activated successfully!"
    echo "📦 Python version: $(python --version)"
    echo "📦 Installed packages:"
    pip list | grep -E "(wikipedia-api|requests)"
    echo ""
    echo "🚀 You can now run NamiBot:"
    echo "   python namibot.py          # Console version"
    echo "   python gui_namibot.py      # GUI version"
    echo "   python run.py              # Launcher"
    echo "   python test_namibot.py     # Test suite"
    echo ""
    echo "To deactivate: conda deactivate"
else
    echo "❌ Failed to activate NamiBot environment"
    echo "Please make sure the environment exists: conda create -n namibot python=3.11"
fi 