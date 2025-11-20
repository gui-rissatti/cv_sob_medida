"""Endpoint for extracting text from CV documents."""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from services.document_processor import DocumentProcessor

router = APIRouter()


class TextExtractionResponse(BaseModel):
    """Response containing extracted text."""

    text: str
    filename: str


@router.post(
    "/extract-cv-text",
    response_model=TextExtractionResponse,
    summary="Extract text from an uploaded CV file",
    tags=["extraction"],
)
async def extract_cv_text(file: UploadFile = File(...)) -> TextExtractionResponse:
    """
    Upload a CV file (PDF, DOCX, TXT) and get the extracted text.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    text = DocumentProcessor.extract_text(file)
    
    return TextExtractionResponse(
        text=text,
        filename=file.filename or "unknown"
    )
