FROM python:3.13

RUN apt-get update && apt-get install -y wget unzip \
    && cd /opt && wget "https://github.com/GumTreeDiff/gumtree/releases/download/v4.0.0-beta2/gumtree-4.0.0-beta2.zip"\
    && cd /opt && unzip "gumtree-4.0.0-beta2.zip"\
    && mv "/opt/gumtree-4.0.0-beta2" "/opt/gumtree"\
    && rm -f /opt/gumtree-4.0.0-beta2.zip \
    && apt-get clean \
    && apt-get purge -y wget unzip \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

ENV PATH=$PATH:/opt/gumtree/bin

WORKDIR /works