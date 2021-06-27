```txt
   ___     _ __ _  _ __ _(_)_ _ __ __
  /   \   | '_ \ || / _` | | ' \\ \ /
 | |\| |  | .__/\_, \__, |_|_||_/_\_\
  \___/   |_|   |__/|___/ ............
```

Python scripts to automate nginx virtual server and stream deployment.


[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/ValentinKolb/pyginx) 

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![made-with-bash](https://img.shields.io/badge/Made%20with-Bash-1f425f.svg)](https://www.gnu.org/software/bash/) 

![Python Version](https://img.shields.io/badge/Python-3.7.3%2B-yellow) ![Debian](https://img.shields.io/badge/Debian-10%20(buster)-orange) ![nginx version](https://img.shields.io/badge/nginx-1.18.0--6.1%20-green)

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

## Dependencies

* python3
* Nginx (obviously)
* python3-certbot-nginx (if you plan to use ssl)

### Python Dependencies

These will be automatically installed if you use the script.

* jinja2
* validators

## Install 

### Install with script (recommend)

```shell
curl https://raw.githubusercontent.com/ValentinKolb/pyginx/main/install.sh | bash
```

**Caution**: This deletes all previous versions of pyginx on your system and override the default config file.
Be sure to back it up if you changed anything.

**Disclaimer**: This script will install pip3 on your system to install all python dependencies.

### Manuel install

```shell
$ git clone git@github.com:ValentinKolb/pyginx.git
$ cd pyginx
$ sudo pip3 install -r requirements.txt

# run
$ sudo python3 pyginx --help
...
```

## Nginx Configuration

For this script to work, your nginx instance must be configured in a specific way.

See [here](https://github.com/ValentinKolb/nginx.conf) for more information.

## Usage

The script has two functions: to create a config file for a virtual http server
and to create the config file for a stream.

### Create http v-server

Run `sudo pyginx http -h` to get http-server specific help.

To create the config file simply type the following

```shell
$ sudo pyginx http -d example.com -u backend1.example.com:80 backend2.example.com:80
# or 
$ sudo pyginx http -d example.com -u backend1.example.com:80 backend2.example.com:80 --no-ssl
```

After `-d` the domain of the virtual server must be entered. With the `-u` parameter all upstream backends can be listed

If `--no-ssl` is specified all is ready now. The created config file opens automatically in nano to edit it further
and when it is correct, nginx is reloaded automatically.

If the flag is not specified certbot will be run automatically to create a certificate.

```shell
$ [sudo] pyginx http -h # for help sudo is not required
...
usage: pyginx http [-h] -d  --upstreams  [...] [--backendName] [--forwardScheme] [--no-ssl]

optional arguments:
  -h, --help            show this help message and exit
  --backendName , -b    The name of the backend. The default value is 'backend_<label/domain>'.
  --forwardScheme       The forward scheme for the backend. Must be 'http' (default) or 'https'
  --no-ssl              Disable SSL: prevent to automatically run certbot to request a ssl certificate and enable https

required:
  -d , --domain         The domain under which the service is reachable. This must be a fully qualified domain name. (e.g. example.com)
  --upstreams  [ ...], -u  [ ...]
                        The upstream and port where the connection is forwarded to. Separate multiple upstreams by spaces. Format: <domain/ip>:<port>
```

### Create a stream (aka port forwarding)

Run `sudo pyginx stream -h` to get stream specific help.

To create the config file run

```shell
$ sudo pyginx stream -p 8080 -u backend1.example.com:80 backend1.example.com:81
# or 
$ sudo pyginx http -p 8080 -u backend1.example.com:80 backend1.example.com:81
```

With `-p` you can specify the port to be forwarded. The upstreams are specified as above.

```shell
$ [sudo] pyginx stream -h # for help sudo is not required
...
usage: pyginx stream [-h] --upstreams  [...] --port  [--backendName]

optional arguments:
  -h, --help            show this help message and exit
  --backendName , -b    The name of the backend. The default value is 'backend_<label/port>'.

required:
  --upstreams  [ ...], -u  [ ...]
                        The upstream and port where the connection is forwarded to. Separate multiple upstreams by spaces. Format: <domain/ip>:<port>
  --port , -p           The port that to be forwarded.

```

### Additional parameters

Run the following to list all:

```shell
$ [sudo] pyginx --help # for help sudo is not required
...
usage: pyginx [-h] [--version] [--config-file] [--label] [--mock] [--verbose | --quiet] {http,stream} ...

Python script to automate nginx virtual server and stream deployment.

positional arguments:
  {http,stream}   run 'pyginx <usage> -h' for more info
    http          Run this command to create a new config file for an http virtual server
    stream        Created a new config file for a tcp stream (i.e port-forwarding). For this the port on this server must be exposed by the firewall

optional arguments:
  -h, --help      show this help message and exit
  --version       Show Version.
  --config-file   The path of the pyginx config file.
  --label         This label is used for the filename of the configuration and log file and for the name of the backend. The default value is the domain for 'http' and the public port for 'stream'
  --mock          Run script in mock mode. In this mode the config is not saved and nginx is not reloaded. Certbot will also not be run.
  --verbose       Verbose output.
  --quiet         Minimal output.

```

### Coming Soon

- [x] specify forward scheme for http backend
- [x] specify backend name
- [x] don't use nano but $EDITOR as default editor for files
- [ ] specify load balancing algorithm for the backend
- [x] list all current config files
- [ ] install and set up nginx
- [ ] remove, edit and disable commands
















