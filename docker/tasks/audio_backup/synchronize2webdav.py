#!/usr/bin/env  python3
# vim:nowrap:

# curl http://127.0.0.1:9001/common-voice-clips | xmllint --format - | less

import logging
logging.basicConfig(level=logging.DEBUG)

import json
import requests
import sys
import tempfile
import untangle   # untangle parses an XML document and returns a Python object which makes it easy to access the data you want.

from pathlib import Path
from tqdm import tqdm
from typing import (
        Any,
        Generator,
        Tuple,
        )
from webdav3.client import Client

from webdav3.exceptions import ConnectionException as webdavConnectionException


def test_nextcloud(
        webdav_hostname: str,
        webdav_login: str,
        webdav_password: str,
        ):
    nextcloud_options = {
            "webdav_hostname": webdav_hostname,
            "webdav_login":    webdav_login,
            "webdav_password": webdav_password,
            }
    nextcloud_client = Client(nextcloud_options)

    #print(nextcloud_client.info("CommonVoice"))
    #print(nextcloud_client.info("CommonVoice/SAMUEL.md"))
    print(*nextcloud_client.list("CommonVoice", get_info=True), sep="\n")

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



def test_s3():
    """
    Learning how AWS S3 boto works.
    """
    import boto3
    BucketName="smallteamtest"
    test_filename="CommonVoice/requirements.txt"

    # List Buckets
    client = boto3.client('s3')
    response = client.list_buckets()
    print(json.dumps(response, indent=3, sort_keys=True, default=str))
    for bucket in response["Buckets"]:
        print(bucket["Name"])

    # Upload a file
    if False:
        with open("requirements.txt", mode="r", encoding="UTF-8") as f:
            object_data = f.read()
            client.put_object(
                    Body=object_data,
                    Bucket=BucketName,
                    Key=test_filename,
                    )

    with open("requirements.txt", mode="rb") as f:
        client.upload_fileobj(
                Fileobj=f,
                Bucket=BucketName,
                Key=test_filename,
                )

    # Check that the file is there
    response = client.list_objects(Bucket=BucketName)
    print(json.dumps(response, indent=3, sort_keys=True, default=str))

    # Download the file
    response = client.get_object(
            Bucket=BucketName,
            Key=test_filename,
            )
    print(json.dumps(response, indent=3, sort_keys=True, default=str))



    if False:
        response = client.create_bucket(
                #ACL="private",
                #Bucket="S3://CommonVoice",
                Bucket="commonVoice",
                #CreateBucketConfiguration={
                #    "LocationConstraint": "us-east-2",
                #    },
                #GrantFullControl="string",
                #GrantRead="string",
                #GrantReadACP="string",
                #GrantWrite="string",
                #GrantWriteACP="string",
                #ObjectLockEnabledForBucket=True|False,
                #ObjectOwnership="BucketOwnerPreferred"|"ObjectWriter"|"BucketOwnerEnforced"
                )
        print(response)




#CV_S3_CONFIG='{"endpoint": "http://s3proxy:80", "accessKeyId": "local-identity", "secretAccessKey": "local-credential", "s3ForcePathStyle": true}'
def synchronize(
        webdav_hostname: str,
        webdav_login: str,
        webdav_password: str,
        s3_config_str: str,
        ):
    """
    Synchronize the audio clips from S3Proxy to NRC's nextcloud.
    """
    s3_config = json.loads(s3_config_str)
    s3_url = f"{s3_config['endpoint']}/common-voice-clips"
    logging.info(f"S3: {s3_url}")

    # What is on the server?
    s3 = untangle.parse(s3_url)
    #print(s3)
    if not hasattr(s3.ListBucketResult, "Contents"):
        logging.info("S3 is empty")
        sys.exit()

    nextcloud_options = {
            "webdav_hostname": f"{webdav_hostname}/remote.php/dav/files/{webdav_login}/",
            "webdav_login":    webdav_login,
            "webdav_password": webdav_password,
            }
    logging.info(f"NextCloud: {webdav_hostname}")
    nextcloud_client = Client(nextcloud_options)

    # What is on our backup?
    def recursive_list(root: str = "CommonVoice") -> Generator[Tuple[str, Any], None, None]:
        """
        """
        directories = nextcloud_client.list(root, get_info=True)
        directories = filter(lambda d: d["isdir"], directories)
        for directory in directories:
            path = Path(directory["path"])
            # /remote.php/dav/files/2c523d8d-449f-4176-bb05-SSSSSSSSSSSS/CommonVoice/
            path = Path("/".join(path.parts[5:]))
            items = nextcloud_client.list(str(path), get_info=True)
            items = filter(lambda d: not d["isdir"], items)
            for item in items:
                path = Path(item["path"])
                path = Path("/".join(path.parts[6:]))
                yield (str(path), item)

    nextcloud = {name for name, _ in recursive_list()}

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
    if not (len(sys.argv) <= 5):
        print("Usage pgm nextcloud_hostname nextcloud_login nextcloud_password s3proxy/ip", file=sys.stderr)
        print(f"current arguments are: {sys.argv}", file=sys.stderr)
        print("Have you properly setup .env-tasks's WEBDAV_HOSTNAME, WEBDAV_LOGIN, WEBDAV_PASSWORD?", file=sys.stderr)
        print("Have you properly setup .env-local-docker's CV_S3_CONFIG?", file=sys.stderr)
    try:
        synchronize(*sys.argv[1:])
    except webdavConnectionException:
        logging.error("Connection timed out for nextcloud.")
