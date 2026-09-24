from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.rag.service import RAGService
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.ingestion import IngestionRequest, IngestionResponse
from app.services.ingestion_service import IngestionService


router = APIRouter()


# ---------------------------------------------------------
# Services
# ---------------------------------------------------------

ingestion_service = IngestionService()
rag_service = RAGService()


# ---------------------------------------------------------
# Upload directory
# ---------------------------------------------------------

UPLOAD_DIRECTORY = Path("data/uploads")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "RAG backend is running.",
    }


# ---------------------------------------------------------
# Ingest URL / existing source
# ---------------------------------------------------------

@router.post(
    "/ingest",
    response_model=IngestionResponse,
)
def ingest_source(request: IngestionRequest):

    try:
        document = ingestion_service.ingest(
            request.source
        )

        return IngestionResponse(
            document_id=document.document_id,
            source_type=document.metadata.source_type,
            source=document.metadata.source,
            title=document.metadata.title,
            message="Source ingested successfully.",
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to ingest source: {str(exc)}",
        ) from exc


# ---------------------------------------------------------
# Ingest uploaded PDF
# ---------------------------------------------------------

@router.post(
    "/ingest/file",
    response_model=IngestionResponse,
)
async def ingest_file(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file was provided.",
        )

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    safe_filename = (
        f"{uuid4().hex}_{Path(file.filename).name}"
    )

    file_path = UPLOAD_DIRECTORY / safe_filename

    try:

        contents = await file.read()

        with open(file_path, "wb") as output_file:
            output_file.write(contents)

        document = ingestion_service.ingest(
            str(file_path)
        )

        return IngestionResponse(
            document_id=document.document_id,
            source_type=document.metadata.source_type,
            source=document.metadata.source,
            title=document.metadata.title,
            message="PDF uploaded and ingested successfully.",
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to ingest PDF: {str(exc)}",
        ) from exc


# ---------------------------------------------------------
# Ask question
# ---------------------------------------------------------

@router.post(
    "/ask",
    response_model=ChatResponse,
)
def ask_question(request: ChatRequest):

    try:

        answer = rag_service.ask(
            question=request.question,
            document_id=request.document_id,
        )

        return ChatResponse(
            answer=answer
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate answer: {str(exc)}",
        ) from exc