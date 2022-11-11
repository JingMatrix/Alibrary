from redis_om import HashModel, Field


class AliShareInfo(HashModel):
    share_id: str = None
    file_extension: str = None
    name: str = Field(index=True, full_text_search=True)
    size: int = None
    file_id: str = Field(primary_key=True)
    type: str = None

    @staticmethod
    def strip(data: dict):
        return AliShareInfo(share_id=data.share_id,
                            file_id=data.file_id,
                            name=data.name,
                            size=data.size,
                            file_extension=data.file_extension,
                            type=data.type)
