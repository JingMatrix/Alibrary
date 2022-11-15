FROM ubuntu
RUN apt update
COPY redis-tools.deb redis-server.deb /
RUN apt install /redis-tools.deb /redis-server.deb -y
RUN apt install python3 python3-pip -y
RUN pip3 install aligo redis_om
COPY archive.rdb redisearch-x64.so /
COPY backend.py relay.py type.py /
RUN mkdir -p $HOME/.aligo
COPY aligo.json /
RUN cp /aligo.json $HOME/.aligo

CMD redis-server --dir / --dbfilename archive.rdb --loadmodule /redisearch-x64.so --daemonize yes && python3 /backend.py
