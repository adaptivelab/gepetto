Gepetto
=======

Gepetto is a very thin wrapper over boto for creating jenkins servers. Usage is
simple as everything is hardcoded (for now)

Usage::

    python -m gepetto.up

As it uses boto under the covers the usual boto conventions of ``/etc/boto.cfg``,
``~/.boto`` or environment variables are used for authorisation. The author prefers
to create a local credentials files and use ``AWS_CREDENTIAL_FILE``::

    > cat creds.ini
    [credentials]
    aws_access_key_id = xxxxxxxxxxxxxxxxxxxx
    aws_secret_access_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    > AWS_CREDENTIAL_FILE=creds.ini python -m gepetto.up


Implementation
**************

Uses ``ami-3b65664f`` from `alestic.com <http://alestic.com>`_ to create an
Ubuntu 12.04 LTS server instance and utilises user-data to run the included
``bootstrap.sh`` which performs the following tasks to prepare the server

* sets the hostname to ``jenkinsalestic$TIMESTAMP.adaptive``
* downloads the required jenkins plugins (git, violations, performance, cobertura)
* installs and starts puppet

The puppetmaster is configured to autosign certificates and so the new jenkins
server should be setup via puppet immediately


TODO
****

There should be a dns entry (perhaps ci.adaptivelab.co.uk) pointing to an
elastic ip that can be re-allocated to any new jenkins instances to minimise
disruption

The puppet-builder templates could probably be bundled into this

Monit or similar to tell when a jenkins server needs rebuilding
