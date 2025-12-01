from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Document(Base):
    """Document model for tracking uploads and processing."""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String(100), unique=True, index=True, nullable=False)
    original_filename = Column(String(255), nullable=False)
    original_extension = Column(String(10), nullable=False)

    # File paths
    original_path = Column(String(500), nullable=False)
    processed_path = Column(String(500), nullable=True)

    # Processing status
    status = Column(String(50), default="uploaded")  # uploaded, processing, completed, error
    error_message = Column(Text, nullable=True)

    # Document metadata
    original_pages = Column(Integer, nullable=True)
    formatted_pages = Column(Integer, nullable=True)

    # Pricing
    price = Column(Float, nullable=True)

    # Payment
    payment_id = Column(String(255), nullable=True)
    payment_status = Column(String(50), default="pending")  # pending, approved, rejected
    payment_method = Column(String(50), nullable=True)

    # Download
    downloaded = Column(Boolean, default=False)
    download_count = Column(Integer, default=0)

    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    payment_confirmed_at = Column(DateTime, nullable=True)
    downloaded_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Document {self.file_id} - {self.original_filename}>"


class PaymentTransaction(Base):
    """Payment transaction model."""

    __tablename__ = "payment_transactions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False)
    file_id = Column(String(100), index=True, nullable=False)

    # Payment gateway
    gateway = Column(String(50), nullable=False)  # mercadopago, stripe
    transaction_id = Column(String(255), unique=True, index=True)

    # Amount
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="BRL")

    # Status
    status = Column(String(50), default="pending")  # pending, approved, rejected, refunded

    # Metadata
    payer_email = Column(String(255), nullable=True)
    payment_method = Column(String(100), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<PaymentTransaction {self.transaction_id} - {self.status}>"
