#!/usr/bin/env python3
"""
Script para configurar as planilhas do Google Sheets.
Execute este script após configurar as credenciais do Google Cloud.
"""

import sys
import os

# Adiciona o diretório do app ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.sheets_service import SheetsService


def main():
    """Configura as planilhas do Google Sheets."""
    print("=" * 60)
    print("SETUP DO GOOGLE SHEETS - ABNT Formatador")
    print("=" * 60)
    print()

    try:
        print("1. Conectando ao Google Sheets...")
        sheets_service = SheetsService()
        print("   ✓ Conexão estabelecida com sucesso!")
        print()

        print("2. Configurando planilhas...")
        if sheets_service.setup_sheets():
            print("   ✓ Planilhas configuradas com sucesso!")
        else:
            print("   ✗ Erro ao configurar planilhas")
            return False
        print()

        print("=" * 60)
        print("CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print()
        print("As seguintes abas foram criadas/configuradas:")
        print("  • Pagamentos - Registros de transações")
        print("  • Arquivos - Registros de uploads e processamentos")
        print()
        print("Você pode acessar a planilha em:")
        print(f"https://docs.google.com/spreadsheets/d/{sheets_service.settings.GOOGLE_SHEETS_SPREADSHEET_ID}")
        print()

        return True

    except FileNotFoundError as e:
        print()
        print("✗ ERRO: Arquivo de credenciais não encontrado!")
        print()
        print("Certifique-se de que o arquivo 'google_credentials.json' está")
        print("no diretório 'backend/' do projeto.")
        print()
        print("Veja GOOGLE_SHEETS_SETUP.md para instruções de como obter")
        print("as credenciais do Google Cloud.")
        return False

    except Exception as e:
        print()
        print(f"✗ ERRO: {str(e)}")
        print()
        print("Verifique se:")
        print("  1. O arquivo google_credentials.json está correto")
        print("  2. O ID da planilha no .env está correto")
        print("  3. A service account tem permissão para acessar a planilha")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
