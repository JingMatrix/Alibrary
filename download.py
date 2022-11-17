# Config:
# Modify the variables: $download_dir.

import os
import sys
import tempfile
from aligo import Aligo


def Download(share_index: str,
             file_name: str,
             share_token: str = None,
             download_dir: str = tempfile.gettempdir()):
    ali = Aligo(use_aria2=True)
    share_data = share_index.split(':')
    share_info = {"share_id": share_data[2], "file_id": share_data[3]}
    if share_token is None:
        share_token: str = str(ali.get_share_token(share_info["share_id"]))

    if len(sys.argv) > 2:
        download_path = os.path.expanduser(sys.argv[2])
    else:
        download_path = download_dir + '/' + file_name

    download_url = ali.get_share_link_download_url(
        share_id=share_info["share_id"],
        file_id=share_info["file_id"],
        share_token=share_token).download_url
    ali.download_file(file_path=download_path, url=download_url)
