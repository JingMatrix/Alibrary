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
2. [redis-stack](https://redis.io/download/), database,
3. [redis-om-python](https://github.com/redis/redis-om-python), `pthon3` API for `redis`,
4. [aria2](https://github.com/aria2/aria2), optional download utility.

## Development plans

- [x] Migrate database to `redis`
- [x] Implement search API
- [ ] Add cli prompt interface
- [ ] Run as cloud service
- [ ] User-friendly front end for public usage
