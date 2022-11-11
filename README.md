# Alibrary

Database toolkit for aliyundrive share links

## Goals

Currently, many people share huge pack of files via [阿里云盘](https://www.aliyundrive.com/).
For example, one can find such share links in [UP云搜](https://www.upyunso.com/), [万人迷吧](https://wanrenmi8.com/cn/index.html) and [云盘资源网](https://www.yunpanziyuan.com/).
Given those abundant resources, we create [Alibrary](https://github.com/JingMatrix/Alibrary) project to index and update shared files.
This project _SHOULD_ reach the following goals:
1. store index data reliably;
2. provide rapid search API;
3. update and validate share links efficiently.

## Dependencies

We use the following projects:
1. [aligo](https://github.com/foyoux/aligo), `python3` API of aliyundrive,
2. [redis](https://github.com/redis/redis) with [RedisSearch](https://github.com/RediSearch/RediSearch) [loaded](https://redis.io/docs/stack/search/quick_start/); alternatively, one can choose [redis-stack](https://redis.io/download/), database,
3. [redis-om-python](https://github.com/redis/redis-om-python), `pthon3` API for `redis`,
4. [python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit), search prompt interface,
4. [aria2](https://github.com/aria2/aria2), optional download utility.

## Performance

1. Index speed: 63886 indexes in around 15 minuties.

## Usage

The first step is start the redis-sever:
```sh
redis-server --dir . --dbfilename archive.rdb --loadmodule /path/to/redisearch.so

```
The module `redisearch.so` above should be compiled on your OS.

If you don't want to comiple it, please download and use `redis-stack` insteadly:
```sh
redis-stack-server --dir . --dbfilename archive.rdb
```
If your `redis-server` or `redis-stack-sever` is alreading runing, please stop it first.

Then you can see search in database and index share links using `aliyun-share`,
see comments inside for usages.
As for search syntax, please refer to the [offical docs](https://redis.io/docs/stack/search/reference/query_syntax/).

## Development plans

- [x] Migrate database to `redis`
- [x] Implement search API
- [x] Add cli prompt interface
- [ ] Improve prompt interface
- [ ] Run as cloud service
- [ ] User-friendly front end for public usage
