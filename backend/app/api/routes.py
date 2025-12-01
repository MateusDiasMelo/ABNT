"""
API Routes
Endpoints para upload, processamento, pagamento e download.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
import os
import uuid
from datetime import datetime, timedelta
import aiofiles

from ..core.config import get_settings
from ..services.document_processor import DocumentProcessor, DocumentAnalyzer
from ..services.payment_service import PaymentService

router = APIRouter()
settings = get_settings()
payment_service = PaymentService()

# Armazena informações de documentos em memória (em produção, usar DB)
documents_store = {}


class DocumentResponse(BaseModel):
    """Resposta de upload de documento."""
    file_id: str
    original_filename: str
    original_extension: str
    status: str
    message: str


class ProcessingResponse(BaseModel):
    """Resposta de processamento."""
    file_id: str
    status: str
    formatted_pages: int
    price: float
    currency: str = "BRL"
    message: str


class PaymentRequest(BaseModel):
    """Requisição de pagamento."""
    file_id: str
    gateway: str  # mercadopago ou stripe
    payer_email: Optional[EmailStr] = None


class PaymentResponse(BaseModel):
    """Resposta de pagamento."""
    success: bool
    payment_id: Optional[str] = None
    status: Optional[str] = None
    qr_code: Optional[str] = None
    qr_code_base64: Optional[str] = None
    ticket_url: Optional[str] = None
    client_secret: Optional[str] = None
    error: Optional[str] = None


class PaymentVerificationRequest(BaseModel):
    """Requisição de verificação de pagamento."""
    file_id: str
    payment_id: str
    gateway: str


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Upload de documento DOCX ou PDF.

    Args:
        file: Arquivo para upload

    Returns:
        Informações do documento
    """
    # Valida extensão
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in settings.allowed_extensions_list:
        raise HTTPException(
            status_code=400,
            detail=f"Formato não suportado. Use: {', '.join(settings.allowed_extensions_list)}"
        )

    # Gera ID único
    file_id = str(uuid.uuid4())

    # Cria diretórios se não existirem
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.PROCESSED_DIR, exist_ok=True)

    # Define caminhos
    original_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.{file_extension}")

    try:
        # Salva arquivo
        async with aiofiles.open(original_path, 'wb') as out_file:
            content = await file.read()

            # Valida tamanho
            if len(content) > settings.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"Arquivo muito grande. Máximo: {settings.MAX_FILE_SIZE / 1048576}MB"
                )

            await out_file.write(content)

        # Valida documento
        is_valid, error_message = DocumentProcessor.validate_document(
            original_path, file_extension
        )

        if not is_valid:
            os.unlink(original_path)
            raise HTTPException(status_code=400, detail=error_message)

        # Analisa documento
        analysis = DocumentAnalyzer.analyze_document(original_path, file_extension)

        # Armazena informações
        documents_store[file_id] = {
            "file_id": file_id,
            "original_filename": file.filename,
            "original_extension": file_extension,
            "original_path": original_path,
            "processed_path": None,
            "status": "uploaded",
            "uploaded_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=settings.FILE_RETENTION_HOURS),
            "analysis": analysis,
            "formatted_pages": None,
            "price": None,
            "payment_status": "pending",
        }

        # Agenda limpeza do arquivo
        background_tasks.add_task(schedule_file_cleanup, file_id)

        return DocumentResponse(
            file_id=file_id,
            original_filename=file.filename,
            original_extension=file_extension,
            status="uploaded",
            message="Arquivo enviado com sucesso"
        )

    except HTTPException:
        raise
    except Exception as e:
        if os.path.exists(original_path):
            os.unlink(original_path)
        raise HTTPException(status_code=500, detail=f"Erro ao processar upload: {str(e)}")


@router.post("/process/{file_id}", response_model=ProcessingResponse)
async def process_document(file_id: str):
    """
    Processa documento aplicando formatação ABNT.

    Args:
        file_id: ID do documento

    Returns:
        Informações do processamento
    """
    # Busca documento
    if file_id not in documents_store:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    doc_info = documents_store[file_id]

    if doc_info["status"] not in ["uploaded", "error"]:
        raise HTTPException(
            status_code=400,
            detail=f"Documento já foi processado. Status: {doc_info['status']}"
        )

    try:
        # Atualiza status
        doc_info["status"] = "processing"

        # Define caminho de saída
        processed_path = os.path.join(
            settings.PROCESSED_DIR,
            f"{file_id}_formatted.docx"
        )

        # Processa documento
        if doc_info["original_extension"] == "docx":
            _, page_count = DocumentProcessor.process_docx(
                doc_info["original_path"],
                processed_path
            )
        elif doc_info["original_extension"] == "pdf":
            _, page_count = DocumentProcessor.process_pdf(
                doc_info["original_path"],
                processed_path
            )
        else:
            raise ValueError("Formato não suportado")

        # Calcula preço
        price = payment_service.calculate_price(page_count)

        # Atualiza informações
        doc_info["processed_path"] = processed_path
        doc_info["formatted_pages"] = page_count
        doc_info["price"] = price
        doc_info["status"] = "completed"
        doc_info["processed_at"] = datetime.utcnow()

        return ProcessingResponse(
            file_id=file_id,
            status="completed",
            formatted_pages=page_count,
            price=price,
            currency="BRL",
            message=f"Documento formatado com sucesso. {page_count} páginas × R$ {settings.PRICE_PER_PAGE} = R$ {price}"
        )

    except Exception as e:
        doc_info["status"] = "error"
        doc_info["error_message"] = str(e)
        raise HTTPException(status_code=500, detail=f"Erro ao processar documento: {str(e)}")


