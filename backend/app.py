#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import os

# Настройка логирования
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SimpleHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        # Healthcheck endpoint (без логирования, для мониторинга)
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK\n")
            return
        
        
        client_ip = self.headers.get('X-Real-IP', self.client_address[0])
        forwarded_for = self.headers.get('X-Forwarded-For', 'N/A')
        
        logging.info(
            f"Запрос: {self.path} | "
            f"Client IP: {client_ip} | "
            f"X-Forwarded-For: {forwarded_for}"
        )
        
        self.send_response(200)
        
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('X-Backend-Server', 'Python-HTTP-Server')
        self.end_headers()
        
        response = "Hello from Effective Mobile!\n"
        self.wfile.write(response.encode('utf-8'))
    
    def log_message(self, format, *args):
        """
        Переопределяем стандартное логирование BaseHTTPRequestHandler.
        Используем logging.debug() для контроля через LOG_LEVEL.
        Это убирает дублирование логов и дает единый формат.
        """
        logging.debug(f"{self.address_string()} - {format % args}")


def run_server(host='0.0.0.0', port=None):
    """
    Запуск HTTP-сервера.
    
    Args:
        host: IP-адрес для прослушивания (0.0.0.0 = все интерфейсы)
        port: Порт для прослушивания (из переменной окружения APP_PORT)
    """
   
    if port is None:
        port = int(os.getenv('APP_PORT', '8080'))
    
    server_address = (host, port)
    httpd = HTTPServer(server_address, SimpleHandler)
    
    logging.info("=== Effective Mobile Backend ===")
    logging.info(f"Сервер запущен на {host}:{port}")
    logging.info(f"Log Level: {LOG_LEVEL}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("\nОстановка сервера...")
        httpd.server_close()
        logging.info("Сервер остановлен")


if __name__ == '__main__':
    run_server()