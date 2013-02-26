#!/usr/bin/env python
import os
import time
from boto.ec2 import connect_to_region
from boto import config

# alestic Ubuntu 12.04 LTS Precise EBS boot
AMI_ID = 'ami-3b65664f'

# ubuntu 12.04 lts
# AMI_ID = 'ami-c1aaabb5'


def connection():
    secret = config.get('credentials', 'aws_secret_access_key')
    key = config.get('credentials', 'aws_access_key_id')
    return connect_to_region('eu-west-1', aws_access_key_id=key,
                             aws_secret_access_key=secret, debug=2)


def userdata():
    with open(os.path.join(os.path.dirname(__file__), 'bootstrap.sh'), 'r') as fo:
        return fo.read()


def security_groups():
    return 'puppets', 'port8080', 'default'


def main():
    conn = connection()
    reservations = conn.run_instances(AMI_ID,
                                      instance_type='m1.medium',
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
