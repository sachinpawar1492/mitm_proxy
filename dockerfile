#Deriving the latest base image
FROM python:3.10

#Labels as key value pair
LABEL Maintainer="Sachin Pawar <sachin.d.pawar@kpn.com>"

RUN apt-get update && apt-get install -y python3

WORKDIR /mitm_proxy

#to COPY the remote file at working directory in container
COPY . .

RUN pip install pipenv
RUN pipenv install --system --deploy
