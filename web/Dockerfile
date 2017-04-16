FROM python:2.7



###System Dep####
RUN apt-get update

RUN apt-get install -y supervisor\
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

### Add app and install dep ###

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app


RUN pip install --no-cache-dir -r requirements.txt

####System Settings#####


#Change Time Zone
RUN cd /etc
RUN rm -f localtime
RUN ln -s /usr/share/zoneinfo/US/Central localtime


# install vim
RUN echo 'syntax on'      >> /root/.vimrc && echo 'alias vi="vim"' >> /root/.bash_profile


#####SSH##########

RUN mkdir /var/run/sshd


####Supervisord####

RUN mkdir -p /var/log/supervisor

# Custom Supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

#ONBUILD Start script
RUN chmod 755 config.sh
RUN ./config.sh



