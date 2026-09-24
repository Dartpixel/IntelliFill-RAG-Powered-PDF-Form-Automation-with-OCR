#!/usr/bin/env python
from pathlib import Path
from fastapi.templating import Jinja2Templates
from unittest.mock import MagicMock

base = Path(__file__).resolve().parent
templates_dir = base / 'templates'

templates = Jinja2Templates(directory=str(templates_dir))

# Create mock request object
mock_request = MagicMock()
mock_request.url = "http://localhost:8000/"

try:
    # Try to render upload.html
    response = templates.TemplateResponse(
        "upload.html",
        {"request": mock_request}
    )
    print('✓ TemplateResponse created successfully')
    print(f'Response type: {type(response)}')
    
except Exception as e:
    print(f'✗ Error rendering template: {type(e).__name__}: {str(e)}')
    import traceback
    traceback.print_exc()
