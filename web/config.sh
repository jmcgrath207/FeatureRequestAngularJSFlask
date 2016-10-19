#!/bin/bash

start() {

#ADD .ENV FILE
. /usr/src/app/.start_env

# Create a user to SSH into as.

if [ "$SSH_USER_LOGIN" = True ] ; then
    useradd -s /bin/bash $USER_NAME
    echo $USER_NAME':'$SSH_USER_PASS | chpasswd
    echo
    echo ssh user password: $SSH_USER_PASS
    echo
fi

if [ "$SSH_ROOT_LOGIN" = False ] ; then
    sed -i -e '/^PermitRootLogin/s/^.*$/PermitRootLogin no/' /etc/ssh/sshd_config
    echo "Removed Root SSH Access"
else
    echo 'root:'$SSH_ROOT_PASS | chpasswd
    echo
    echo ssh root password: $SSH_ROOT_PASS
    echo

fi

}

# Call all functions
start

#Add sed for =.*
#RUN for env in $(cat .env | grep ^[^#\;]); do unset  $env; done