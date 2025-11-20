"""Service for extracting text from various document formats."""
import io
from typing import BinaryIO

import pypdf
from docx import Document
from fastapi import UploadFile, HTTPException


class DocumentProcessor:
    """Handles text extraction from uploaded files."""

    @staticmethod
    def extract_text(file: UploadFile) -> str:
        """Extract text from an uploaded file based on its content type."""
        content_type = file.content_type
        filename = file.filename.lower() if file.filename else ""

        try:
            if content_type == "application/pdf" or filename.endswith(".pdf"):
                return DocumentProcessor._extract_from_pdf(file.file)
            elif (
                content_type
                == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                or filename.endswith(".docx")
            ):
                return DocumentProcessor._extract_from_docx(file.file)
            elif content_type == "text/plain" or filename.endswith(".txt"):
                return DocumentProcessor._extract_from_txt(file.file)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {content_type}. Supported formats: PDF, DOCX, TXT",
                )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=500, detail=f"Error processing file: {str(e)}"
            )

    @staticmethod
    def _extract_from_pdf(file_obj: BinaryIO) -> str:
        """Extract text from a PDF file."""
        try:
            reader = pypdf.PdfReader(file_obj)
            text = []
            for page in reader.pages:
                text.append(page.extract_text())
            return "\n".join(text)
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")

    @staticmethod
    def _extract_from_docx(file_obj: BinaryIO) -> str:
        """Extract text from a DOCX file."""
        try:
            doc = Document(file_obj)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"Failed to parse DOCX: {str(e)}")

    @staticmethod
    def _extract_from_txt(file_obj: BinaryIO) -> str:
        """Extract text from a TXT file."""
        try:
            return file_obj.read().decode("utf-8")
        except UnicodeDecodeError:
            # Try latin-1 fallback
            file_obj.seek(0)
            return file_obj.read().decode("latin-1")
        except Exception as e:
            raise ValueError(f"Failed to parse TXT: {str(e)}")
