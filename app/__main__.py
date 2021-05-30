# https://github.com/hnasr/javascript_playground/tree/master/nginx

from data_objects import *

from jinja2 import Environment, FileSystemLoader

# set up jinja2
from user_interface import *

file_loader = FileSystemLoader("http_templates")
jinja_env = Environment(loader=file_loader)


# NGINX CONF FUNCTIONS

def collect_upstream_data() -> list[Upstream]:
    """
    this function prompts the user to enter the data for one oder multiple upstreams

    Returns
    -------
    list :
        a list containing all upstreams the user entered
    """
    upstreams: list[Upstream] = []

    while True:

        upstream_name = input_with_default("Enter the name of the upstream.txt (the default is 'backend'): ", "backend")

        load_balancing_algorithm = show_options(
            prompt="Do you want to change the load-balancing algorithm? (The default is Round Robin)",
            options={
                "[0] ip_hash": "ip_hash",
                "[1] least_conn": "least_conn;"
            },
            allow_no_input=True,
            default=""
        )

        upstream_servers: list[UpstreamServer] = []
        while True:
            server_addr = input("Enter the address of the server : ")
            server_port = input("Enter the port of the server    : ")

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
        enable_ssl = ask_yes_no("Do you want to enable ssl?  ", default="Yes")
        ipv6_support = ask_yes_no("Do you want to enable ipv6? ", default="Yes")
        enable_HSTS = ask_yes_no("Do you want to enable HSTS? ", default="Yes")

        server_name = input("""Enter the name under which the server should be accessible.
Separate multiple names with commas. (e.g.: example.com www.example.com)
? > """)

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

    while option := show_options(
            prompt=HEADER,
            options={
                "[a] add new server": add_http_stream,
                "[s] add new tcp stream": add_tcp_stream,
                "[h] display help text": lambda: print_error("Not yet implemented!\n"),
                "[test] for testing purposes": lambda: print_success("TEST"),
                "[q] quit": ""
            }):
        option()
