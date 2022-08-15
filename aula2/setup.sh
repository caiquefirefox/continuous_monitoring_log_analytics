#install basic packages
sudo apt-get install net-tools -y
sudo apt-get install curl -y
sudo apt-get install telnet -y 
sudo apt-get install bind-utils -y 
sudo apt-get install net-tools -y 
sudo apt get install curl -y 
sudo apt-get install bash-completion


# install docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker vagrant

# installl docker compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose


# install  k8s
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb

# install  kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl



# kubectl autocompletion
echo 'source <(kubectl completion bash)' >>~/.bashrc
kubectl completion bash >/etc/bash_completion.d/kubectl


export LC_ALL=C
sudo apt install -y python2-minimal; 
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py; 
python2 get-pip.py; 
sudo pip install cql PyYAML psutil ccm