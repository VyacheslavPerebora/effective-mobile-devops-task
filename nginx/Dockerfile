FROM nginx:alpine

# Удаляем дефолтную конфигурацию nginx
RUN rm /etc/nginx/conf.d/default.conf

# Копируем основную конфигурацию
COPY nginx.conf /etc/nginx/nginx.conf

# Копируем шаблон сервера (официальный образ автоматически обработает .template файлы)
COPY nginx.conf.template /etc/nginx/templates/server.conf.template