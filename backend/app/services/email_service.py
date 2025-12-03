"""
Email Service
Gerencia envio de emails para os usuários.
"""

import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional
from pathlib import Path
from ..core.config import get_settings

logger = logging.getLogger(__name__)


class EmailService:
    """Serviço de envio de emails."""

    def __init__(self):
        self.settings = get_settings()

    def is_configured(self) -> bool:
        """Verifica se o serviço de email está configurado."""
        return bool(
            self.settings.SMTP_HOST
            and self.settings.SMTP_USERNAME
            and self.settings.SMTP_PASSWORD
            and self.settings.SMTP_FROM_EMAIL
        )

    def send_document_email(
        self,
        to_email: str,
        document_path: str,
        file_id: str,
        payment_amount: float
    ) -> bool:
        """
        Envia o documento formatado por email após pagamento confirmado.

        Args:
            to_email: Email do destinatário
            document_path: Caminho do arquivo a ser enviado
            file_id: ID do arquivo
            payment_amount: Valor pago

        Returns:
            True se enviado com sucesso, False caso contrário
        """
        if not self.is_configured():
            logger.warning("Serviço de email não configurado. Email não será enviado.")
            return False

        try:
            logger.info(f"Preparando email para {to_email}")

            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = f"{self.settings.SMTP_FROM_NAME} <{self.settings.SMTP_FROM_EMAIL}>"
            msg['To'] = to_email
            msg['Subject'] = "Seu documento ABNT formatado está pronto!"

            # Corpo do email
            body = f"""
Olá!

Seu pagamento de R$ {payment_amount:.2f} foi confirmado com sucesso!

Seu documento já foi formatado seguindo as normas ABNT NBR 14724 e NBR 6023.
O arquivo está anexo neste email.

Detalhes do pedido:
- ID do arquivo: {file_id}
- Valor pago: R$ {payment_amount:.2f}

Obrigado por usar o ABNT Formatador!

---
ABNT Formatador
Formatação automática de trabalhos acadêmicos
            """

            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # Anexar arquivo
            document_path_obj = Path(document_path)
            if document_path_obj.exists():
                with open(document_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{document_path_obj.name}"'
                    )
                    msg.attach(part)
                logger.info(f"Arquivo anexado: {document_path_obj.name}")
            else:
                logger.error(f"Arquivo não encontrado: {document_path}")
                return False

            # Enviar email
            logger.info(f"Conectando ao servidor SMTP: {self.settings.SMTP_HOST}:{self.settings.SMTP_PORT}")

            if self.settings.SMTP_USE_TLS:
                server = smtplib.SMTP(self.settings.SMTP_HOST, self.settings.SMTP_PORT)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.settings.SMTP_HOST, self.settings.SMTP_PORT)

            server.login(self.settings.SMTP_USERNAME, self.settings.SMTP_PASSWORD)

            text = msg.as_string()
            server.sendmail(self.settings.SMTP_FROM_EMAIL, to_email, text)
            server.quit()

            logger.info(f"Email enviado com sucesso para {to_email}")
            return True

        except Exception as e:
            logger.error(f"Erro ao enviar email para {to_email}: {str(e)}")
            logger.exception(e)
            return False
