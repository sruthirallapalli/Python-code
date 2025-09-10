FROM python:3.8-slim
MAINTAINER sruthi
LABEL This is to deploy python project
WORKDIR /work
COPY requirements.txt /work
RUN pip install --no -cache -dir -r requirements.txt

COPY  . /work/
EXPOSE 5000
ENV FLASK_APP =app.py
CMD ["flask","run","-host","0.0.0.0"]

