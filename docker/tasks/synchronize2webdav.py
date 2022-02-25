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
        ):
    """
    Synchronize the audio clips from S3Proxy to NRC's nextcloud.
    """
    s3_url = "http://s3proxy:9001/common-voice-clips"
    options = {
            'webdav_hostname': webdav_hostname,
            'webdav_login':    webdav_login,
            'webdav_password': webdav_password,
            }
    nextcloud_client = Client(options)

    # What is on the server?
    s3 = untangle.parse(s3_url)
    #print(s3)

    # What is on our backup?
    nextcloud = {
            Path(item["path"]).name: item
            for item in nextcloud_client.list("CommonVoice", get_info=True)
            }
    for f in tqdm(s3.ListBucketResult.Contents[1:]):
        name = Path(f.Key.cdata).name
        #print(name)
        #print(f.Size.cdata)
        if name not in nextcloud.keys():
            #print("Uploading", name)
            with tempfile.NamedTemporaryFile() as temp:
                r = requests.get(f"{s3_url}/{f.Key.cdata}")
                # open('facebook.ico', 'wb').write(r.content)
                temp.write(r.content)
                nextcloud_client.upload_sync(
                        local_path=temp.name,
                        remote_path=f"CommonVoice/{name}")





if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage pgm hostname login password")
    synchronize(*sys.argv[1:])
