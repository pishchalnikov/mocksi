# MockSi

Simple REST API Server to manage mock services in Docker containers for automation testing

## Quick start
### Requirements
```
python3
Docker
Make
```

### Installation

```
$ git clone git@github.com:pishchalnikov/mocksi.git

$ cd mocksi

$ cat config.yaml
services:
  httpd:
    image: httpd
    version: latest
    port: 80

$ docker pull httpd

$ make build

$ make run

```

### How to use
```
$ curl http://localhost:9090/api/services
["httpd"]

$ curl -X POST -H "Content-Type: application/json" http://localhost:9090/api/containers -d '{"image":"httpd"}'
{
    "created": 1535901984,
    "id": "acf7292665249a13e5d00ed1ac8e73ce0f476f3820b1fcb8299545a926c4f9b8",
    "image": "httpd",
    "port": 32770,
    "state": "running",
    "status": "Up Less than a second",
    "version": "latest"
}

$ curl http://localhost:9090/api/containers
[
    {
        "created": 1535901984,
        "id": "acf7292665249a13e5d00ed1ac8e73ce0f476f3820b1fcb8299545a926c4f9b8",
        "image": "httpd",
        "port": 32770,
        "state": "running",
        "status": "Up Less than a second",
        "version": "latest"
    }
]

$ curl http://localhost:32770
<html><body><h1>It works!</h1></body></html>

$ curl -X DELETE http://localhost:9090/api/containers/acf7292665249a13e5d00ed1ac8e73ce0f476f3820b1fcb8299545a926c4f9b8
{
    "status": "OK"
}

$ curl http://localhost:9090/api/containers
[]
```
Add mock services in `config.yaml` and pull it if needed