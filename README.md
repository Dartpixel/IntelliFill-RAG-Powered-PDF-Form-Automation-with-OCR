# IntelliFill — RAG-Powered PDF Form Automation with OCR

> An AI-powered system that automatically fills PDF forms using information retrieved from a document knowledge base.

## 🚀 Overview

IntelliFill processes multiple PDFs as a **knowledge base** and uses **RAG, embeddings, metadata, chunking, and LLMs** to retrieve relevant information and automatically populate a target PDF form.

It supports both **AcroForm and non-AcroForm PDFs**, using **Tesseract OCR** for static/scanned documents, and provides APIs through **FastAPI**.

## ✨ Features

- 📚 Multi-PDF knowledge base
- 🧩 Document chunking & metadata extraction
- 🔢 Semantic embeddings & retrieval
- 🧠 Retrieval-Augmented Generation (RAG)
- 📝 Automatic PDF form filling
- 📋 AcroForm field extraction & filling
- 🔍 OCR-based processing for non-AcroForm PDFs
- 🤖 LLM-powered field value generation
- ⚡ FastAPI backend
- 📥 Downloadable completed PDFs

## 🔄 Workflow

```text
Reference PDFs
     ↓
Text Extraction / OCR
     ↓
Chunking + Metadata
     ↓
Embeddings
     ↓
Knowledge Base
     ↓
Target PDF Form
     ↓
Field Extraction
     ↓
RAG Retrieval
     ↓
LLM
     ↓
Auto-Fill
     ↓
Completed PDF
```

## 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │    Reference PDFs    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   PDF Text / OCR     │
                         │      Extraction      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Chunking        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │     Metadata + Embeddings   │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                         ┌──────────────────────┐
                         │    Vector Index      │
                         │    / Knowledge Base  │
                         └──────────┬───────────┘
                                    │
                                    │
                         ┌──────────▼───────────┐
                         │   Target PDF Form    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Form Extraction    │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴───────────┐
                         │                      │
                         ▼                      ▼
                  ┌─────────────┐       ┌─────────────┐
                  │   AcroForm  │       │ Non-AcroForm│
                  │    Fields   │       │     PDF     │
                  └──────┬──────┘       └──────┬──────┘
                         │                      │
                         │                OCR / Tesseract
                         │                      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Semantic Retrieval   │
                         │       (RAG)          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │         LLM          │
                         │  Field Value Mapping │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   PDF Auto Filling   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Completed PDF      │
                         │     Download         │
                         └──────────────────────┘
```

## 🛠️ Tech Stack

```text
Python
FastAPI
RAG
LLMs
Embeddings
OCR / Tesseract
PDF & AcroForm Processing
Metadata & Semantic Search
```

## ⚙️ Installation
```text

git clone https://github.com/Dartpixel/IntelliFill-RAG-Powered-PDF-Form-Automation-with-OCR.git
cd IntelliFill-RAG-Powered-PDF-Form-Automation-with-OCR

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

Create a .env file for required API/model credentials.
```

## ▶️ Run

```text
uvicorn app.main:app --reload
API Documentation: http://127.0.0.1:8000/docs
```
