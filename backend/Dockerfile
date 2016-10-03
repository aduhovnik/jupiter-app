FROM jupiterapp/backend:initial

COPY . /backend
WORKDIR /backend
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ./manage.py runserver 0.0.0.0:8000