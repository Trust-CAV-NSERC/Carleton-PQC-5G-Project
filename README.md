# Self Directed Studies Project
## Author
Georges Ankenmann - Carleton University

## Background
Rainbow keys are large (at least 60 KB, while Dilithium only 1.3 KB). But if we don’t update key frequently over the air we can embed the Rainbow secret or public key into car, as Rainbow has small signatures (66 bytes, while Dilithium is 2.4 KB), considering SCMS(Security Credential Management System) or Smart City IoT(Internet of things) message length might be only a few hundred bytes. We test both quantum resistant Saber and Kyber algorithms on L5 (AeroXO) Trusted Connected and Autonomous Vehicles track over Ericsson ENCQOR 5G (Evolution of Networked Services through a Corridor in Québec and Ontario for Research and Innovation).

## Purpose
The purpose of this project is to experiment with post quantum encryption algorithms and measure the latency of various types of deployment. 

## Notes
All client and server testing have been performed on Ubuntu 20.04.02 LTS.

# Stationary Tests
Part of the testing required to see how the latency of various algorithms would work when the client was at rest. These series of test only tests one algorithm at once. The client and server must be rebuilt to test another algorithm. The client supports mutliple servers. The client performs multiple tasks sequentially. Data is tagged with a fixed GPS ID.

## Cipher Text Latency Tests
The first test is performed to test the latency of key exchange algorithms. A mock client and server have been setup and designed in Python to support this scenario. The client exchanges public keys with the server and transferres an encrypted secret. 

## Clear Text Latency Tests
The second test is performed to test te latency of message siging. A mock client and server have been setup and designed in Python to support this scenario. The client asks for the server's public key, and then asks for a signed message. The client then performs a verification on the signed message based on the requested public key.

## Build Instructions - Base Image - All machines
1. Install Docker on local machine
1. In the Base Image directory, build base image and tag it as `base_image` - `docker build -t base_image .`
1. In the Client directory, build client image and tag it as `client` - `docker build -t client .`
1. In the Server directory, build the server image and tag it as `server` - `docker build -t server .`
1. Run the server - `docker run --rm -p 5000:5000 --name server --net=testnet server`
1. Run the client - `docker run --rm --net=testnet -e GPS_ID=0001 client`

## Build Instructions - Server and client are on seperate machines
1. Install Docker on local machine
1. In the Base Image directory, build base image and tag it as `base_image` - `docker build -t base_image .`
1. In the Client directory, edit the `app.py` file to reflect the IP address of the remote server (line 15).
1. In the Client directory, build client image and tag it as `client` - `docker build -t client .`
1. In the Server directory, build the server image and tag it as `server` - `docker build -t server .`

### On the server machine:
1. Run the server - `docker run --rm -p 5000:5000 --name server server`

### On the client machine:
1. Run the client - `docker run --rm -e GPS_ID=0001 client`

# In Motion Tests
Another part of the testing is to support a way to test, in real time, the latency of various message signing algorithms. A client and server have been implemented to support these requirements. The series of Dilithium and Rainbow algorithms are tested and compared. 

## How to run In Motion Tests
### Requirements
1. A USB GPS reciever and `gpsd` installed/running on the client laptop
1. Docker and Docker-compose installed on the client and server
1. `base_image` built on the client and server

### Server
1. Build the base image on the server
1. Run `docker-compose up --build -d` on the server inside of the `In Motions Test/Server` directory.

### Client
1. Build the base image on the client
1. Plug in the GPS USB reciever into the client
1. Run `sudo gpsd -N -G /dev/ttyUSB0`
1. Run `docker-compose up --build` on the server inside of the `In Motions Test/Client` directory. 

### Data Parser
A data parser app has been written to convert the `.json` files to a CSV, which should help in graphing the data. 

1. Build the data parser image - `docker build -t parser .`
1. Run the data parser container - `'docker run --rm -it -v /opt/pqc/data:/opt/data -v /opt/pqc/dropoff:/opt/dropoff parser`

The resulting `.csv` files will be in the `/opt/dropoff` directory. 