"""По POST запросу от GitHub Actions выполняет синхронизацию изменений и перезапуск сервера Django"""
import logging
import logging.config
import subprocess
import sys

from environs import Env
from flask import Flask, request, jsonify

log = logging.getLogger(__name__)

application = Flask(__name__)
env = Env()
env.read_env()
auth_token = env('CI_TOKEN', None)


def deploy_test_server():
    changedir = subprocess.run(['cd $HOME/www/test.derzn.ru/dz/'], stdout=subprocess.PIPE, text=True)
    log.info(changedir.stdout)
    project_pull = subprocess.run(['git pull'], stdout=subprocess.PIPE, text=True)
    log.info(project_pull.stdout)
    activate_env = subprocess.run(['source $HOME/www/test.derzn.ru/venv/bin/activate'], stdout=subprocess.PIPE, text=True)
    log.info(activate_env.stdout)
    migrate = subprocess.run(['./manage.py migrate'], stdout=subprocess.PIPE, text=True)
    log.info(migrate.stdout)
    restart_server = subprocess.run(['touch $HOME/www/test.derzn.ru/.restart-app'],  stdout=subprocess.PIPE, text=True)
    log.info(restart_server.stdout)
    return {'status': True}, 200


@application.route("/", methods=['POST'])
def deploy_handler():
    if request.headers.get('Authorization') != auth_token:
        return jsonify({'message': 'Bad token'}), 401

    if request.method == 'POST':
        log.debug(f'Recieved {request.data}')
        result, status = deploy_test_server()
        return jsonify(result), status


def main():
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

    if not auth_token:
        log.error('There is no auth token in env')
        sys.exit(1)
    application.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()