@router.post("/payment/create", response_model=PaymentResponse)
async def create_payment(payment_request: PaymentRequest):
    """
    Cria um pagamento.

    Args:
        payment_request: Dados do pagamento

    Returns:
        Informações do pagamento
    """
    # Busca documento
    if payment_request.file_id not in documents_store:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    doc_info = documents_store[payment_request.file_id]

    if doc_info["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail="Documento ainda não foi processado"
        )

    if doc_info["price"] is None:
        raise HTTPException(status_code=400, detail="Preço não calculado")

    try:
        description = f"Formatação ABNT - {doc_info['original_filename']} ({doc_info['formatted_pages']} páginas)"

        if payment_request.gateway == "mercadopago":
            result = payment_service.create_mercadopago_payment(
                amount=doc_info["price"],
                description=description,
                file_id=payment_request.file_id,
                payer_email=payment_request.payer_email
            )
        elif payment_request.gateway == "stripe":
            result = payment_service.create_stripe_payment_intent(
                amount=doc_info["price"],
                description=description,
                file_id=payment_request.file_id,
                payer_email=payment_request.payer_email
            )
        else:
            raise HTTPException(status_code=400, detail="Gateway de pagamento inválido")

        if result.get("success"):
            doc_info["payment_id"] = result.get("payment_id")
            doc_info["payment_gateway"] = payment_request.gateway

        return PaymentResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar pagamento: {str(e)}")


@router.post("/payment/verify")
async def verify_payment(verification: PaymentVerificationRequest):
    """
    Verifica o status de um pagamento.

    Args:
        verification: Dados da verificação

    Returns:
        Status do pagamento
    """
    # Busca documento
    if verification.file_id not in documents_store:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    doc_info = documents_store[verification.file_id]

    try:
        if verification.gateway == "mercadopago":
            result = payment_service.verify_mercadopago_payment(verification.payment_id)
        elif verification.gateway == "stripe":
            result = payment_service.verify_stripe_payment(verification.payment_id)
        else:
            raise HTTPException(status_code=400, detail="Gateway inválido")

        # Atualiza status se aprovado
        if result.get("approved"):
            doc_info["payment_status"] = "approved"
            doc_info["payment_confirmed_at"] = datetime.utcnow()

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar pagamento: {str(e)}")


@router.get("/download/{file_id}")
async def download_document(file_id: str):
    """
    Download do documento formatado.

    Args:
        file_id: ID do documento

    Returns:
        Arquivo DOCX formatado
    """
    # Busca documento
    if file_id not in documents_store:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    doc_info = documents_store[file_id]

    # Verifica pagamento
    if doc_info["payment_status"] != "approved":
        raise HTTPException(
            status_code=403,
            detail="Pagamento não confirmado. Complete o pagamento para fazer o download."
        )

    # Verifica se arquivo existe
    if not doc_info["processed_path"] or not os.path.exists(doc_info["processed_path"]):
        raise HTTPException(status_code=404, detail="Arquivo processado não encontrado")

    # Atualiza contagem de downloads
    doc_info["downloaded"] = True
    doc_info["download_count"] = doc_info.get("download_count", 0) + 1
    doc_info["downloaded_at"] = datetime.utcnow()

    # Retorna arquivo
    return FileResponse(
        path=doc_info["processed_path"],
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"{doc_info['original_filename'].rsplit('.', 1)[0]}_ABNT.docx"
    )


@router.get("/status/{file_id}")
async def get_document_status(file_id: str):
    """
    Obtém status do documento.

    Args:
        file_id: ID do documento

    Returns:
        Status e informações
    """
    if file_id not in documents_store:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    doc_info = documents_store[file_id]

    return {
        "file_id": file_id,
        "original_filename": doc_info["original_filename"],
        "status": doc_info["status"],
        "formatted_pages": doc_info.get("formatted_pages"),
        "price": doc_info.get("price"),
        "payment_status": doc_info.get("payment_status"),
        "uploaded_at": doc_info["uploaded_at"],
        "expires_at": doc_info["expires_at"],
    }


async def schedule_file_cleanup(file_id: str):
    """
    Agenda limpeza de arquivos temporários.

    Args:
        file_id: ID do arquivo
    """
    # Em produção, usar Celery ou similar
    # Por ora, apenas registra
    pass
