FROM ubuntu:22.04

# set workspace as workdir
WORKDIR /workspace

# install utils 
RUN apt-get update && apt-get install -y git python3 pip python3-dev

# create a folder for the creator script
RUN mkdir -p /usr/local/creator

# copy creator to the installation folder to the workspace
COPY ./creator/ /usr/local/creator/

# clone tar code
RUN git clone https://git.savannah.gnu.org/git/tar.git

# clone musl cross-compilers creator
RUN git clone https://github.com/sudogauss/musl-cross-make.git

# install launcher
RUN cd /usr/local/creator && pip install .

ENTRYPOINT ["/bin/bash"]