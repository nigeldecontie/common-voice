# Common Voice

## Links
* [Common Voice - Github](https://github.com/common-voice/common-voice) Mozilla Common Voice, a platform for collecting speech donations in order to create public domain datasets for training voice recognition-related tools.
* [Matrix Chat](https://chat.mozilla.org/#/room/#common-voice:mozilla.org)
* [Discourse](https://discourse.mozilla.org/c/voice/239)
* [Auth0](https://auth0.com/)
* [stream-transcoder.js](https://www.npmjs.com/package/stream-transcoder) Flexible media transcoding using FFmpeg. Stream media in and out - converting it on the fly.


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
- Is it set up so that auth0 let’s us define a list of email address or something that are whitelisted for signing up?
    The recordings should also only be accessible to pre-defined sets of users.
    Do you have a sense of whether it will be easier to password protect the entire site or whether we could have tiers of access for particular recordings?

Let me know if you have any questions though!


## Auth0
Like it or not, you need a [Auth0](https://auth0.com/) account to get Common Voice to work.
Add the following lines to `.env-local-docker` which is locate at the root of the git repository.
```
CV_AUTH0_DOMAIN="dev-24cisdir.us.auth0.com"
CV_AUTH0_CLIENT_ID="<YOUR_ID>"
CV_AUTH0_CLIENT_SECRET="<YOU_HAVE_A_SECRET>"
```

### Whitelisting emails
* [Auth0 Rules](https://auth0.com/docs/customize/rules)
* [Manage User Access to Applications](https://auth0.com/docs/manage-users/user-accounts/manage-user-access-to-applications)
* [Rules examples](https://github.com/auth0/rules/tree/aeaf93bc058408e260192d0941a688963449d6be/src/rules)
* [Whitelist for a Specific App](https://github.com/auth0/rules/blob/aeaf93bc058408e260192d0941a688963449d6be/src/rules/simple-user-whitelist-for-app.js) Only allow access to users with whitelist email addresses on a specific app.
* [Whitelist](https://github.com/auth0/rules/blob/aeaf93bc058408e260192d0941a688963449d6be/src/rules/simple-user-whitelist.js) Only allow access to users with specific whitelist email addresses.
* [Whitelist on Specific Connection](https://github.com/auth0/rules/blob/aeaf93bc058408e260192d0941a688963449d6be/src/rules/simple-whitelist-on-a-connection.js) Only allow access to users coming from a whitelist on specific connection.
* [Email domain whitelist](https://github.com/auth0/rules/blob/aeaf93bc058408e260192d0941a688963449d6be/src/rules/simple-domain-whitelist.js) Only allow access to users with specific whitelist email domains.
* [Whitelist on the cloud](https://github.com/auth0/rules/blob/aeaf93bc058408e260192d0941a688963449d6be/src/rules/dropbox-whitelist.js) Determine access to users based on a whitelist of emails stored in Dropbox.
* [Add country to the user profile](https://github.com/auth0/rules/blob/aeaf93bc058408e260192d0941a688963449d6be/src/rules/add-country.js) Add a country attribute to the user based on their IP address.
* [Disable social signups](https://github.com/auth0/rules/blob/aeaf93bc058408e260192d0941a688963449d6be/src/rules/disable-social-signup.js) Disable signups from social connections.
* [Force email verification](https://github.com/auth0/rules/blob/aeaf93bc058408e260192d0941a688963449d6be/src/rules/email-verified.js) Only allow access to users with verified emails.

Looking at [Whitelist for a Specific App](https://github.com/auth0/rules/blob/aeaf93bc058408e260192d0941a688963449d6be/src/rules/simple-user-whitelist-for-app.js) seems to be promising.
```javascript
/**
 * @title Whitelist for a Specific App
 * @overview Only allow access to users with whitelist email addresses on a specific app
 * @gallery true
 * @category access control
 *
 * This rule will only allow access to users with specific email addresses on a specific app.
 *
 */

function (user, context, callback) {

  // Access should only be granted to verified users.
  if (!user.email || !user.email_verified) {
    return callback(new UnauthorizedError('Access denied.'));
  }

  // only enforce for NameOfTheAppWithWhiteList
  // bypass this rule for all other apps
  if(context.clientName !== 'NameOfTheAppWithWhiteList'){
    return callback(null, user, context);
  }

  const whitelist = [ 'user1@example.com', 'user2@example.com' ]; // authorized users
  const userHasAccess = whitelist.some(function (email) {
    return email === user.email;
  });

  if (!userHasAccess) {
    return callback(new UnauthorizedError('Access denied.'));
  }

  callback(null, user, context);
}
```


## Changing the Audio Format
To change the audio codec, the format & the sample rate, you have to add the following lines to `.env-local-docker` which is located at the root of the repository.
```
CV_TRANSCODE_CODEC='pcm_s16le'
CV_TRANSCODE_FORMAT='wav'
CV_TRANSCODE_SAMPLE_RATE='44100'
```

### Available Lossless Audio Codecs
```bash
ffmpeg -codecs |& grep ".EA..S"
```
or
```bash
docker container exec -it web ffmpeg -codecs |& grep ".EA..S"
```
```bash
docker container exec -it web ffmpeg -codecs \
 |& grep ".EA..S" \
 | sed -e 's| \([^ ]\+\) \([^ ]\+\) \+\(.\+\)|\1\t\2\t\3|' \
 | tabulate --sep $'\t' --format pipe
```
| Attributes | Name | Description |
|--------|------------------|----------------------------------------------------------------|
| DEA..S | alac             | ALAC (Apple Lossless Audio Codec)                              |
| DEA.LS | dts              | DCA (DTS Coherent Acoustics) (decoders: dca ) (encoders: dca ) |
| DEA..S | flac             | FLAC (Free Lossless Audio Codec)                               |
| DEA..S | mlp              | MLP (Meridian Lossless Packing)                                |
| DEA..S | pcm_f32be        | PCM 32-bit floating point big-endian                           |
| DEA..S | pcm_f32le        | PCM 32-bit floating point little-endian                        |
| DEA..S | pcm_f64be        | PCM 64-bit floating point big-endian                           |
| DEA..S | pcm_f64le        | PCM 64-bit floating point little-endian                        |
| DEA..S | pcm_s16be        | PCM signed 16-bit big-endian                                   |
| DEA..S | pcm_s16be_planar | PCM signed 16-bit big-endian planar                            |
| DEA..S | pcm_s16le        | PCM signed 16-bit little-endian                                |
| DEA..S | pcm_s16le_planar | PCM signed 16-bit little-endian planar                         |
| DEA..S | pcm_s24be        | PCM signed 24-bit big-endian                                   |
| DEA..S | pcm_s24daud      | PCM D-Cinema audio signed 24-bit                               |
| DEA..S | pcm_s24le        | PCM signed 24-bit little-endian                                |
| DEA..S | pcm_s24le_planar | PCM signed 24-bit little-endian planar                         |
| DEA..S | pcm_s32be        | PCM signed 32-bit big-endian                                   |
| DEA..S | pcm_s32le        | PCM signed 32-bit little-endian                                |
| DEA..S | pcm_s32le_planar | PCM signed 32-bit little-endian planar                         |
| DEA..S | pcm_s64be        | PCM signed 64-bit big-endian                                   |
| DEA..S | pcm_s64le        | PCM signed 64-bit little-endian                                |
| DEA..S | pcm_s8           | PCM signed 8-bit                                               |
| DEA..S | pcm_s8_planar    | PCM signed 8-bit planar                                        |
| DEA..S | pcm_u16be        | PCM unsigned 16-bit big-endian                                 |
| DEA..S | pcm_u16le        | PCM unsigned 16-bit little-endian                              |
| DEA..S | pcm_u24be        | PCM unsigned 24-bit big-endian                                 |
| DEA..S | pcm_u24le        | PCM unsigned 24-bit little-endian                              |
| DEA..S | pcm_u32be        | PCM unsigned 32-bit big-endian                                 |
| DEA..S | pcm_u32le        | PCM unsigned 32-bit little-endian                              |
| DEA..S | pcm_u8           | PCM unsigned 8-bit                                             |
| DEA..S | s302m            | SMPTE 302M                                                     |
| DEA..S | truehd           | TrueHD                                                         |
| DEA..S | tta              | TTA (True Audio)                                               |
| DEA.LS | wavpack          | WavPack (encoders: wavpack libwavpack )                        |


### Available Formats
```bash
ffmpeg -formats
```
or
```bash
docker container exec -it web ffmpeg -formats
```


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

## Why `You're on the staging server.`
Originating from `web/src/components/layout/layout.tsx`
It uses `web/src/utility.ts:isProduction()` which simply check if the `window.location.origin === URLS.HTTP_ROOT` where `URLS.HTTP_ROOT` is `https://commonvoice.mozilla.org`.


## File Changed so Far.
* `server/src/lib/api.ts`
* `server/src/lib/bucket.ts`
* `server/src/lib/clip.ts`
