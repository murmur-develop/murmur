FROM python:3.11

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG INSTALL_ZSH=true

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN apt-get install -y ffmpeg libnacl-dev python3-dev
RUN python -m pip install --upgrade pip

# devcontainer common script
RUN git clone --depth 1 https://github.com/microsoft/vscode-dev-containers.git
RUN bash vscode-dev-containers/script-library/common-debian.sh "${INSTALL_ZSH}" "${USERNAME}" "${USER_UID}" "${USER_GID}" \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/library-scripts

USER $USERNAME