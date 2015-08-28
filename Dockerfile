FROM debian:latest

MAINTAINER Chris Wolfe

# patch the base image
RUN apt-get update --yes
RUN apt-get dist-upgrade --yes

# install some dependencies
RUN apt-get install cython --yes
RUN apt-get install python-pip --yes

RUN pip install --upgrade pip

ADD . /twisted_wsgi_nr
WORKDIR /twisted_wsgi_nr

RUN python setup.py install

EXPOSE 8713

ENTRYPOINT ["pleasework"]
