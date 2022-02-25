#!/usr/bin/env  python3
# vim:nowrap:

#curl http://127.0.0.1:9001/common-voice-clips | xmllint --format - | less

import requests
import sys
import tempfile
import untangle

from pathlib import Path
from tqdm import tqdm
from webdav3.client import Client



def test(
        webdav_hostname: str,
        webdav_login: str,
        webdav_password: str,
        ):
    options = {
            'webdav_hostname': webdav_hostname,
            'webdav_login':    webdav_login,
            'webdav_password': webdav_password,
            }
    nextcloud_client = Client(options)

    #print(nextcloud_client.info("CommonVoice"))
    #print(nextcloud_client.info("CommonVoice/SAMUEL.md"))
    print(*nextcloud_client.list("CommonVoice", get_info=True), sep='\n')

    # Upload resource
    #nextcloud_client.upload_sync(
    #        remote_path="CommonVoice/18f74bcf-210c-43e6-b443-78248399c0ce.00ec30d708e2eb40fa300f933a680de09010ceed5d4daff387ae375f0a962be3.wav",
    #        local_path="18f74bcf-210c-43e6-b443-78248399c0ce.00ec30d708e2eb40fa300f933a680de09010ceed5d4daff387ae375f0a962be3.wav")
    #nextcloud_client.upload_sync(remote_path="dir1/file1", local_path="~/Documents/file1")
    #nextcloud_client.upload_sync(remote_path="dir1/dir2/", local_path="~/Documents/dir2/")

    # Send missing files
    #nextcloud_client.push(remote_directory="CommonVoice", local_directory="CommonVoice")


    if False:
        r = requests.get("http://s3proxy:9001/common-voice-clips")
        print(r.text)



def synchronize(
        webdav_hostname: str,
        webdav_login: str,
        webdav_password: str,
        s3proxy_ip: str = "s3proxy",
        ):
    """
    Synchronize the audio clips from S3Proxy to NRC's nextcloud.
    """
    s3_url = f"http://{s3proxy_ip}:9001/common-voice-clips"
    options = {
            'webdav_hostname': f"https://{webdav_hostname}/remote.php/dav/files/{webdav_login}/",
            'webdav_login':    webdav_login,
            'webdav_password': webdav_password,
            }
    nextcloud_client = Client(options)

    # What is on the server?
    s3 = untangle.parse(s3_url)
    #print(s3)

    # What is on our backup?
    def recursive_list(root: str = "CommonVoice"):
        """
        """
        directories = nextcloud_client.list(root, get_info=True)
        directories = filter(lambda d: d["isdir"], directories)
        for directory in directories:
            path = Path(directory["path"])
            # /remote.php/dav/files/2c523d8d-449f-4176-bb05-SSSSSSSSSSSS/CommonVoice/
            path = Path('/'.join(path.parts[5:]))
            items = nextcloud_client.list(str(path), get_info=True)
            items = filter(lambda d: not d["isdir"], items)
            for item in items:
                path = Path(item["path"])
                path = Path('/'.join(path.parts[6:]))
                yield (str(path), item)

    nextcloud = { name for name, _ in recursive_list() }

    missing_recordings = {
            f.Key.cdata for f in s3.ListBucketResult.Contents[1:]
            }.difference(nextcloud)
    for name in tqdm(missing_recordings, desc="Sync S3 => nextcloud", unit="Items"):
        with tempfile.NamedTemporaryFile() as temp:
            r = requests.get(f"{s3_url}/{name}")
            temp.write(r.content)
            nextcloud_client.mkdir("CommonVoice/" + str(Path(name).parent))
            nextcloud_client.upload_sync(
                    local_path=temp.name,
                    remote_path=f"CommonVoice/{name}",
                    )





if __name__ == "__main__":
    if not ( 4<= len(sys.argv) <= 5):
        print("Usage pgm hostname login password [s3proxy/ip]")
    synchronize(*sys.argv[1:])
