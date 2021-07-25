FROM ubuntu:focal
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update
RUN apt-get -y install python3 python-is-python3 python3-pip cmake gcc git ninja-build libssl-dev python3-pytest python3-pytest-xdist unzip xsltproc doxygen graphviz gpsd gpsd-clients gpsbabel
RUN git clone -b main https://github.com/open-quantum-safe/liboqs.git /opt/liboqs && cd /opt/liboqs &&  mkdir build && cd build && cmake -GNinja -DBUILD_SHARED_LIBS=ON .. && ninja && ninja install
RUN git clone https://github.com/open-quantum-safe/liboqs-python /opt/liboqs-python && cd /opt/liboqs-python && python3 setup.py install
RUN pip install requests flask flask_jwt pycrypto iperf3 gpsd-py3 pika geopy