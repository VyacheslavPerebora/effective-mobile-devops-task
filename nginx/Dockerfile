FROM nginx:alpine

# Удаляем дефолтную конфигурацию nginx
RUN rm /etc/nginx/conf.d/default.conf

# Копируем нашу кастомную конфигурацию
COPY nginx.conf /etc/nginx/nginx.conf