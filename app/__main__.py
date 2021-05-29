# https://github.com/hnasr/javascript_playground/tree/master/nginx

import os
import sys
import subprocess
from typing import Any

import validators

from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader

# set up jinja2
file_loader = FileSystemLoader("./templates")
jinja_env = Environment(loader=file_loader)


@dataclass(frozen=True)
class LocationType:
    pass


class Root(LocationType):
    path: str


class ProxyPass(LocationType):
    forward_scheme: str
    forward_host: str
    forward_port: str


@dataclass(frozen=True)
class Location:
    location_path: str
    location_type: LocationType

    def validate(self) -> bool:
        return True


@dataclass(frozen=True)
class HTTPServer:
    http_port: str
    server_name: list[str]
    ipv6_support: bool
    redirect_http_to_https: bool

    type: str = "HTTP_SERVER"


class HTTPSServer(HTTPServer):
    https_port: str
    enable_HSTS: bool
    use_http2: bool

    type: str = "HTTPS_SERVER"


@dataclass(frozen=True)
class UpstreamServer:
    addr: str
    port: str

    def validate(self):
        return any([self.addr == 'localhost',
                    validators.domain(self.addr),
                    validators.ipv4(self.addr),
                    validators.ipv6(self.addr)]) \
               and self.port.isnumeric()


@dataclass(frozen=True)
class Upstream:
    name: str
    servers: list[UpstreamServer]


# USER INTERFACE HELPER FUNCTIONS

def display_menu(options: dict):
    while True:
        print("What to you want to do?")
        for option in options.values():
            print(option["text"])

        if (selection := input("> ").lower().strip()) in options:
            options[selection]["func"]()
        else:
            print("invalid selection")


def ask_yes_no(question="", default="Yes") -> bool:
    """
    this function asks the user a yes or no question. it will return True, if the user entered the same answer as
    the default answer, so if the default is 'Yes' and the entered 'y', True will be returned

    Parameters
    ----------
    question : str
        will be printed
    default : str
        whether 'Yes' or 'No' is the default answer

    Returns
    -------
    bool :
        return whether the answer was the default answer
    """

    print(question.strip(), "[Y/n] : " if default == "Yes" else "[y/N] : ", end="")

    while (_in := input().strip().lower()) not in ["", "y", "n"]:
        print("Invalid Option, enter again: ", end="")

    if default == "Yes":
        return _in in ["", "y"]
    elif default == "No":
        return _in in ["", "n"]


def exit_error(msg: str, exit_code=-1):
    """
    prints an error messages and exits the program

    Parameters
    ----------
    msg : str
        will be printed
    exit_code : int
        the exit code of the program
    """
    print(msg, file=sys.stderr)
    exit(exit_code)


def input_with_default(prompt="", default="") -> str:
    """
    this functions prompt the user for input and if the user enters nothing the default is used

    Parameters
    ----------
    prompt : str
        will be printed before the input, should contain a message explaining what the default is
    default : str
        will returned if the user enters nothing

    Returns
    -------
    str :
        either the input or the default
    """
    return _in if (_in := input(prompt)) else default


def show_options(options: dict[str, ...], prompt="") -> ...:
    """
    displays options for the user to select one

    Parameters
    ----------
    options : dict
        this dict should contain the different options as keys.
        the should follow the pattern '[letter/word] description'
    prompt : str
        will be printed before the options are displayed

    Returns
    -------
    ... :
        the matching value for the selected key
    """
    parsed_options = {}
    for option in options:
        parsed_options[option[option.find("["): option.find("]")]] = option

    if prompt:
        print(prompt)
    for option in options:
        print(option)

    while True:
        selection = input("> ")
        if selection not in parsed_options:
            print_error("Invalid Selection")
        else:
            return options[parsed_options[selection]]


# GENERAL HELPER FUNCTIONS

def print_error(msg: str):
    print(msg, file=sys.stderr)


