# Automation script to use on VM.
# In real life, this would be a CI/CD pipeline.

# Ensure docker is installed.
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common -y
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/debian \
    $(lsb_release -cs) \
    stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io -y

# Download model.
gsutil cp gs://gcp_workshop/my-xgb-model.model model/

# Build docker image.
sudo docker build . -t gcr.io/{insert-gcp-project-id}/server

# Configure docker auth.
echo y | sudo gcloud auth configure-docker

# Push to container registry.
sudo docker push gcr.io/{insert-gcp-project-id}/server
