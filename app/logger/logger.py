import os
import logging
from logging.handlers import TimedRotatingFileHandler


def configure_logging(app):
    # Crear la carpeta de logs si no existe
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Ruta base del archivo de logs
    log_file_path = os.path.join(log_directory, "log")

    # Eliminar todos los manejadores existentes del logger de la aplicación
    del app.logger.handlers[:]

    # Crear y configurar el manejador de consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # Filtrar para asegurar que WARNING, ERROR y CRITICAL aparezcan en consola
    class WarningErrorCriticalFilter(logging.Filter):
        def filter(self, record):
            return record.levelno >= logging.WARNING

    console_handler.addFilter(WarningErrorCriticalFilter())

    # Crear y configurar el manejador de archivo con rotación diaria
    file_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=30)
    file_handler.suffix = "%Y_%m_%d"  # Formato de fecha para el nombre del archivo, sin .txt
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # Agregar los manejadores configurados al logger de la aplicación
    app.logger.addHandler(console_handler)
    app.logger.addHandler(file_handler)

    # Establecer el nivel del logger de la aplicación al más bajo posible
    app.logger.setLevel(logging.DEBUG)

    # Desactivar la propagación para evitar que los logs se manejen por otros logger de Flask
    app.logger.propagate = False