FROM python:3.9.6-alpine
LABEL authors="lingfengcoder@github.com"

ADD . /code

WORKDIR /code

RUN pip install --no-cache-dir -r  requirements.txt

CMD ["python3","app.py"]

#CMD ["uvicorn","app:app","--reload" ]