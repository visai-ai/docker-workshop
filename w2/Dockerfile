FROM python:3.6-slim-buster

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 4000

CMD [ "python3", "-m" , "flask", "run", "--port=4000", "--host=0.0.0.0"]