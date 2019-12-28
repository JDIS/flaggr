FROM nginx:stable-alpine
RUN apk add certbot gettext
RUN mkdir -p /var/www/html
COPY --from=frontend-user /app/dist /var/www/html
COPY --from=frontend-admin /app/dist /var/www/html/admin
COPY nginx.conf /etc/nginx/nginx-template.conf
COPY nginx-http.conf /etc/nginx/nginx-http.conf
COPY run.sh /
RUN chmod +x /run.sh
EXPOSE 80
EXPOSE 443
ENTRYPOINT ["/bin/sh", "/run.sh"]
