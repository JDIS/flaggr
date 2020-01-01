if [ ! -z "${DOMAIN}" ]; then

  echo 'USING HTTPS WITH DOMAIN ${DOMAIN}'

  if [ ! -f /etc/letsencrypt/$DOMAIN/fullchain.pem ]; then
    certbot certonly -n --agree-tos -m=egg997@gmail.com -d $DOMAIN --standalone
  else
    certbot renew
  fi

  echo 'GENERATING NGINX CONF FILE'
  envsubst '${DOMAIN}' < /etc/nginx/nginx-template.conf > /etc/nginx/nginx.conf
  echo 'STARTING NGINX'

  nginx -g "daemon off;"

else

  echo 'NOT USING HTTPS BECAUSE $DOMAIN IS NOT SET, FALLBACK TO HTTP'

  nginx -g "daemon off;" -c /etc/nginx/nginx-http.conf

fi
