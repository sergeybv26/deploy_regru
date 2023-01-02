"""По POST запросу от GitHub Actions выполняет синхронизацию изменений и перезапуск сервера Django"""
import json
import logging
import logging.config
import os

from aiohttp import web

log = logging.getLogger(__name__)


class DeployApi:
    """Получает запрос от скрипта GitHub Actions и выполняет обновление сервера"""

    def __init__(self, auth_token):
        self.token = auth_token

    async def deploy(self, request):
        if request.headers.get('Authorization') != self.token:
            return web.Response(text=json.dumps({'message': 'Bad token'}), status=401,
                                headers={"Access-Control-Allow-Origin": "*"},
                                content_type='application/json'
                                )

        log.debug(f'Recieved {request.data}')


def main():
    auth_token = os.getenv('CI_TOKEN', None)
    log_config = {
        "version": 1,
        "handlers": {
            "streamHandler": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "log_formatter",
                "level": "INFO"
            },
            "fileHandler": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "log_formatter",
                "filename": "bot.log",
                "maxBytes": 20000,
                "backupCount": 2,
                "encoding": "utf-8"
            }
        },
        "formatters": {
            "log_formatter": {
                "format": "%(asctime)s %(levelname)-8s %(filename)s %(message)s"
            }
        },
        "loggers": {
            "bot-helper": {
                "handlers": ["streamHandler", "fileHandler"],
                "level": "DEBUG"
            }
        }
    }
    logging.config.dictConfig(log_config)
