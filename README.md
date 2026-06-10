# Effective Mobile DevOps Task

> Простое веб-приложение с Python backend и Nginx reverse proxy, развернутое в Docker-контейнерах

## 📋 Содержание

- [Архитектура приложения](#архитектура-приложения)
- [Особенности безопасности](#особенности-безопасности)
- [Пошаговая инструкция запуска](#пошаговая-инструкция-запуска)
- [Проверка работоспособности](#проверка-работоспособности)
- [Схема взаимодействия](#схема-взаимодействия)
- [Использованные технологии](#использованные-технологии)
- [Структура проекта](#структура-проекта)

---

## 🏗️ Архитектура приложения

Приложение состоит из двух Docker-контейнеров, взаимодействующих через изолированную сеть:

| Компонент | Описание | Порт | Доступность |
|-----------|----------|------|-------------|
| **Backend** | Python HTTP-сервер | 8080 | Только внутри Docker-сети |
| **Nginx** | Reverse proxy | 80 | Публичный доступ |

### Поток запросов

1. Клиент отправляет HTTP-запрос на `http://localhost:80`
2. Nginx принимает запрос и проксирует его на `http://backend:8080`
3. Backend обрабатывает запрос и возвращает ответ "Hello from Effective Mobile!"
4. Nginx передаёт ответ клиенту

---

## 🔒 Особенности безопасности

- ✅ Backend изолирован — порт 8080 не публикуется наружу
- ✅ Backend работает от непривилегированного пользователя (не root)
- ✅ Используются минимальные Alpine-образы (~50MB суммарно)
- ✅ Nginx скрывает свою версию (`server_tokens off`)
- ✅ Передаются стандартные заголовки (X-Real-IP, X-Forwarded-For, Host)
- ✅ Healthcheck для обоих контейнеров

---


## 🚀 Пошаговая инструкция запуска

### Шаг 1: Предварительные требования

Убедитесь, что установлены:

- Docker версии **20.10** или выше
- Docker Compose версии **2.0** или выше

**Проверка версий:**

```bash
docker --version
docker compose version
```

### Шаг 2: Клонирование репозитория

```bash
git clone https://github.com/VyacheslavPerebora/effective-mobile-devops-task.git
cd effective-mobile-devops-task
```

### Шаг 3: Настройка переменных окружения

Создайте файл `.env` из шаблона:

```bash
cp .env.example .env
```

По умолчанию используются следующие значения (можно оставить без изменений):

```env
BACKEND_PORT=8080
NGINX_HOST_PORT=80
BACKEND_SERVICE=backend
NETWORK_NAME=eldabaof-mobile-network
LOG_LEVEL=info
```

### Шаг 4: Запуск приложения

```bash
docker compose up -d --build
```

**Параметры:**
- `-d` — запуск в фоновом режиме (daemon)
- `--build` — пересборка образов при изменениях

**Ожидаемый вывод:**

```
[+] Building 15.2s (12/12) FINISHED
[+] Running 3/3
 ✔ Network effective-mobile-network    Created
 ✔ Container effective-mobile-backend  Healthy
 ✔ Container effective-mobile-nginx    Started
```

### Шаг 5: Проверка статуса контейнеров

```bash
docker compose ps
```

**Ожидаемый вывод:**

```
NAME                          STATUS          PORTS
effective-mobile-backend      Up (healthy)    
effective-mobile-nginx        Up (healthy)    0.0.0.0:80->80/tcp
```

> ⚠️ **Примечание:** Оба контейнера должны иметь статус `healthy` (может потребоваться 10-30 секунд после запуска).

---


## ✅ Проверка работоспособности

### 1. Основная проверка

```bash
curl http://localhost
```

**Ожидаемый результат:**

```
Hello from Effective Mobile!
```

### 2. Проверка изоляции backend

Backend не должен быть доступен напрямую:

```bash
curl http://localhost:8080
```

**Ожидаемый результат:**

```
curl: (7) Failed to connect to localhost port 8080: Connection refused
```

### 3. Проверка healthcheck nginx

```bash
curl http://localhost/nginx-health
```

**Ожидаемый результат:**

```
Nginx is healthy
```

### 3. Проверка healthcheck backend

```bash
curl http://localhost/health
```

**Ожидаемый результат:**

```
OK

```

---



## 📊 Схема взаимодействия

```
                +-------------------+
                |       Client      |
                +-------------------+
                          |
                          v
                +-------------------+
                |   Nginx (port 80) |
                |   Reverse Proxy   |
                +-------------------+
                          |
                          v
                +-------------------+
                | Backend (8080)    |
                | Python HTTPServer |
                +-------------------+
```

---


## 🛠️ Использованные технологии

| Компонент | Технология | Версия |
|-----------|------------|--------|
| **Backend** | Python | 3.11-alpine |
| **HTTP Server** | http.server | stdlib |
| **Reverse Proxy** | Nginx | alpine |
| **Контейнеризация** | Docker | 20.10+ |
| **Оркестрация** | Docker Compose | v2 |
| **Базовая ОС** | Alpine Linux | 3.x |

---



## 📁 Структура проекта

```
effective-mobile-devops-task/
│
├── backend/
│   ├── .dockerignore           # Игнорируемые файлы для сборки backend образа
│   ├── app.py                  # Код Python приложения (stdlib only)
│   └── Dockerfile              # Образ Python HTTP-сервера
│
├── nginx/
│   ├── .dockerignore           # Игнорируемые файлы для сборки nginx образа
│   ├── Dockerfile              # Образ Nginx с поддержкой переменных окружения
│   ├── nginx.conf              # Основная конфигурация Nginx
│   └── nginx.conf.template     # Шаблон сервера reverse proxy с переменными
│
├── docker-compose.yml          # Оркестрация Docker сервисов
│
├── .env                        # Переменные окружения (не коммитится в Git)
├── .env.example                # Шаблон переменных окружения
│
├── .gitignore                  # Игнорируемые файлы для Git
└── README.md                   # Документация проекта
```

---



## 📝 Дополнительные команды

### Остановка приложения

```bash
docker compose down
```

### Просмотр логов

```bash
# Все сервисы
docker compose logs -f

# Только backend
docker compose logs -f backend

# Только nginx
docker compose logs -f nginx
```

### Пересборка образов

```bash
docker compose build --no-cache
```

### Очистка ресурсов

```bash
# Остановка и удаление контейнеров, сетей
docker compose down

```