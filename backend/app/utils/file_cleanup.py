"""
File Cleanup Utility
Sistema de limpeza automática de arquivos temporários.
"""

import os
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import List
import logging

from ..core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class FileCleanupService:
    """Serviço de limpeza de arquivos temporários."""

    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.processed_dir = Path(settings.PROCESSED_DIR)
        self.retention_hours = settings.FILE_RETENTION_HOURS

    def cleanup_old_files(self) -> dict:
        """
        Remove arquivos mais antigos que o tempo de retenção.

        Returns:
            Estatísticas da limpeza
        """
        stats = {
            "uploads_deleted": 0,
            "processed_deleted": 0,
            "total_size_freed": 0,
            "errors": []
        }

        # Calcula data limite
        cutoff_time = datetime.now() - timedelta(hours=self.retention_hours)
        cutoff_timestamp = cutoff_time.timestamp()

        # Limpa uploads
        if self.upload_dir.exists():
            stats["uploads_deleted"], freed = self._cleanup_directory(
                self.upload_dir, cutoff_timestamp
            )
            stats["total_size_freed"] += freed

        # Limpa processados
        if self.processed_dir.exists():
            stats["processed_deleted"], freed = self._cleanup_directory(
                self.processed_dir, cutoff_timestamp
            )
            stats["total_size_freed"] += freed

        logger.info(
            f"Limpeza concluída: {stats['uploads_deleted'] + stats['processed_deleted']} "
            f"arquivos removidos, {stats['total_size_freed'] / 1024 / 1024:.2f} MB liberados"
        )

        return stats

    def _cleanup_directory(self, directory: Path, cutoff_timestamp: float) -> tuple:
        """
        Limpa arquivos antigos de um diretório.

        Args:
            directory: Diretório para limpar
            cutoff_timestamp: Timestamp de corte

        Returns:
            Tupla (arquivos_deletados, bytes_liberados)
        """
        deleted_count = 0
        size_freed = 0

        try:
            for file_path in directory.iterdir():
                if file_path.is_file():
                    try:
                        # Verifica idade do arquivo
                        file_mtime = file_path.stat().st_mtime

                        if file_mtime < cutoff_timestamp:
                            # Remove arquivo
                            file_size = file_path.stat().st_size
                            file_path.unlink()

                            deleted_count += 1
                            size_freed += file_size

                            logger.debug(f"Arquivo removido: {file_path}")

                    except Exception as e:
                        logger.error(f"Erro ao remover {file_path}: {str(e)}")

        except Exception as e:
            logger.error(f"Erro ao acessar diretório {directory}: {str(e)}")

        return deleted_count, size_freed

    def cleanup_specific_file(self, file_id: str) -> bool:
        """
        Remove arquivos específicos associados a um file_id.

        Args:
            file_id: ID do arquivo

        Returns:
            True se removido com sucesso
        """
        success = True

        # Busca e remove arquivos com o file_id
        for directory in [self.upload_dir, self.processed_dir]:
            if directory.exists():
                for file_path in directory.glob(f"{file_id}*"):
                    try:
                        file_path.unlink()
                        logger.info(f"Arquivo removido: {file_path}")
                    except Exception as e:
                        logger.error(f"Erro ao remover {file_path}: {str(e)}")
                        success = False

        return success

    def get_directory_stats(self) -> dict:
        """
        Obtém estatísticas dos diretórios.

        Returns:
            Estatísticas
        """
        stats = {
            "upload_dir": self._get_dir_stats(self.upload_dir),
            "processed_dir": self._get_dir_stats(self.processed_dir),
        }

        return stats

    def _get_dir_stats(self, directory: Path) -> dict:
        """
        Obtém estatísticas de um diretório.

        Args:
            directory: Diretório

        Returns:
            Estatísticas
        """
        if not directory.exists():
            return {"exists": False, "file_count": 0, "total_size": 0}

        file_count = 0
        total_size = 0

        for file_path in directory.iterdir():
            if file_path.is_file():
                file_count += 1
                total_size += file_path.stat().st_size

        return {
            "exists": True,
            "file_count": file_count,
            "total_size": total_size,
            "total_size_mb": round(total_size / 1024 / 1024, 2)
        }


def schedule_cleanup_task():
    """
    Função para agendar limpeza periódica.
    Pode ser executada via Celery ou cron.
    """
    service = FileCleanupService()
    stats = service.cleanup_old_files()

    logger.info(f"Limpeza agendada concluída: {stats}")

    return stats


# Para execução standalone
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("Iniciando limpeza de arquivos...")
    service = FileCleanupService()

    # Mostra estatísticas atuais
    print("\nEstatísticas antes da limpeza:")
    stats_before = service.get_directory_stats()
    print(f"Upload: {stats_before['upload_dir']['file_count']} arquivos, "
          f"{stats_before['upload_dir']['total_size_mb']} MB")
    print(f"Processados: {stats_before['processed_dir']['file_count']} arquivos, "
          f"{stats_before['processed_dir']['total_size_mb']} MB")

    # Executa limpeza
    cleanup_stats = service.cleanup_old_files()

    print("\nResultado da limpeza:")
    print(f"Uploads removidos: {cleanup_stats['uploads_deleted']}")
    print(f"Processados removidos: {cleanup_stats['processed_deleted']}")
    print(f"Espaço liberado: {cleanup_stats['total_size_freed'] / 1024 / 1024:.2f} MB")

    # Mostra estatísticas finais
    print("\nEstatísticas após limpeza:")
    stats_after = service.get_directory_stats()
    print(f"Upload: {stats_after['upload_dir']['file_count']} arquivos, "
          f"{stats_after['upload_dir']['total_size_mb']} MB")
    print(f"Processados: {stats_after['processed_dir']['file_count']} arquivos, "
          f"{stats_after['processed_dir']['total_size_mb']} MB")
