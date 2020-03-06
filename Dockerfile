FROM centos:centos7
MAINTAINER YAM Technology <itsupport@yamholdings.com>

RUN groupadd pybot && \
    adduser pybot -g pybot

ENV USER_TOKEN ""
ENV BOT_TOKEN ""

RUN yum install -y \
      bash \
      # required for slack client pip package
      build-base \
      python3 \
      py3-pip

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
RUN mkdir /etc/pybot

COPY ./*.py /etc/pybot/

WORKDIR /etc/pybot/
USER pybot

CMD ["python3", "./rtm.py"]
