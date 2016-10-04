FROM jupiterapp/backend:initial

ENV BACKEND_PATH /backend
WORKDIR ${BACKEND_PATH}
COPY . ${BACKEND_PATH}

RUN apt-get -y install netcat libpq-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ${BACKEND_PATH}/init/entry.sh