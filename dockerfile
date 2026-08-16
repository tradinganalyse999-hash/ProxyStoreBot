FROM dunglas/frankenphp:1-php8.2
RUN install-php-extensions bcmath gd zip curl mbstring intl pdo_mysql
COPY . /app
WORKDIR /app
