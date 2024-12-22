from flask import Flask
import logging
import sys

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Устанавливаем уровень логирования на INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат вывода
    handlers=[
        logging.StreamHandler(sys.stdout),  # Логируем в stdout, чтобы Docker собрал логи
        logging.FileHandler('/app/logs/flask_app.log')  # Логируем также в файл внутри контейнера
    ]
)

@app.route('/')
def hello_world():
    app.logger.info("Hello world route accessed")  # Логируем доступ к маршруту
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

