FROM python:3.12

WORKDIR /pdf-tool

COPY . .

RUN pip install -r requirements.txt

CMD ["flask", "--app", "/pdf-tool/src", "run", "--host=0.0.0.0", "--port=80"]