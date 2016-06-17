Title: Using Openstack Swift as a storage backend for Docker registry
Date: 2016-06-03 06:30
Category: Openstack
Tags: Openstack, Architecture, Docker
Slug: docker-backend-swift
Authors: Arun prasath
Summary: Demo on how to use Openstack swift as storage backend for Docker registry


The following are some of the supporting storage backends for Docker registry.

inmemory: A temporary storage driver using a local inmemory map. This exists solely for reference and testing.
filesystem: A local storage driver configured to use a directory tree in the local filesystem.
s3: A driver storing objects in an Amazon Simple Storage Solution (S3) bucket.
azure: A driver storing objects in Microsoft Azure Blob Storage.
swift: A driver storing objects in Openstack Swift.
oss: A driver storing objects in Aliyun OSS.
gcs: A driver storing objects in a Google Cloud Storage bucket.

#Setting up swift as a storage backend
Create a file config.yaml
```
# cat config.yaml
version: 0.1
log:
  fields:
    service: registry
storage:
  cache:
    blobdescriptor: inmemory
  swift: 
    username: <username>    
    password: <password> 
    authurl: https://mycloud.openstack.com:5000/v2.0 
    tenant: <tenantname> 
    tenantid: <tenantID> 
    insecureskipverify: true 
    container: my_docker_registry 
    rootdirectory: /swift/object/name/prefix 
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
```
Enter Openstack auth information under ‘swift’ field.
Launch a docker-registry container
```
# docker run -d -p 5000:5000 --restart=always --name registry -v `pwd`/config.yml:/etc/docker/registry/config.yml registry:2
```
Download a image for testing and set the tag as localhost:5000
```
# docker pull busybox && docker tag busybox localhost:5000/busybox
Using default tag: latest
Trying to pull repository docker.io/library/busybox ... latest: Pulling from library/busybox
9a163e0b8d13: Already exists 
fef924a0204a: Already exists 
Digest: sha256:97473e34e311e6c1b3f61f2a721d038d1e5eef17d98d1353a513007cf46ca6bd
Status: Image is up to date for docker.io/busybox:latest
```
Push the image
```
# docker push localhost:5000/busybox
The push refers to a repository [localhost:5001/busybox] (len: 1)
fef924a0204a: Pushed 
9a163e0b8d13: Pushed 
latest: digest: sha256:241bf973af8196d58b3c439835fd37d5c773a42d496ffa00d8148893ba2de1dc size: 3202
```
You can now see that the image is now pushed into Swift container
```
# swift list my_docker_registry
files/docker/registry/v2/blobs/sha256/16/16a7ebd378002f1261dfb5e21cc22d9473aaac7e06a1cd4ff4e26cfd75432e8f/data
files/docker/registry/v2/blobs/sha256/5f/5f70bf18a086007016e948b04aed3b82103a36bea41755b6cddfaf10ace3c6ef/data
files/docker/registry/v2/blobs/sha256/89/898337b1808cb8c9578cfcc571daa4a9943e6300c3eefc1ab495365ccae4f9af/data
files/docker/registry/v2/repositories/busybox/_layers/sha256/16a7ebd378002f1261dfb5e21cc22d9473aaac7e06a1cd4ff4e26cfd75432e8f/link
files/docker/registry/v2/repositories/busybox/_layers/sha256/5f70bf18a086007016e948b04aed3b82103a36bea41755b6cddfaf10ace3c6ef/link
files/docker/registry/v2/repositories/busybox/_manifests/revisions/sha256/241bf973af8196d58b3c439835fd37d5c773a42d496ffa00d8148893ba2de1dc/link
files/docker/registry/v2/repositories/busybox/_manifests/revisions/sha256/241bf973af8196d58b3c439835fd37d5c773a42d496ffa00d8148893ba2de1dc/signatures/sha256/898337b1808cb8c9578cfcc571daa4a9943e6300c3eefc1ab495365ccae4f9af/link
files/docker/registry/v2/repositories/busybox/_manifests/tags/latest/current/link
files/docker/registry/v2/repositories/busybox/_manifests/tags/latest/index/sha256/241bf973af8196d58b3c439835fd37d5c773a42d496ffa00d8148893ba2de1dc/link
segments/2f6/46f636b65722f72656769737472792f76322f7265706f7369746f726965732f62757379626f782f5f75706c6f6164732f33333535633665662d393132372d346137642d613666622d6139316162343634376538322f646174610e3541c038ea9fc7bc970b6f183975425b0b07f470d1ea5918295cd612559b9fda39a3ee5e6b4b0d3255bfef95601890afd80709/0000000000000001
segments/2f6/46f636b65722f72656769737472792f76322f7265706f7369746f726965732f62757379626f782f5f75706c6f6164732f34623663356532612d643662352d343035312d623035342d3564623834323234313731362f64617461b83e74b4d96e60a446b0c884ea31b9f278a58a094544c6473cec4e8e83351ca7da39a3ee5e6b4b0d3255bfef95601890afd80709/0000000000000001
```
