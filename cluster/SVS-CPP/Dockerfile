FROM ubuntu:noble


RUN apt update && \
    apt install -y git build-essential libboost-all-dev libssl-dev libsqlite3-dev pkg-config python3

RUN git clone https://github.com/named-data/ndn-cxx/ && \
    cd ndn-cxx && \
    ./waf configure && \
    ./waf && \
    ./waf install && \
    ldconfig

COPY ndn-svs /ndn-svs

RUN cd ndn-svs && \
    ./waf configure --enable-static --disable-shared --with-examples && \
    ./waf


