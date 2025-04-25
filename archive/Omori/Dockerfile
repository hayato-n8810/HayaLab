FROM python:3.13

RUN apt update && apt install -y\
  openjdk-17-jre\
  && apt clean

RUN cd /opt && wget "https://github.com/GumTreeDiff/gumtree/releases/download/v4.0.0-beta2/gumtree-4.0.0-beta2.zip"
RUN cd /opt && unzip "gumtree-4.0.0-beta2.zip"
RUN mv "/opt/gumtree-4.0.0-beta2" "/opt/gumtree"
ENV PATH=$PATH:/opt/gumtree/bin

COPY socsel.tar.gz /workspace/
RUN pip3 install /workspace/socsel.tar.gz
