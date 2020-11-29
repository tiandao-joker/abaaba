from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from abaaba.settings import FDFS_BASE_URL, FDFS_CLIENT_CONF


class FDFSStorage(Storage):
    """  fdfs文件存储  """

    def __init__(self, client_conf=None, base_url=None):
        if client_conf is None:
            client_conf = FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url is None:
            base_url = FDFS_BASE_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        """  打开文件时 是以二进制方式打开 """
        pass

    def _save(self, name, content):
        """  存储文件 """
        # 创建一个fdfs对象
        client = Fdfs_client("./utils/fdfs/client.conf")

        # 上传文件到fdfs系统中
        res = client.upload_by_buffer(content.read())
        """
                它的返回值是个字典  内容如下：
                return dict {
                    'Group name'      : group_name,
                    'Remote file_id'  : remote_file_id,
                    'Status'          : 'Upload successed.',
                    'Local file name' : '',
                    'Uploaded size'   : upload_size,
                    'Storage IP'      : storage_ip
                } 
                """
        if res.get("Status") != "Upload successed.":
            # 说明上传失败，然后手动抛出一个异常
            raise Exception("图片上传失败")

        # 如果上面if条件没有满足 那么说明上传成功,获取图片的路径
        filename = res.get("Remote file_id")
        return filename

    def exists(self, name):
        """  django 判断文件名是否可用 """
        return False

    def url(self, name):
        # 返回访问文件的url路径
        return self.base_url + name
