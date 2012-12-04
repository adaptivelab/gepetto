#!/usr/bin/env python
import ConfigParser
import collections
import time
import sys
from boto.ec2 import connect_to_region

Credentials = collections.namedtuple('Credentials', ['key', 'secret'])


class Config(object):

    @property
    def config(self):
        if not hasattr(self, '_config'):
            try:
                fp = open('creds.ini')
            except IOError as err:
                sys.exit(err)
            config = ConfigParser.ConfigParser()
            config.readfp(fp)
            self._config = config
        return self._config

    def __call__(self):
        return self.config


get_config = Config()


# alestic Ubuntu 12.04 LTS Precise EBS boot
AMI_ID = 'ami-3b65664f'

# ubuntu 12.04 lts
# AMI_ID = 'ami-c1aaabb5'


def credentials():
    config = get_config()
    secret = config.get('credentials', 'aws_secret_access_key')
    key = config.get('credentials', 'aws_access_key_id')
    return Credentials(key=key, secret=secret)


def connection():
    creds = credentials()
    return connect_to_region('eu-west-1', aws_access_key_id=creds.key,
                             aws_secret_access_key=creds.secret, debug=2)


def userdata():
    with open('bootstrap.sh', 'r') as fo:
        return fo.read()


def security_groups():
    return 'puppets', 'port8080', 'default'


def main():
    conn = connection()
    reservations = conn.run_instances(AMI_ID,
                                      instance_type='t1.micro',
                                      key_name='jenkins',
                                      security_groups=security_groups(),
                                      user_data=userdata(), max_count=1)
    instance = reservations.instances[0]
    status = instance.update()
    while status == 'pending':
        time.sleep(5)
        status = instance.update()
    if status == 'running':
        instance.add_tag("Name", "Jenkins")


if __name__ == "__main__":
    main()
