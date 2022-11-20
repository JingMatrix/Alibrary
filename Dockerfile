FROM ubuntu/postgres
RUN apt update
RUN apt install git -y
RUN apt install wget cmake -y
RUN apt install python3-pip -y
RUN apt install postgresql-server-dev-all  -y
RUN pip3 install psycopg2
RUN pg_createcluster 14 main
RUN git clone --depth 1 https://github.com/JingMatrix/Alibrary
RUN wget -q https://github.com/JingMatrix/Alibrary/releases/download/v2.0/alibrary.sql -O /alibrary.sql
RUN git clone --shallow-submodules --recursive --depth 1 https://github.com/JingMatrix/pg_jieba
RUN cd /pg_jieba  && cmake -B build -S . -DPostgreSQL_TYPE_INCLUDE_DIR=/usr/include/postgresql/14/server && make -C build install
RUN pg_ctlcluster --skip-systemctl-redirect 14 main start && su postgres -c 'createuser -s root'  && createdb alibrary && psql alibrary < /alibrary.sql
RUN rm /Alibrary/relay.py

CMD pg_ctlcluster --skip-systemctl-redirect 14 main start && python3 /Alibrary/search.py
