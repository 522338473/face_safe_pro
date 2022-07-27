FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Shanghai

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y gcc procps net-tools apt-utils libpq-dev \
    && ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone \
    && pip install pipenv==2020.11.15 -i https://mirrors.aliyun.com/pypi/simple/

WORKDIR /app

COPY . /app

RUN pipenv sync  && pipenv install --dev

RUN chmod +x /app/start.sh

CMD ["sh", "start.sh"]
