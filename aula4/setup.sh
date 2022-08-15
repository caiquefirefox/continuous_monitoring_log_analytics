#!/bin/bash
#install basic packages
sudo apt-get install net-tools -y
sudo apt-get install curl -y
sudo apt-get install telnet -y 
sudo apt-get install bind-utils -y 
sudo apt-get install net-tools -y 
sudo apt get install curl -y 
sudo apt-get install bash-completion
#install golang
sudo apt install golang
# install docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# installl docker compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
# install  k8s
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.12.0/kind-linux-amd64
chmod +x ./kind
# install  kubectl
sudo curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# START DOCKER
sudo gpasswd -a $USER  docker
sudo gpasswd -a $USER root
sudo service docker start 
sudo usermod -aG docker $USER
newgrp docker



