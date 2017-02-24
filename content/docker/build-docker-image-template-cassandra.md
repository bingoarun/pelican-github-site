Title: Building images using templated conf files using Python
Date: 2017-02-24 15:02
Category: Docker
Tags: Docker, Cassandra
Slug: build-docker-image-template-cassandra
Authors: Arun prasath
Summary: Building images using templated configuration files using Python with Cassandra as example.


In Docker world, when building images it is a good practice to parameterize all the important configuration variables. This enables to launch the docker container with different configurations. The variables are provided mostly using Docker environment variables. For example, it is good to parameterize LISTEN_ADDRESS for nginx image. In ideal scenrio it is far better to mount the conf file directly in the image. But when you don't want to maintain an additional conf file, you can build the image in such a way that it can accept environment variables and apply the changes in configuration files.

One such example is Docker cassandra image [https://hub.docker.com/_/cassandra/](https://hub.docker.com/_/cassandra/)

In that image most of the configuration variables in cassandra.yaml can be changed by providing appropriate environment variables. Eg. CASSANDRA_LISTEN_ADDRESS, CASSANDRA_BROADCAST_ADDRESS .

Internally, that Docker image runs an entry point shell script which gets the environment variable and change the configuration file using sed.

```

if [ "$1" = 'cassandra' ]; then
	: ${CASSANDRA_RPC_ADDRESS='0.0.0.0'}

	: ${CASSANDRA_LISTEN_ADDRESS='auto'}
	if [ "$CASSANDRA_LISTEN_ADDRESS" = 'auto' ]; then
		CASSANDRA_LISTEN_ADDRESS="$(hostname --ip-address)"
	fi

	: ${CASSANDRA_BROADCAST_ADDRESS="$CASSANDRA_LISTEN_ADDRESS"}

	if [ "$CASSANDRA_BROADCAST_ADDRESS" = 'auto' ]; then
		CASSANDRA_BROADCAST_ADDRESS="$(hostname --ip-address)"
	fi
	: ${CASSANDRA_BROADCAST_RPC_ADDRESS:=$CASSANDRA_BROADCAST_ADDRESS}

	if [ -n "${CASSANDRA_NAME:+1}" ]; then
		: ${CASSANDRA_SEEDS:="cassandra"}
	fi
	: ${CASSANDRA_SEEDS:="$CASSANDRA_BROADCAST_ADDRESS"}

	sed -ri 's/(- seeds:).*/\1 "'"$CASSANDRA_SEEDS"'"/' "$CASSANDRA_CONFIG/cassandra.yaml"

	for yaml in \
		broadcast_address \
		broadcast_rpc_address \
		cluster_name \
		endpoint_snitch \
		listen_address \
		num_tokens \
		rpc_address \
		start_rpc \
	; do
		var="CASSANDRA_${yaml^^}"
		val="${!var}"
		if [ "$val" ]; then
			sed -ri 's/^(# )?('"$yaml"':).*/\2 '"$val"'/' "$CASSANDRA_CONFIG/cassandra.yaml"
		fi
	done

	for rackdc in dc rack; do
		var="CASSANDRA_${rackdc^^}"
		val="${!var}"
		if [ "$val" ]; then
			sed -ri 's/^('"$rackdc"'=).*/\1 '"$val"'/' "$CASSANDRA_CONFIG/cassandra-rackdc.properties"
		fi
	done
fi
```

It all looks pretty neat but what if we need to change a whole lot of variables or if we need to add additional configuration variable / environment variable. We will need to add additional logies to handle that variable. Also when the size grows big, the script looks ugly and unmanageble and unreadable.

In such case we can use Python to do the same job for all good reason. The idea is to template all the configuration files like Jinja2 format and use Python to get the environment variables and render the template. With this approach, you don't need to write a lot of 'if' in bash. Instead you can just mark the variable value as template.

```
listen_address: {{ env['CASSANDRA_LISTEN_ADDRESS'] or 'localhost' }}
```

Here the image with take the value from environment variable or it will use the default value with the environment value is not set.

The following is the Python code which accepts first argument as the templated file and renders a file with values from environment variables.

```
from jinja2 import Environment, FileSystemLoader
import os
import sys

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def print_html_doc():
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    print j2_env.get_template(sys.argv[1]).render(
        env=os.environ
    )

if __name__ == '__main__':
    print_html_doc()
```

Ofcourse you will still need a little bit of bash to redirect the output to the conf file location.

```
#!/bin/bash

python /apply-template.py /templates/cassandra.yaml.tmpl > /etc/cassandra/cassandra.yaml
python /apply-template.py /templates/cassandra-env.sh.tmpl > /etc/cassandra/cassandra-env.sh
```

But once such a setup is ready, you can easily use jinja2 templated variable values in configuration files and use environment variables to make changes to configuration files.

A fully built cassandra image is here for reference - [https://github.com/bingoarun/cassandra-docker-template-conf](https://github.com/bingoarun/cassandra-docker-template-conf)
