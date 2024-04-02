FROM ubuntu:22.04

RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list

RUN apt update && apt-get install -y neofetch inetutils-ping net-tools