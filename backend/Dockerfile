# Используем официальный минимальный образ Python
# alpine - облегченная версия Linux, образ весит ~50MB вместо ~900MB
FROM python:3.11-alpine

# Метаданные образа
LABEL maintainer="kulttura.hardware@gmail.com"
LABEL description="Simple Python HTTP server for Effective Mobile test task"

# Создаем непривилегированного пользователя для запуска приложения
# Это повышает безопасность - приложение не работает от root
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

WORKDIR /app

# Копируем файл приложения в контейнер
# Используем --chown для назначения владельца сразу при копировании
COPY --chown=appuser:appuser app.py .

# Переключаемся на непривилегированного пользователя
USER appuser

# Документируем, что приложение слушает порт 8080
EXPOSE 8080

# Используем exec form (JSON array) для корректной передачи сигналов
CMD ["python3", "app.py"]