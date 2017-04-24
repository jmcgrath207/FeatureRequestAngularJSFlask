FROM python:2.7

#install all system and python dep

WORKDIR /usr/src/app

RUN apt-get update  && apt-get install -y supervisor\
   gcc \
	 python-pip \
	 git \
	 openssh-server \
	 passwd \
	 python-dev \
   libssl-dev \
	 libffi-dev \
	 uwsgi-plugin-python \
	 sudo \
	 vim \
	&& rm -rf /var/lib/apt/lists/*



COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt && cd /etc && rm -f localtime && ln -s /usr/share/zoneinfo/US/Central localtime && \
echo 'syntax on'      >> /root/.vimrc && echo 'alias vi="vim"' >> /root/.bash_profile && \
mkdir /var/run/sshd && mkdir -p /usr/src/app && mkdir -p /var/log/supervisor

# Adding all the files in web root

COPY . /usr/src/app

# Custom Supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

#ONBUILD Start script
RUN chmod 755 config.sh && sleep 1s && ./config.sh