def check_root():
    """
    this function checks if the script is run with root privileges. if not, it issues an error message and exits,
    otherwise the function returns
    """
    if not os.geteuid() == 0:
        exit_error("You must run this script as root", 1)


def check_installs():
    """
    this function checks if all system utilities are installed

    if checks for:
        - nginx
        - certbot (with nginx plugin)

    if not everything is installed, it prompts the user whether to install them.
    if not, the function will exit the program
    """
    print("Checking dependencies...", end="\n")

    # nginx
    try:
        subprocess.run(["nginx", "-v"])
    except FileNotFoundError:
        if ask_yes_no(question="Nginx is not installed on your system, do you want to install it?"):
            subprocess.run(["apt-get", "update"])
            return_code = subprocess.run(["apt-get", "install", "nginx", "-y"]).returncode

            if return_code == 0:
                print("\nNginx was successfully installed!\n")
                subprocess.run(["systemctl", "status", "nginx"])
            else:
                exit_error("Unable to install nginx")
        else:
            exit_error("This script can only be run when nginx is installed")

    # lets encrypt
    try:
        subprocess.run(["certbot", "--nginx", "--version"])
    except FileNotFoundError:
        if ask_yes_no(question="LetsEncrypt is not installed on your system, do you want to install it?"):
            subprocess.run(["apt-get", "update"])
            return_code = subprocess.run(["apt-get", "install", "python3-certbot-nginx", "-y"]).returncode

            if return_code == 0:
                print("LetsEncrypt was successfully installed!")
                subprocess.run(["certbot", "--nginx", "--version"])
            else:
                exit_error("Unable to install LetsEncrypt")
        else:
            exit_error("This script can only be run when nginx is installed")


# NGINX CONF FUNCTIONS

def collect_upstream_data() -> list[Upstream]:
    """
    this function prompts the user to enter the data for one oder multiple upstreams

    Returns
    -------

    """
    upstreams: list[Upstream] = []

    while True:

        upstream_name = input_with_default("Enter the name of the upstream.txt (the default is 'backend'): ", "backend")

        # todo load balancing algorithm : https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/

        upstream_servers: list[UpstreamServer] = []
        while True:
            server_addr = input_with_default("Enter the server IP oder DNS-name (the default is 'localhost'): ",
                                             "localhost")
            server_port = input_with_default("Enter the port the server is listening on (the default is '80'): ", "80")

            server = UpstreamServer(addr=server_addr, port=server_port)

            if server.validate():
                upstream_servers.append(server)
                if ask_yes_no(question="Add additional servers?", default="No"):
                    break
            else:
                print_error("Invalid entries")

        upstreams.append(Upstream(name=upstream_name, servers=upstream_servers))

        if ask_yes_no(question="Add additional upstream?", default="No"):
            return upstreams


def collect_http_server_data(upstreams: list[Upstream]) -> list[HTTPServer]:
    servers: list[HTTPServer] = []

    while True:
        enable_ssl = ask_yes_no("Do you want to enable ssl on this server?")
        forward_http_to_https = ask_yes_no("Do you want to forward http to https")

        locations: list[Location] = []
        print("Configuring Locations ...")
        while True:
            path = input_with_default("Enter the path of the location (the default is '/'): ", "/")


def add_http_stream():
    print("adding http stream")


def add_tcp_stream():
    print("adding tcp stream")


if __name__ == '__main__':
    # check_root()
    # check_installs()

    """display_menu(options={
        "a": {"func": add_http_stream, "text": "[a] add new server"},
        "s": {"func": add_tcp_stream, "text": "[s] add new tcp stream"},
        "h": {"func": lambda: print("Not yet implemented!\n"), "text": "[h] display help text"},
        "q": {"func": lambda: exit(0), "text": "[q] quit"}
    })"""

    ups = collect_upstream_data()

    print(ups)

    template = jinja_env.get_template("upstream")

    print(template.render(upstreams=ups))
