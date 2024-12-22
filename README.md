# Test-job
# Установка Docker и Docker Compose

# Обновляем пакеты и устанавливаем необходимые зависимости
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Добавляем ключ и репозиторий Docker
curl -fsSL https://get.docker.com | sudo bash

# Устанавливаем Docker
sudo apt install docker-ce

# Проверяем установку Docker
sudo docker --version

# Устанавливаем Docker Compose
sudo apt install docker-compose

# Проверяем установку Docker Compose
docker-compose --version


# 1. Контейнеризация веб-приложения с Docker

# Устанавливаем Python 3 и pip
sudo apt install python3-pip

# Создаём директорию для приложения
mkdir /home/sadmin/flask-app
cd /home/sadmin/flask-app

# Создаём файл app.py
echo -e 'from flask import Flask\n\napp = Flask(__name__)\n\n@app.route("/")\ndef hello_world():\n    return "Hello, World!"\n\nif __name__ == "__main__":\n    app.run(host="0.0.0.0", port=5000)' > app.py

# Создаём файл requirements.txt
echo 'flask' > requirements.txt

# Создаём Dockerfile
echo -e 'FROM python:3.9\n\nWORKDIR /app\n\nCOPY requirements.txt /app/\n\nRUN pip install --no-cache-dir -r requirements.txt\n\nCOPY . /app/\n\nCMD ["python", "app.py"]' > Dockerfile

# Создаём docker-compose.yml
echo -e 'version: "3"\nservices:\n  flask-app:\n    build: .\n    ports:\n      - "5000:5000"' > docker-compose.yml

# Запускаем контейнеры с помощью docker-compose
docker-compose up -d

# Открываем приложение в браузере на http://localhost:5000


# 2. Настройка Nginx как reverse proxy

# Создаём директорию для конфигурации Nginx
mkdir /home/sadmin/nginx

# Создаём конфигурационный файл Nginx
echo -e 'server {\n    listen 80;\n\n    location / {\n        proxy_pass http://flask-app:5000;\n        proxy_set_header Host $host;\n        proxy_set_header X-Real-IP $remote_addr;\n        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n        proxy_set_header X-Forwarded-Proto $scheme;\n    }\n}' > /home/sadmin/nginx/default.conf

# Создаём Dockerfile для Nginx
echo -e 'FROM nginx:latest\nCOPY nginx/default.conf /etc/nginx/conf.d/' > /home/sadmin/nginx/Dockerfile

# Обновляем docker-compose.yml для использования Nginx
echo -e 'version: "3"\nservices:\n  flask-app:\n    build: ./flask-app\n    ports:\n      - "5000:5000"\n  nginx:\n    build: ./nginx\n    ports:\n      - "80:80"\n    depends_on:\n      - flask-app' > docker-compose.yml

# Перезапускаем docker-compose
docker-compose up -d


# 3. Настройка CI/CD пайплайна с Jenkins

# Устанавливаем Jenkins на сервере
sudo apt install openjdk-11-jdk
wget -q -O - https://pkg.jenkins.io/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian/ stable main > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install jenkins

# Запускаем Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Открываем Jenkins в браузере
echo "Jenkins is available at http://localhost:8080"
echo "Unlock Jenkins using the following command:"
sudo cat /var/lib/jenkins/secrets/initialAdminPassword

# Вводим пароль в веб-интерфейсе Jenkins и выполняем настройку

# Создаём файл Jenkinsfile для автоматической сборки и деплоя
echo -e 'pipeline {\n    agent any\n    stages {\n        stage("Build") {\n            steps {\n                script {\n                    sh "docker-compose build"\n                }\n            }\n        }\n        stage("Deploy") {\n            steps {\n                script {\n                    sh "docker-compose up -d"\n                }\n            }\n        }\n    }\n}' > /home/sadmin/jenkins/Jenkinsfile

# Добавляем файл Jenkinsfile в репозиторий и настраиваем Jenkins для отслеживания изменений в GitHub


# 4. Мониторинг и логирование

# Создаём директорию для логов
mkdir /home/sadmin/flask-app/logs
mkdir /home/sadmin/nginx/logs

# Обновляем конфигурацию docker-compose.yml для монтирования логов
echo -e 'version: "3"\nservices:\n  flask-app:\n    build: ./flask-app\n    ports:\n      - "5000:5000"\n    volumes:\n      - ./logs:/app/logs\n  nginx:\n    build: ./nginx\n    ports:\n      - "80:80"\n    depends_on:\n      - flask-app\n    volumes:\n      - ./logs:/var/log/nginx' > docker-compose.yml

# Перезапускаем контейнеры
docker-compose up -d

# Проверяем логи приложения Flask
tail -f ./logs/access.log ./logs/error.log

