FROM jupiterapp/frontend:initial

COPY ./app /frontend/app
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/conf.d/ /etc/nginx/conf.d/

WORKDIR /frontend/app
RUN npm install -s

CMD nginx
