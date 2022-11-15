FROM ubuntu
RUN apt update
RUN apt install python3 python3-pip wget -y
RUN pip3 install redis_om
RUN wget -q 'http://mirrors.edge.kernel.org/ubuntu/pool/universe/r/redis/redis-server_7.0.4-1_amd64.deb'
RUN wget -q 'http://mirrors.edge.kernel.org/ubuntu/pool/universe/r/redis/redis-tools_7.0.4-1_amd64.deb'
RUN apt install /redis*.deb -y
RUN wget -q 'https://github.com/JingMatrix/Alibrary/releases/download/v0.3/archive.rdb'
RUN wget -q 'https://github.com/JingMatrix/Alibrary/releases/download/v0.2/redisearch-linux-x64.so'
COPY search.py type.py /

CMD redis-server --dir / --dbfilename archive.rdb --loadmodule /redisearch-linux-x64.so --daemonize yes && python3 /search.py
