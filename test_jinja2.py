#!/usr/bin/env python
from pathlib import Path
from fastapi.templating import Jinja2Templates

base = Path(__file__).resolve().parent
templates_dir = base / 'templates'
print(f'Templates dir: {templates_dir}')
print(f'Exists: {templates_dir.exists()}')
print(f'Files: {list(templates_dir.glob("*.html"))}')

try:
    templates = Jinja2Templates(directory=str(templates_dir))
    print('✓ Jinja2Templates initialized successfully')
    
    # Try to load upload.html
    template = templates.get_template("upload.html")
    print('✓ upload.html template loaded successfully')
except Exception as e:
    print(f'✗ Error: {type(e).__name__}: {str(e)}')
    import traceback
    traceback.print_exc()
