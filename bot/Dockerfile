# Debian-based Linux operating system based on free software.
FROM ubuntu

# Install wkhtmltopdf
WORKDIR /root
RUN apt-get update && apt-get install -y wget xz-utils
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
RUN tar vxf wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
RUN cp wkhtmltox/bin/wk* /usr/local/bin

# Additional configuration or commands as needed