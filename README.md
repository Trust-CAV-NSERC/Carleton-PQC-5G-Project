# Self Directed Studies Project
## Author
Georges Ankenmann - Carleton University

## Purpose
The purpose of this project is to experiment with post quantum encryption algorithms and measure the latency of various types of deployment. 

## Build Instructions - All on one machine
1. Install Docker on local machine
1. create a network called `testNet` - `docker network create testnet`
1. In the Base Image directory, build base image and tag it as `base_image` - `docker build -t base_image .`
1. In the Client directory, build client image and tag it as `client` - `docker build -t client .`
1. In the Server directory, build the server image and tag it as `server` - `docker build -t server .`
1. Run the server - `docker run --rm -p 5000:5000 --name server --net=testnet server`
1. Run the client - `docker run --rm --net=testnet client`

## Build Instructions - Server and client are on seperate machines
1. Install Docker on local machine
1. In the Base Image directory, build base image and tag it as `base_image` - `docker build -t base_image .`
1. In the Client directory, edit the `app.py` file to reflect the IP address of the remote server (line 10-11).
1. In the Client directory, build client image and tag it as `client` - `docker build -t client .`
1. In the Server directory, build the server image and tag it as `server` - `docker build -t server .`

### On the server machine:
1. Run the server - `docker run --rm -p 5000:5000 --name server server`

### On the client machine:
1. Run the client - `docker run --rm client`