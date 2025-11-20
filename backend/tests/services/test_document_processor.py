"""Tests for DocumentProcessor service."""
import io
import pytest
from fastapi import UploadFile, HTTPException
from services.document_processor import DocumentProcessor

def test_extract_from_txt():
    content = b"Hello world"
    file = UploadFile(filename="test.txt", file=io.BytesIO(content), headers={"content-type": "text/plain"})
    
    text = DocumentProcessor.extract_text(file)
    assert text == "Hello world"

def test_extract_unsupported_format():
    content = b"fake content"
    file = UploadFile(filename="test.exe", file=io.BytesIO(content), headers={"content-type": "application/x-msdownload"})
    
    with pytest.raises(HTTPException) as exc:
        DocumentProcessor.extract_text(file)
    assert exc.value.status_code == 400
    assert "Unsupported file type" in exc.value.detail

# Note: Testing PDF/DOCX requires actual files or mocking pypdf/docx
# For this quick test, we verify the logic flow and TXT support.
