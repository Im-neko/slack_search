FROM python:3.7

RUN apt-get update
RUN apt-get -y install locales && \
  localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

WORKDIR /src

COPY ./crawler/pip-list.txt .

RUN pip install --upgrade pip
RUN pip install -r pip-list.txt

CMD ["python", "index.py"]
