FROM nginx:alpine

# Удаляем дефолтную конфигурацию nginx
RUN rm /etc/nginx/conf.d/default.conf

# Копируем шаблон конфигурации (официальный образ автоматически обработает .template файлы)
COPY nginx.conf.template /etc/nginx/templates/nginx.conf.template