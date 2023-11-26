FROM python:3.9.6
LABEL authors="lingfengcoder@github.com"

#ENTRYPOINT ["top", "-b"]

ADD . /code

WORKDIR /code

RUN pip install --no-cache-dir -r  requirements.txt

#CMD ["python","/code/app.py"]

CMD ["python3","app.py"]