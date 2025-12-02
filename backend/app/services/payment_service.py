"""
Payment Service
Gerencia pagamentos via Mercado Pago e Stripe.
"""

from typing import Dict, Optional
import mercadopago
import stripe
from ..core.config import get_settings


class PaymentService:
    """Serviço de pagamento."""

    def __init__(self):
        self.settings = get_settings()

    def create_mercadopago_payment(
        self,
        amount: float,
        description: str,
        file_id: str,
        payer_email: Optional[str] = None
    ) -> Dict:
        """
        Cria um pagamento via Mercado Pago.

        Args:
            amount: Valor em reais
            description: Descrição do pagamento
            file_id: ID do arquivo
            payer_email: Email do pagador

        Returns:
            Dados do pagamento
        """
        # Check if MercadoPago credentials are configured
        # Priority: Use real MercadoPago API if credentials are available
        if not self.settings.MERCADOPAGO_ACCESS_TOKEN or self.settings.MERCADOPAGO_ACCESS_TOKEN == "":
            # Fallback to development mode only if no credentials are configured
            if self.settings.PAYMENT_DEV_MODE:
                import uuid
                import base64
                import qrcode
                import io

                # Generate a fake PIX code for development
                fake_qr_data = f"00020126360014BR.GOV.BCB.PIX0114+55119999999990204000053039865802BR5925ABNT Formatador LTDA6009SAO PAULO62070503***6304{uuid.uuid4().hex[:4].upper()}"

                # Create a real QR code that can be scanned
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(fake_qr_data)
                qr.make(fit=True)

                # Generate QR code image
                img = qr.make_image(fill_color="black", back_color="white")

                # Convert to base64
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)
                fake_qr_base64 = base64.b64encode(buffer.getvalue()).decode()

                return {
                    "success": True,
                    "payment_id": f"dev_{uuid.uuid4().hex}",
                    "status": "pending",
                    "qr_code": fake_qr_data,
                    "qr_code_base64": fake_qr_base64,
                    "ticket_url": None,
                }
            else:
                raise ValueError("Mercado Pago não configurado e modo de desenvolvimento desabilitado")

        # Use real MercadoPago API
        # This is now the primary path when credentials are configured

        # Initialize SDK
        sdk = mercadopago.SDK(self.settings.MERCADOPAGO_ACCESS_TOKEN)

        payment_data = {
            "transaction_amount": float(amount),
            "description": description,
            "payment_method_id": "pix",
            "external_reference": file_id,
            "notification_url": f"https://seu-dominio.com/api/webhooks/mercadopago",
            "payer": {
                "email": payer_email if payer_email else "cliente@abntformatador.com",
                "first_name": "Cliente",
                "last_name": "ABNT Formatador"
            }
        }

        try:
            # Create PIX payment using MercadoPago SDK
            # Documentation: https://www.mercadopago.com.br/developers/pt/docs/checkout-api/integration-configuration/integrate-with-pix
            payment_response = sdk.payment().create(payment_data)

            # Check if the request was successful (HTTP 201)
            if payment_response.get("status") != 201:
                error_message = payment_response.get("response", {}).get("message", "Erro desconhecido do Mercado Pago")
                return {
                    "success": False,
                    "status": "error",
                    "error": f"Mercado Pago retornou erro: {error_message}"
                }

            payment = payment_response["response"]

            # Ensure status is always a string
            payment_status = str(payment.get("status", "pending"))

            # Extract QR Code data from response
            # qr_code_base64: Base64-encoded PNG image of QR Code (ready to display)
            # qr_code: Raw PIX payment code string (for copy-paste)
            # Both fields are inside: response.point_of_interaction.transaction_data
            return {
                "success": True,
                "payment_id": str(payment.get("id")),
                "status": payment_status,
                "qr_code": payment.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code"),
                "qr_code_base64": payment.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code_base64"),
                "ticket_url": payment.get("transaction_details", {}).get("external_resource_url"),
            }
        except Exception as e:
            return {
                "success": False,
                "status": "error",
                "error": str(e)
            }

    def create_stripe_payment_intent(
        self,
        amount: float,
        description: str,
        file_id: str,
        payer_email: Optional[str] = None
    ) -> Dict:
        """
        Cria um Payment Intent no Stripe.

        Args:
            amount: Valor em reais
            description: Descrição
            file_id: ID do arquivo
            payer_email: Email do pagador

        Returns:
            Dados do pagamento
        """
        if not self.settings.STRIPE_SECRET_KEY:
            raise ValueError("Stripe não configurado")

        stripe.api_key = self.settings.STRIPE_SECRET_KEY

        try:
            # Converte BRL para centavos
            amount_cents = int(amount * 100)

            payment_intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency="brl",
                description=description,
                metadata={
                    "file_id": file_id,
                },
                receipt_email=payer_email,
            )

            return {
                "success": True,
                "payment_id": payment_intent.id,
                "client_secret": payment_intent.client_secret,
                "status": payment_intent.status,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def verify_mercadopago_payment(self, payment_id: str) -> Dict:
        """
        Verifica o status de um pagamento no Mercado Pago.

        Args:
            payment_id: ID do pagamento

        Returns:
            Status do pagamento
        """
        # Development mode: keep payments pending to allow QR code display
        # In dev mode, payments remain pending indefinitely for testing
        if self.settings.PAYMENT_DEV_MODE:
            if payment_id.startswith("dev_"):
                return {
                    "success": True,
                    "status": "pending",
                    "status_detail": "pending_waiting_payment",
                    "approved": False,
                }

        # Production mode: check real payment status
        if not self.settings.MERCADOPAGO_ACCESS_TOKEN:
            raise ValueError("Mercado Pago não configurado")

        sdk = mercadopago.SDK(self.settings.MERCADOPAGO_ACCESS_TOKEN)

        try:
            payment_response = sdk.payment().get(payment_id)
            payment = payment_response["response"]

            return {
                "success": True,
                "status": payment.get("status"),
                "status_detail": payment.get("status_detail"),
                "approved": payment.get("status") == "approved",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def verify_stripe_payment(self, payment_intent_id: str) -> Dict:
        """
        Verifica o status de um Payment Intent no Stripe.

        Args:
            payment_intent_id: ID do Payment Intent

        Returns:
            Status do pagamento
        """
        if not self.settings.STRIPE_SECRET_KEY:
            raise ValueError("Stripe não configurado")

        stripe.api_key = self.settings.STRIPE_SECRET_KEY

        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            return {
                "success": True,
                "status": payment_intent.status,
                "approved": payment_intent.status == "succeeded",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def calculate_price(self, page_count: int) -> float:
        """
        Calcula o preço baseado no número de páginas.

        Args:
            page_count: Número de páginas

        Returns:
            Preço total em reais
        """
        return round(page_count * self.settings.PRICE_PER_PAGE, 2)
