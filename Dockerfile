FROM python:3.5

WORKDIR /usr/src/api

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./manage.py runserver"]

