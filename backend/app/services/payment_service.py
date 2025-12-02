"""
Payment Service
Gerencia pagamentos via Mercado Pago e Stripe.
"""

from typing import Dict, Optional
import mercadopago
import stripe
import logging
from ..core.config import get_settings

# Configure logging
logger = logging.getLogger(__name__)


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
        # IMPORTANTE: Sistema sempre usa API REAL do Mercado Pago
        # Nunca gera QR Code genérico/falso
        logger.info("=" * 60)
        logger.info("🔍 VERIFICAÇÃO DE CREDENCIAIS DO MERCADO PAGO")
        logger.info("=" * 60)

        # Verifica se credenciais estão configuradas
        has_token = bool(self.settings.MERCADOPAGO_ACCESS_TOKEN and
                        self.settings.MERCADOPAGO_ACCESS_TOKEN != "" and
                        not self.settings.MERCADOPAGO_ACCESS_TOKEN.startswith("APP_USR-your-"))

        logger.info(f"📋 MERCADOPAGO_ACCESS_TOKEN configurado: {has_token}")

        if has_token and self.settings.MERCADOPAGO_ACCESS_TOKEN:
            logger.info(f"📋 Token (primeiros 30 chars): {self.settings.MERCADOPAGO_ACCESS_TOKEN[:30]}...")

        logger.info("=" * 60)

        # CREDENCIAIS NÃO CONFIGURADAS - RETORNA ERRO CLARO
        if not has_token:
            error_msg = """
╔════════════════════════════════════════════════════════════╗
║  ❌ ERRO: CREDENCIAIS DO MERCADO PAGO NÃO CONFIGURADAS    ║
╚════════════════════════════════════════════════════════════╝

MOTIVO: O servidor NÃO tem credenciais válidas do Mercado Pago.

ONDE CONFIGURAR:
  Arquivo: /caminho/para/backend/.env

  Adicione estas linhas:
  MERCADOPAGO_ACCESS_TOKEN=APP_USR-seu-token-real-aqui
  MERCADOPAGO_PUBLIC_KEY=APP_USR-sua-chave-real-aqui
  PAYMENT_DEV_MODE=False

COMO OBTER CREDENCIAIS:
  1. Acesse: https://www.mercadopago.com.br/developers/panel/app
  2. Selecione ou crie uma aplicação
  3. Copie "Access Token" e "Public Key"
  4. Cole no arquivo .env
  5. Reinicie o servidor

IMPORTANTE:
  - Este sistema NUNCA gera QR Code genérico
  - Sempre usa API real do Mercado Pago
  - Sem credenciais = sem pagamentos
            """
            logger.error(error_msg)

            return {
                "success": False,
                "status": "error",
                "error": "Credenciais do Mercado Pago não configuradas no servidor. Contate o administrador do sistema."
            }

        # Use real MercadoPago API
        logger.info("=" * 60)
        logger.info("✅ USANDO API REAL DO MERCADO PAGO")
        logger.info("=" * 60)
        logger.info(f"💰 Valor: R$ {amount}")
        logger.info(f"📝 Descrição: {description}")
        logger.info(f"🆔 File ID: {file_id}")
        logger.info("=" * 60)

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
            logger.info("🌐 Chamando API do Mercado Pago...")
            payment_response = sdk.payment().create(payment_data)

            logger.info("=" * 60)
            logger.info("📥 RESPOSTA DA API DO MERCADO PAGO")
            logger.info("=" * 60)
            logger.info(f"📊 Status HTTP: {payment_response.get('status')}")

            # Check if the request was successful (HTTP 201)
            if payment_response.get("status") != 201:
                error_message = payment_response.get("response", {}).get("message", "Erro desconhecido do Mercado Pago")
                error_details = payment_response.get("response", {})

                logger.error("=" * 60)
                logger.error("❌ ERRO NA API DO MERCADO PAGO")
                logger.error("=" * 60)
                logger.error(f"Mensagem: {error_message}")
                logger.error(f"Detalhes: {error_details}")
                logger.error("=" * 60)

                return {
                    "success": False,
                    "status": "error",
                    "error": f"Mercado Pago retornou erro: {error_message}"
                }

            payment = payment_response["response"]

            # Ensure status is always a string
            payment_status = str(payment.get("status", "pending"))

            # Extract QR Code data from response
            qr_code = payment.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code")
            qr_code_base64 = payment.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code_base64")

            logger.info(f"✅ Payment ID: {payment.get('id')}")
            logger.info(f"✅ Status: {payment_status}")
            logger.info("=" * 60)
            logger.info("🔍 ANÁLISE DO QR CODE RETORNADO")
            logger.info("=" * 60)
            logger.info(f"📱 QR Code (string PIX): {'✅ PRESENTE' if qr_code else '❌ AUSENTE'}")
            logger.info(f"🖼️  QR Code Base64 (imagem): {'✅ PRESENTE' if qr_code_base64 else '❌ AUSENTE'}")

            if qr_code_base64:
                logger.info(f"📏 Tamanho do Base64: {len(qr_code_base64)} caracteres")
                logger.info("✅ QR Code válido retornado pela API do Mercado Pago")
            else:
                logger.error("=" * 60)
                logger.error("❌ ERRO CRÍTICO: QR CODE NÃO RETORNADO")
                logger.error("=" * 60)
                logger.error("A API do Mercado Pago NÃO retornou o QR Code!")
                logger.error(f"Resposta point_of_interaction: {payment.get('point_of_interaction', {})}")
                logger.error("=" * 60)
                logger.error("POSSÍVEIS CAUSAS:")
                logger.error("1. Credenciais inválidas ou expiradas")
                logger.error("2. Conta do Mercado Pago sem permissão para PIX")
                logger.error("3. API do Mercado Pago mudou o formato da resposta")
                logger.error("4. Modo de teste requer configuração adicional")
                logger.error("=" * 60)

            logger.info("=" * 60)

            # qr_code_base64: Base64-encoded PNG image of QR Code (ready to display)
            # qr_code: Raw PIX payment code string (for copy-paste)
            # Both fields are inside: response.point_of_interaction.transaction_data
            return {
                "success": True,
                "payment_id": str(payment.get("id")),
                "status": payment_status,
                "qr_code": qr_code,
                "qr_code_base64": qr_code_base64,
                "ticket_url": payment.get("transaction_details", {}).get("external_resource_url"),
            }
        except Exception as e:
            logger.error("=" * 60)
            logger.error("❌ EXCEÇÃO AO CRIAR PAGAMENTO")
            logger.error("=" * 60)
            logger.error(f"Tipo: {type(e).__name__}")
            logger.error(f"Mensagem: {str(e)}")
            logger.error("=" * 60)

            import traceback
            logger.error(traceback.format_exc())

            return {
                "success": False,
                "status": "error",
                "error": f"Erro ao criar pagamento: {str(e)}"
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
