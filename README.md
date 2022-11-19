# Alibrary

Database toolkit for aliyundrive share links

## Goals

Currently, many people share huge pack of files via [阿里云盘](https://www.aliyundrive.com/).
For example, one can find such share links in [UP云搜](https://www.upyunso.com/), [万人迷吧](https://wanrenmi8.com/cn/index.html), [找资源](https://zhaoziyuan.la/) and [云盘资源网](https://www.yunpanziyuan.com/).
Given those abundant resources, we create [Alibrary](https://github.com/JingMatrix/Alibrary) project to index and update shared files.
This project _SHOULD_ reach the following goals:
1. store index data reliably;
2. provide rapid search API;
3. update and validate share links efficiently.

## Dependencies

We use the following projects:
1. [aligo](https://github.com/foyoux/aligo), `python3` API of aliyundrive,
2. [PostgreSQL](https://www.postgresql.org/) with full-text search extension [pg_jieba](https://github.com/JingMatrix/pg_jieba), database storage with Chinese segemntation,
3. [psycopg2](https://www.psycopg.org/), `pthon3` API for `PostgreSQL`,
4. [python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit), search prompt interface,
5. [humanize](https://github.com/python-humanize/humanize), show file size,
6. [aria2](https://github.com/aria2/aria2), optional download utility.


## Demo

The following host demo sites are mirrors to each other:
1. [on github.io](https://jingmatrix.github.io/en/Alibrary),
2. [on onerender.com](https://jianyu-ma.onrender.com/en/Alibrary),
3. [on netlify.app](https://jianyu-ma.netlify.app/en/Alibrary),
4. [on math.cnrs.fr](https://jianyu-ma.perso.math.cnrs.fr/en/Alibrary).

Their datasets are the same, `alibrary.sql` in [v2.0](https://github.com/JingMatrix/Alibrary/releases/tag/v2.0).

## Usage

To begin with, you can download `alibrary.sql` in the [release page](https://github.com/JingMatrix/Alibrary/releases) as a sample dataset and load it into `PostgresSQL`.
To load it, you must have the `pg_jieba` extension installed.
This sample includes 552,544 records without duplications.

After this, you can search indexes in our sample database or index your costume share links using [aliyun-share](aliyun-share),
see comments inside it for usage details.
As for search syntax, please refer to the [tsquery](https://www.postgresql.org/docs/current/datatype-textsearch.html#DATATYPE-TSQUERY).

## Development plans

- [x] Migrate database to `redis`
- [x] Implement search API
- [x] Add cli prompt interface
- [x] Improve prompt interface
- [x] Run as cloud service
- [x] User-friendly front end for public usage
- [x] Migrate database to `PostgresSQL`
