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
