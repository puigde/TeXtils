# TeXtils
Some custom TeX utils

### Installing with pip:
```bash
git clone https://github.com/puigde/TeXtils.git
cd TeXtils
pip install .
```

### Development utils:
**Build and run test**
```bash
#!/bin/bash
set -e
echo "Building the project..."
python setup.py build
echo "Running unit tests..."
python -m unittest discover -s tests
echo "All tests passed. Proceeding with commit."
```
