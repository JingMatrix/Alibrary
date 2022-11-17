from redis import Redis


class AliShareInfo():
    db: Redis = Redis(host="localhost", port=6379)
    share_id: str = None
    name: str = None
    size: int = 0
    file_id: str = None
    type: str = None

    def __init__(self, data):
        if type(data) is dict:
            self.__dict__ = data
        else:
            self.file_id = data.file_id
            self.share_id = data.share_id
            self.name = data.name
            self.size = data.size
            self.type = data.type

    def key(self):
        return ':Ali:' + self.share_id + ':' + self.file_id

    def save(self):
        self.db.hset(self.key(), 'n', self.name)
        self.db.hset(self.key(), 's', self.size // 1024)

    def index(self, share_id: str = None):
        if share_id is None:
            share_id = self.share_id

        cmd = 'FT.CREATE ' + share_id + ' '
        cmd += 'ON HASH '
        cmd += 'LANGUAGE chinese '
        cmd += 'NOOFFSETS '
        cmd += 'NOFIELDS '
        cmd += 'NOFREQS '
        cmd += 'PREFIX 1 ' + ':Ali:' + share_id + ': '
        cmd += 'SCHEMA n TEXT'
        self.db.execute_command(cmd)
