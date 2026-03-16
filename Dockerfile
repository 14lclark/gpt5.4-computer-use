FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive


RUN echo "Acquire::http::Pipeline-Depth 0; Acquire::http::No-Cache true; Acquire::BrokenProxy true;" >> /etc/apt/apt.conf.d/99fixbadproxy
RUN apt-get update 
RUN apt-get update 
RUN apt-get install -y xfce4 xfce4-goodies x11vnc xvfb xdotool imagemagick x11-apps sudo software-properties-common firefox-esr && \
    apt-get remove -y light-locker xfce4-screensaver xfce4-power-manager || true  && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash agent-user     && echo "agent-user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
# USER agent-user

CMD ["sleep", "infinity"]
# WORKDIR /home/agent-user

# RUN x11vnc -storepasswd secret /home/agent-user/.vncpass

# EXPOSE 5900
# CMD ["/bin/sh", "-c", "\
#     Xvfb :99 -screen 0 1280x800x24 >/dev/null 2>&1 & \
#     x11vnc -display :99 -forever -rfbauth /home/agent-user/.vncpass -listen 0.0.0.0 -rfbport 5900 >/dev/null 2>&1 & \
#     export DISPLAY=:99 && \
#     startxfce4 >/dev/null 2>&1 & \
#     sleep 2 && echo 'Container running!' && \
#     tail -f /dev/null \
# "]