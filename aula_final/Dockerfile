FROM vulnerables/web-dvwa
RUN sed -i 's/LogLevel warn/LogLevel info/' /etc/apache2/apache2.conf && \
    echo 'LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\" \"%{cookie}n\" \"%{PHPSESSID}C\"" combined' >> /etc/apache2/apache2.conf && \
    echo 'CustomLog ${APACHE_LOG_DIR}/access.log combined' >> /etc/apache2/apache2.conf
VOLUME /var/log/apache2
EXPOSE 80
CMD ["/run.sh"]

