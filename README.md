# minecraft-release-hook

To be run regular. Each time it runs, it checks the current release version and compares it to one locally saved.
If they do not match, it will send an HTTP POST to a specified url and save the new version locally.

Create a .env with your URL:

`API_ENDPOINT=https://cloud.docker.com/api/build/v1/source/.../trigger/.../call/`

## run container

`docker run --rm -it --env-file  .env -v $(pwd)/version.json:/root/version.json halandar/mc-release-webhook:latest`

## crontab example

```crontab
MAILTO="mycool@mailaddress.net"
* */2 * * * docker run --rm -it --env-file /etc/.env -v /etc/mc-version.json:/root/version.json halandar/mc-release-webhook:latest
```
