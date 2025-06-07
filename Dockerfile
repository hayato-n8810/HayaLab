FROM python:3.12-slim
WORKDIR /opt

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    openjdk-17-jre \
    && wget "https://github.com/GumTreeDiff/gumtree/releases/download/v4.0.0-beta2/gumtree-4.0.0-beta2.zip" \
    && unzip "gumtree-4.0.0-beta2.zip" \
    && mv "gumtree-4.0.0-beta2" "gumtree" \
    && rm gumtree-4.0.0-beta2.zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH=$PATH:/opt/gumtree/bin

COPY socsel.tar.gz /works/
RUN pip3 install /works/socsel.tar.gz

WORKDIR /works

EXPOSE 4567