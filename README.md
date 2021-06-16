# Self Directed Studies Project
## Author
Georges Ankenmann - Carleton University

## Background
Rainbow keys are large (at least 60 KB, while Dilithium only 1.3 KB). But if we don’t update key frequently over the air we can embed the Rainbow secret or public key into car, as Rainbow has small signatures (66 bytes, while Dilithium is 2.4 KB), considering SCMS(Security Credential Management System) or Smart City IoT(Internet of things) message length might be only a few hundred bytes. We test both quantum resistant Saber and Kyber algorithms on L5 (AeroXO) Trusted Connected and Autonomous Vehicles track over Ericsson ENCQOR 5G (Evolution of Networked Services through a Corridor in Québec and Ontario for Research and Innovation).

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