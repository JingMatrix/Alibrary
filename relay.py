from aligo import Aligo, BatchRequest, BatchSubRequest


def Relay(file_id: str, share_id: str, relay_folder: str = None) -> str:
    print('Relaying file ', file_id)
    relay_folder = relay_folder or '637163bbabb15d41782d41f4bcda41a243107a89'

    share_token = str(ali.get_share_token(share_id))
    relayed_files = ali.get_file_list(parent_file_id=relay_folder)
    if len(relayed_files) > 10:
        ali.batch_delete_files([f.file_id for f in relayed_files])
    relay_file = ali.share_file_saveto_drive(share_id=share_id,
                                             share_token=share_token,
                                             file_id=file_id,
                                             to_parent_file_id=relay_folder)
    return ali.share_file(file_id=relay_file.file_id).share_url


class CustomAligo(Aligo):
    """自定义 aligo """
    V3_FILE_DELETE = '/v3/file/delete'

    def delete_file(self, file_id: str, drive_id: str = None) -> bool:
        """删除文件"""
        drive_id = drive_id or self.default_drive_id
        response = self._post(self.V3_FILE_DELETE,
                              body={
                                  'drive_id': drive_id,
                                  'file_id': file_id
                              })
        return response.status_code == 204

    def batch_delete_files(self,
                           file_id_list: [str],
                           drive_id: str = None):
        """批量删除文件"""
        drive_id = drive_id or self.default_drive_id
        result = self.batch_request(
            BatchRequest(requests=[
                BatchSubRequest(id=file_id,
                                url='/file/delete',
                                body={
                                    'drive_id': drive_id,
                                    'file_id': file_id
                                }) for file_id in file_id_list
            ]), dict)
        return list(result)


ali = CustomAligo()
