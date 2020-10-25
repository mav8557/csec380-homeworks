FROM php:fpm
RUN docker-php-ext-install mysqli
RUN docker-php-ext-enable mysqli

COPY ./armbook /usr/share/nginx/html/armbook

EXPOSE 9000
