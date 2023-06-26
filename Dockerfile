FROM python:3.9.6
LABEL authors="lingfengcoder@github.com"

#ENTRYPOINT ["top", "-b"]

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt

CMD ["python","/code/app.py"]

#CMD ["uvicorn","app:app","--reload" ]