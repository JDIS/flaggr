# from https://fr.vuejs.org/v2/cookbook/dockerize-vuejs-app.html
# étape de build
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# étape de production
FROM nginx:stable-alpine as production-stage
RUN mkdir -p /var/log/nginx
RUN mkdir -p /var/www/html
COPY --from=build-stage /app/dist /var/www/html
COPY nginx_config/nginx.conf /etc/nginx/nginx.conf
COPY nginx_config/default.conf /etc/nginx/conf.d/default.conf
RUN chown nginx:nginx /var/www/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]