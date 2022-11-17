FROM i386/redis
RUN echo 'deb http://deb.debian.org/debian sid main contrib non-free' > /etc/apt/sources.list.d/sid.list
RUN apt update
RUN apt install libc6 python3 python3-pip wget -y
RUN pip3 install redis_om
RUN wget -q 'https://github.com/JingMatrix/Alibrary/releases/download/v1.0/archive.rdb' -O /archive.rdb
RUN wget -q 'https://github.com/JingMatrix/Alibrary/releases/download/v0.2/redisearch-linux-x32.so' -O /redisearch.so
RUN chmod +x /redisearch.so
COPY search.py type.py /

CMD python3 /search.py
