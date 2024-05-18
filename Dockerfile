FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04

LABEL maintainer="Esteban MARTEL <martel.esteban.33@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3-pip \
    build-essential \
    cmake \
    libopencv-dev \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && bash ~/miniconda.sh -b -p $HOME/miniconda \
    && rm ~/miniconda.sh \
    && $HOME/miniconda/bin/conda init \
    && $HOME/miniconda/bin/conda config --set auto_activate_base false

ENV PATH="/root/miniconda/bin:$PATH"

WORKDIR /app
COPY . .

RUN conda create -n video-bg-changer python=3.11

SHELL ["conda", "run", "-n", "video-bg-changer", "/bin/bash", "-c"]

RUN conda install -n video-bg-changer setuptools wheel \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

RUN conda install -n video-bg-changer pytorch torchvision torchaudio -c pytorch

# Exposer le port utilisé par l'application (si nécessaire)
# EXPOSE 5000

# Commande pour exécuter l'application
CMD ["bash", "-c", "source ~/.bashrc && conda activate video-bg-changer && python3 BackgroundChanger.py"]
