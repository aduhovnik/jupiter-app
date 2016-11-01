FROM jupiterapp/frontend:initial

COPY ./data /frontend/data
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/conf.d/ /etc/nginx/conf.d/
CMD nginx
