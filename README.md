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
2. [redis](https://github.com/redis/redis) with [RediSearch](https://github.com/RediSearch/RediSearch) [loaded](https://redis.io/docs/stack/search/quick_start/); alternatively, one can choose [redis-stack](https://redis.io/download/), database,
3. [redis-om-python](https://github.com/redis/redis-om-python), `pthon3` API for `redis`,
4. [python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit), search prompt interface,
5. [humanize](https://github.com/python-humanize/humanize), show file size,
6. [aria2](https://github.com/aria2/aria2), optional download utility.

## Performance

1. Index speed: 63886 indexes done in around 15 minutes (with the author's average internet connection).
2. Index data size: 150644 indexes within size 34M.

## Demo

The following host demo sites are mirrors to each other:
1. [on github.io](https://jingmatrix.github.io/en/Alibrary),
2. [on onerender.com](https://jianyu-ma.onrender.com/en/Alibrary),
3. [on netlify.app](https://jianyu-ma.netlify.app/en/Alibrary),
4. [on math.cnrs.fr](https://jianyu-ma.perso.math.cnrs.fr/en/Alibrary).

Their datasets are the same, `archive.rdb` in [v0.2](https://github.com/JingMatrix/Alibrary/releases/tag/v0.2) and [v0.3](https://github.com/JingMatrix/Alibrary/releases/tag/v0.3).

## Usage

To begin with, you can download `archive.rdb` in the [release page](https://github.com/JingMatrix/Alibrary/releases) as sample dataset.
Our database `archive.rdb` includes all indexes from [well-chosen share links](share_urls.md),
and it contains 150644 records of e-books.

The next step is to start the redis-sever:
```sh
redis-server --dir . --dbfilename archive.rdb --loadmodule /path/to/redisearch.so

```
The module `redisearch.so` above should be compiled on your OS.
Complied binaries from `Android arm64` and `Linux amd64` could be found in the [release page](https://github.com/JingMatrix/Alibrary/releases/tag/v0.2).

If you don't want to compile it, please download and use `redis-stack` instead:
```sh
redis-stack-server --dir . --dbfilename archive.rdb
```
If your `redis-server` or `redis-stack-sever` is already running, please stop it first.
Please notice that our `archive.rdb` requires `redis-sever` with version higher than `v7.0`.

Finally, you can search indexes in our sample database or index your costume share links using [aliyun-share](aliyun-share),
see comments inside it for details.
As for search syntax, please refer to the [official docs](https://redis.io/docs/stack/search/reference/query_syntax/).

## Development plans

- [x] Migrate database to `redis`
- [x] Implement search API
- [x] Add cli prompt interface
- [x] Improve prompt interface
- [x] Run as cloud service
- [x] User-friendly front end for public usage
