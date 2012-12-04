#!/bin/bash

set -e -x

# required jenkins plugins:
# * violations
# * git
# * performance
# * cobertura
# restart jenkins

# if [ ! -n "$1" ]
# then
#     echo "Usage: $(basename $0) newhostname"
#     exit 1
# fi

HOSTNAME="jenkinsalestic-$(date --iso-8601=minutes | sed 's/://' | cut -d'+' -f1).adaptive"

# since we're now auto-signing on the puppetmaster we may no longer need to set the hostname
echo "$HOSTNAME" | sudo tee /etc/hostname
sudo hostname $(cat /etc/hostname)
test $(grep -c puppetmaster /etc/hosts) -lt 1 && echo "
10.48.235.26 puppet puppetmaster puppetmaster.eu-west-1.compute.internal
127.0.0.1    $HOSTNAME
54.246.87.68 jenkins" | sudo tee -a /etc/hosts

# download the required jenkins plugins
PLUGIN_URL='http://updates.jenkins-ci.org/download/plugins'
PLUGIN_DEST='/var/lib/jenkins/plugins'
sudo mkdir -p $PLUGIN_DEST

places=(git/1.1.16/git.hpi violations/0.7.11/violations.hpi performance/1.8/performance.hpi cobertura/1.7.1/cobertura.hpi)

for place in ${places[@]}; do
    dest="$PLUGIN_DEST/$(basename $place)"
    sudo wget -q -O $dest "$PLUGIN_URL/$place"
done

# install puppet and announce our presence to the puppetmaster
sudo apt-get -y update
sudo apt-get -y install puppet
sudo sed -i /etc/default/puppet -e 's/START=no/START=yes/'
sudo service puppet restart
# sudo puppet agent --verbose  --logdest console --no-daemonize --server=puppetmaster.eu-west-1.compute.internal
