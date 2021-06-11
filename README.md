```txt
   ___     _ __ _  _ __ _(_)_ _ __ __
  /   \   | '_ \ || / _` | | ' \\ \ /
 | |\| |  | .__/\_, \__, |_|_||_/_\_\
  \___/   |_|   |__/|___/ ............
```

Python scripts to automate nginx virtual server and stream deployment.

Tested on `Debian` with `Python 3.7.3`

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

todo!

## Usage

The script has two functions: to create a config file for a virtual http server
and to create the config file for a stream.

### Create http server

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

### Create a stream (aka port forwarding)

Run `sudo pyginx stream -h` to get stream specific help.

To create the config file run

```shell
$ sudo pyginx stream -p 8080 -u backend1.example.com:80 backend1.example.com:81
# or 
$ sudo pyginx http -p 8080 -u backend1.example.com:80 backend1.example.com:81
```

With `-p` you can specify the port to be forwarded. The upstreams are specified as above.

### Additional parameters

Run the following to list all:

```shell
sudo pyginx --help
```

| Parameter         | Info                              |
|-------------------|-----------------------------------|
| `--version`       | show program's version number and exit    |
| `--config-file`   | after this flag a custom config file can be specified. the default config file in located here: `/etc/pyginx.d/pyginx.ini` |



















