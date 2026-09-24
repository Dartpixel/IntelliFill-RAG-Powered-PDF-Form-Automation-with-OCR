from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from jinja2 import Environment, FileSystemLoader

from app.auto_fill import generate_form_data
from app.pdf_filler import fill_pdf

app = FastAPI()

# Get absolute path to templates
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

# Mount static files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
OUTPUT_DIR = BASE_DIR / "data" / "outputs"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

generated_data = {}


@app.get("/test")
async def test():
    """Test endpoint to verify server is running"""
    return {"status": "ok", "templates_dir": str(TEMPLATES_DIR), "exists": TEMPLATES_DIR.exists()}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with PDF upload form"""
    template = jinja_env.get_template("upload.html")
    return template.render(request=request)


@app.post("/upload", response_class=HTMLResponse)
async def upload_pdf(
    request: Request,
    pdf_file: UploadFile = File(...)
):
    """Upload PDF and extract/generate form field values"""
    
    try:
        uploaded_file_path = (
            UPLOAD_DIR / pdf_file.filename
        )

        with open(uploaded_file_path, "wb") as f:
            f.write(await pdf_file.read())

        fields, generated_values = generate_form_data(
            str(uploaded_file_path)
        )

        generated_data["input_pdf"] = str(
            uploaded_file_path
        )

        generated_data["fields"] = fields
        generated_data["values"] = generated_values

        template = jinja_env.get_template("review.html")
        return template.render(
            request=request,
            generated_values=generated_values
        )
    except Exception as e:
        template = jinja_env.get_template("error.html") if Path(TEMPLATES_DIR / "error.html").exists() else None
        if template:
            return template.render(request=request, error=str(e))
        return f"<h1>Error</h1><p>{str(e)}</p>"


@app.post("/generate-pdf", response_class=HTMLResponse)
async def generate_pdf(request: Request):
    """Generate filled PDF from cached values"""

    try:
        if not generated_data.get("values"):
            return "<h1>Error</h1><p>No form fields were found in the PDF. Cannot generate filled PDF without fields.</p><a href='/'>Upload another PDF</a>"

        input_pdf = generated_data["input_pdf"]

        submitted_values = await request.form()
        field_values = {
            field_name: str(submitted_values.get(field_name, value))
            for field_name, value in generated_data["values"].items()
        }
        generated_data["values"] = field_values

        output_file = OUTPUT_DIR / "filled_form.pdf"

        fill_pdf(
            input_pdf_path=input_pdf,
            output_pdf_path=str(output_file),
            field_values=field_values,
            fields_metadata=generated_data.get("fields")
        )

        template = jinja_env.get_template("result.html")
        return template.render(
            request=request,
            file_name="filled_form.pdf"
        )
    except Exception as e:
        template = jinja_env.get_template("error.html") if Path(TEMPLATES_DIR / "error.html").exists() else None
        if template:
            return template.render(request=request, error=str(e))
        return f"<h1>Error</h1><p>{str(e)}</p>"


@app.get("/download/{file_name}")
async def download_file(file_name: str):

    file_path = OUTPUT_DIR / file_name

    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type="application/pdf"
    )