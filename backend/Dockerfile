FROM python:3.5

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8888

CMD python app.py