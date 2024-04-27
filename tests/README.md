
# Development Guide

Connect to Python debugger in VS Code:

```python
poetry run python -m debugpy --listen 5678 --wait-for-client src/cmdict/__main__.py search banana
```
