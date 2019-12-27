FROM nginx:stable-alpine
RUN mkdir -p /var/log/nginx
RUN mkdir -p /var/www/html
COPY --from=frontend-user /app/dist /var/www/html
COPY --from=frontend-admin /app/dist /var/www/html/admin
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf
RUN chown nginx:nginx /var/www/html
EXPOSE 80
EXPOSE 443
CMD ["nginx", "-g", "daemon off;"]