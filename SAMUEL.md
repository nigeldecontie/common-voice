# Common Voice

## Tasks

Hey Samuel, I mentioned I would pass on the info about what we’re looking for.
My guess is you’d want to be more involved in the ML part of the project no?
This is really a web development project.

Here’s a description:
We’re looking for a developer to create an instance of Mozilla Common Voice (https://github.com/common-voice/common-voice) the stack is Docker, React, TypeScript, MySQL, S3.
Common Voice was set up to do crowd-source recording of audio, so there are some changes that would need to be made.
Namely:
- we need the data to be unavailable to the public
- we need registration to be limited
- we need minor style and markup changes (ie taking away the language around Mozilla and adding some markup around the project)
- Common Voice currently collects audio in a lossy format (mp3), we need to change this to lossless
  16bit, 48k sample rate, lossless wav files
- Perhaps add some server-side scripting to automate signal processing/de-noising/backup

Let me know if you have any questions though!


## S3proxy

What is stored in our S3 proxy.
This is similar to `ls`.
```bash
curl http://127.0.0.1:9001/common-voice-clips \
| xmllint --format -
```
```
<?xml version="1.0" encoding="UTF-8"?>
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Name>common-voice-clips</Name>
  <Prefix/>
  <MaxKeys>1000</MaxKeys>
  <Marker/>
  <IsTruncated>false</IsTruncated>
  <Contents>
    <Key>18f74bcf-210c-43e6-b443-78248399c0ce/</Key>
    <LastModified>2022-01-18T19:28:13Z</LastModified>
    <ETag>"d41d8cd98f00b204e9800998ecf8427e"</ETag>
    <Size>4096</Size>
    <StorageClass>STANDARD</StorageClass>
    <Owner>
      <ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID>
      <DisplayName>CustomersName@amazon.com</DisplayName>
    </Owner>
  </Contents>
  <Contents>
    <Key>18f74bcf-210c-43e6-b443-78248399c0ce/00003ee1748579223ce314d00265913ba19835024b6e536f0d425230da27a629.mp3</Key>
    <LastModified>2022-01-18T19:25:38Z</LastModified>
    <ETag>"31c67dbfbb001f63468af54c228b77b6"</ETag>
    <Size>35901</Size>
    <StorageClass>STANDARD</StorageClass>
    <Owner>
      <ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID>
      <DisplayName>CustomersName@amazon.com</DisplayName>
    </Owner>
  </Contents>
</ListBucketResult>
```


Retrieve a file and check what file type it is.
```bash
curl http://127.0.0.1:9001/common-voice-clips/18f74bcf-210c-43e6-b443-78248399c0ce/00003ee1748579223ce314d00265913ba19835024b6e536f0d425230da27a629.mp3 \
| file -
```
```
/dev/stdin: Audio file with ID3 version 2.4.0, contains:MPEG ADTS, layer III, v1, 48 kbps, 32 kHz, Monaural
```
