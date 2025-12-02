"""
Google Sheets Service
Gerencia operações de leitura e escrita no Google Sheets como banco de dados.
"""

import gspread
from google.oauth2.service_account import Credentials
from typing import Dict, List, Optional, Any
from datetime import datetime
import os
from ..core.config import get_settings


class SheetsService:
    """Serviço para integração com Google Sheets."""

    def __init__(self):
        """Inicializa o serviço do Google Sheets."""
        self.settings = get_settings()
        self.client = None
        self.spreadsheet = None
        self._authenticate()

    def _authenticate(self):
        """Autentica com Google Sheets API."""
        try:
            # Define os escopos necessários
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            # Caminho para o arquivo de credenciais
            credentials_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                self.settings.GOOGLE_SHEETS_CREDENTIALS_FILE
            )

            # Autentica usando o arquivo de credenciais
            credentials = Credentials.from_service_account_file(
                credentials_path,
                scopes=scopes
            )

            # Cria o cliente gspread
            self.client = gspread.authorize(credentials)

            # Abre a planilha pelo ID
            self.spreadsheet = self.client.open_by_key(
                self.settings.GOOGLE_SHEETS_SPREADSHEET_ID
            )

        except Exception as e:
            print(f"Erro ao autenticar com Google Sheets: {str(e)}")
            raise

    def get_worksheet(self, sheet_name: str = None):
        """
        Obtém uma planilha específica.

        Args:
            sheet_name: Nome da planilha. Se None, usa a primeira planilha.

        Returns:
            Worksheet object
        """
        if sheet_name:
            return self.spreadsheet.worksheet(sheet_name)
        return self.spreadsheet.sheet1

    def create_payment_record(
        self,
        file_id: str,
        file_name: str,
        page_count: int,
        amount: float,
        payment_method: str,
        payment_id: str,
        status: str = "pending",
        payer_email: Optional[str] = None,
        sheet_name: str = "Pagamentos"
    ) -> bool:
        """
        Cria um registro de pagamento na planilha.

        Args:
            file_id: ID do arquivo
            file_name: Nome do arquivo
            page_count: Número de páginas
            amount: Valor do pagamento
            payment_method: Método de pagamento (mercadopago, stripe)
            payment_id: ID do pagamento no gateway
            status: Status do pagamento
            payer_email: Email do pagador
            sheet_name: Nome da aba na planilha

        Returns:
            True se sucesso, False caso contrário
        """
        try:
            worksheet = self.get_worksheet(sheet_name)

            # Prepara os dados
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = [
                timestamp,
                file_id,
                file_name,
                str(page_count),
                f"R$ {amount:.2f}",
                payment_method,
                payment_id,
                status,
                payer_email or ""
            ]

            # Adiciona a linha na planilha
            worksheet.append_row(row)
            return True

        except Exception as e:
            print(f"Erro ao criar registro de pagamento: {str(e)}")
            return False

    def update_payment_status(
        self,
        payment_id: str,
        new_status: str,
        sheet_name: str = "Pagamentos"
    ) -> bool:
        """
        Atualiza o status de um pagamento.

        Args:
            payment_id: ID do pagamento
            new_status: Novo status
            sheet_name: Nome da aba na planilha

        Returns:
            True se sucesso, False caso contrário
        """
        try:
            worksheet = self.get_worksheet(sheet_name)

            # Encontra a célula com o payment_id (coluna 7)
            cell = worksheet.find(payment_id)

            if cell:
                # Atualiza o status (coluna 8)
                worksheet.update_cell(cell.row, 8, new_status)
                return True

            return False

        except Exception as e:
            print(f"Erro ao atualizar status do pagamento: {str(e)}")
            return False

    def get_payment_by_id(
        self,
        payment_id: str,
        sheet_name: str = "Pagamentos"
    ) -> Optional[Dict[str, Any]]:
        """
        Busca um pagamento pelo ID.

        Args:
            payment_id: ID do pagamento
            sheet_name: Nome da aba na planilha

        Returns:
            Dicionário com os dados do pagamento ou None
        """
        try:
            worksheet = self.get_worksheet(sheet_name)

            # Encontra a célula com o payment_id
            cell = worksheet.find(payment_id)

            if cell:
                # Obtém toda a linha
                row = worksheet.row_values(cell.row)

                return {
                    "timestamp": row[0] if len(row) > 0 else None,
                    "file_id": row[1] if len(row) > 1 else None,
                    "file_name": row[2] if len(row) > 2 else None,
                    "page_count": int(row[3]) if len(row) > 3 else 0,
                    "amount": row[4] if len(row) > 4 else None,
                    "payment_method": row[5] if len(row) > 5 else None,
                    "payment_id": row[6] if len(row) > 6 else None,
                    "status": row[7] if len(row) > 7 else None,
                    "payer_email": row[8] if len(row) > 8 else None,
                }

            return None

        except Exception as e:
            print(f"Erro ao buscar pagamento: {str(e)}")
            return None

    def get_all_payments(
        self,
        sheet_name: str = "Pagamentos"
    ) -> List[Dict[str, Any]]:
        """
        Retorna todos os pagamentos.

        Args:
            sheet_name: Nome da aba na planilha

        Returns:
            Lista de dicionários com os pagamentos
        """
        try:
            worksheet = self.get_worksheet(sheet_name)

            # Obtém todos os registros (pula o cabeçalho)
            records = worksheet.get_all_records()

            return records

        except Exception as e:
            print(f"Erro ao buscar pagamentos: {str(e)}")
            return []

    def create_file_record(
        self,
        file_id: str,
        file_name: str,
        original_path: str,
        processed_path: Optional[str] = None,
        page_count: int = 0,
        status: str = "uploaded",
        sheet_name: str = "Arquivos"
    ) -> bool:
        """
        Cria um registro de arquivo na planilha.

        Args:
            file_id: ID do arquivo
            file_name: Nome do arquivo
            original_path: Caminho do arquivo original
            processed_path: Caminho do arquivo processado
            page_count: Número de páginas
            status: Status do processamento
            sheet_name: Nome da aba na planilha

        Returns:
            True se sucesso, False caso contrário
        """
        try:
            worksheet = self.get_worksheet(sheet_name)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = [
                timestamp,
                file_id,
                file_name,
                original_path,
                processed_path or "",
                str(page_count),
                status
            ]

            worksheet.append_row(row)
            return True

        except Exception as e:
            print(f"Erro ao criar registro de arquivo: {str(e)}")
            return False

    def update_file_status(
        self,
        file_id: str,
        new_status: str,
        processed_path: Optional[str] = None,
        page_count: Optional[int] = None,
        sheet_name: str = "Arquivos"
    ) -> bool:
        """
        Atualiza o status de processamento de um arquivo.

        Args:
            file_id: ID do arquivo
            new_status: Novo status
            processed_path: Caminho do arquivo processado
            page_count: Número de páginas
            sheet_name: Nome da aba na planilha

        Returns:
            True se sucesso, False caso contrário
        """
        try:
            worksheet = self.get_worksheet(sheet_name)

            # Encontra a célula com o file_id
            cell = worksheet.find(file_id)

            if cell:
                # Atualiza o status (coluna 7)
                worksheet.update_cell(cell.row, 7, new_status)

                # Atualiza o caminho processado se fornecido (coluna 5)
                if processed_path:
                    worksheet.update_cell(cell.row, 5, processed_path)

                # Atualiza o número de páginas se fornecido (coluna 6)
                if page_count is not None:
                    worksheet.update_cell(cell.row, 6, str(page_count))

                return True

            return False

        except Exception as e:
            print(f"Erro ao atualizar status do arquivo: {str(e)}")
            return False

    def setup_sheets(self):
        """
        Configura as planilhas iniciais com cabeçalhos.
        """
        try:
            # Configura planilha de Pagamentos
            try:
                payments_sheet = self.spreadsheet.worksheet("Pagamentos")
            except:
                payments_sheet = self.spreadsheet.add_worksheet(
                    title="Pagamentos",
                    rows="1000",
                    cols="10"
                )

            # Define cabeçalhos para Pagamentos
            headers_payments = [
                "Data/Hora",
                "ID Arquivo",
                "Nome Arquivo",
                "Páginas",
                "Valor",
                "Método",
                "ID Pagamento",
                "Status",
                "Email"
            ]

            # Verifica se já tem cabeçalho
            if not payments_sheet.row_values(1):
                payments_sheet.update('A1:I1', [headers_payments])

            # Configura planilha de Arquivos
            try:
                files_sheet = self.spreadsheet.worksheet("Arquivos")
            except:
                files_sheet = self.spreadsheet.add_worksheet(
                    title="Arquivos",
                    rows="1000",
                    cols="10"
                )

            # Define cabeçalhos para Arquivos
            headers_files = [
                "Data/Hora",
                "ID Arquivo",
                "Nome",
                "Caminho Original",
                "Caminho Processado",
                "Páginas",
                "Status"
            ]

            # Verifica se já tem cabeçalho
            if not files_sheet.row_values(1):
                files_sheet.update('A1:G1', [headers_files])

            print("Planilhas configuradas com sucesso!")
            return True

        except Exception as e:
            print(f"Erro ao configurar planilhas: {str(e)}")
            return False
