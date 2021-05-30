# https://github.com/hnasr/javascript_playground/tree/master/nginx

import subprocess
from data_objects import *
from user_interface import *
from jinja2 import Environment, FileSystemLoader

# set up jinja2
file_loader = FileSystemLoader("http_templates")
jinja_env = Environment(loader=file_loader, lstrip_blocks=True, trim_blocks=True)

# global variables
websocket_support = False


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

        upstream_name = input_with_default("Enter the name of the upstream (the default is 'backend'): ", "backend")

        load_balancing_algorithm = show_options(
            prompt="What load-balancing algorithm should this backend use?",
            options={
                "[1] Round Robin (default)": "# no load balancing method is specified for Round Robin",
                "[2] ip_hash": "ip_hash",
                "[3] least_conn": "least_conn;"
            },
            allow_no_input=True,
            default="# no load balancing method is specified for Round Robin"
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
        upstreams.append(Upstream(
            name=upstream_name,
            servers=upstream_servers,
            load_balancing_algorithm=load_balancing_algorithm,
            comment=input_with_default("Do you want to add a comment (default is none)? ", default="")
        ))
        if ask_yes_no("Do you want to add an additional upstream?", default="No"):
            return upstreams


def collect_location_data(upstreams: list[Upstream]) -> list[Location]:
    global websocket_support

    locations: list[Location] = []
    print("Configuring Locations ...")
    while True:
        path = input_with_default("Enter the path of the location (the default is '/'): ", "/")

        proxy_pass = None
        root = None
        selected_option = show_options(
            prompt="Where should this location be forwarded to?",
            options={
                "[1] use Proxy Pass (default)": "proxy_pass",
                "[2] specify Root file directory": "root",
                "[3] use 'try_files $uri $uri/ =404'": None
            },
            default="proxy_pass"
        )

        if selected_option == "proxy_pass":
            print("Configuring Proxy Pass ...")

            options = {}
            for i, upstream in enumerate(upstreams, start=1):
                options[f'[{i}] {upstream.name}'] = upstream.name
            proxy_pass = ProxyPass(
                upstream=show_options(
                    prompt="Which backend should be used for Proxy Pass?",
                    options=options
                )
            )
        elif selected_option == "root":
            print("Configuring Root file directory ...")
            root = input("Please enter the path: ")

        if _websocket_support := ask_yes_no("Do you want to add websocket support for this location?", default="Yes"):
            websocket_support = True
        locations.append(Location(
            proxy_pass=proxy_pass,
            root=root,
            location_path=path,
            websocket_support=_websocket_support,
            max_file_size=input_with_default("Please enter the maximal file size (the default is 1MB): ",
                                             default="1MB"),
            comment=input_with_default("Do you want to add a comment (default is none)? ", default="")
        ))

        if ask_yes_no("Do you want to add an additional location?", default="No"):
            return locations


def collect_http_server_data(upstreams: list[Upstream]) -> list[HTTPServer]:
    """
    this functions prompts the user for all data stored in a server block

    Parameters
    ----------
    upstreams : list
        all Upstreams configured to be used for a proxy_pass

    Returns
    -------
    list :
        all server blocks entered by the user
    """
    servers: list[HTTPServer] = []
    while True:
        servers.append(HTTPServer(
            server_name=input("Enter the domain (e.g. example.com, sepperate multiple by commas): "),
            ipv6_support=ask_yes_no("Do you want to enable ipv6?", default="Yes"),
            enable_HSTS=ask_yes_no("Do you want to enable HSTS?", default="Yes"),
            comment=input_with_default("Do you want to add a comment (default is none)? ", default=""),
            locations=collect_location_data(upstreams)
        ))
        if ask_yes_no("Do you want to add an additional server?", default="No"):
            return servers


def add_http_stream():
    """
    creates a config file for an http proxy and deploys it
    """

    def fast_config() -> HTTPTemplate:
        server_name = input("Enter the domain (e.g. example.com, sepperate multiple by commas): ")
        config_name = server_name.split()[0]
        while True:
            backend_server_addr = input("Enter the addr of the upstream server: ")
            backend_server_port = input("Enter the port of the upstream server: ")

            upstream_server = UpstreamServer(
                addr=backend_server_addr,
                port=backend_server_port
            )
            if upstream_server.validate():
                break
            else:
                print_error("Invalid , please enter again")

        upstream = Upstream(
            servers=[
                upstream_server
            ]
        )

        return HTTPTemplate(
            config_name=config_name,
            events=EventBlock(),
            http=HTTPBlock(
                upstreams=[
                    upstream
                ],
                http_servers=[
                    HTTPServer(
                        server_name=server_name,
                        locations=[
                            Location(
                                proxy_pass=ProxyPass(
                                    upstream=upstream
                                )
                            )
                        ]
                    )
                ]
            )
        )

    def detailed_config() -> HTTPTemplate:
        upstreams = collect_upstream_data()
        server_data = collect_http_server_data(upstreams)
        config_name = input_with_default(
            f"Enter the name of the configuration (the default is {server_data[0].server_name.split()[0]}): ",
            default=server_data[0].server_name.split()[0])
        return HTTPTemplate(
            config_name=config_name,
            events=EventBlock(),
            http=HTTPBlock(
                upstreams=upstreams,
                http_servers=server_data,
                websocket_support=websocket_support
            )
        )

    http_template_data = show_options(
        prompt="Do you want to use the autoconfig or the detailed configuration?",
        options={
            "[a] autoconfig (default)": fast_config,
            "[d] detailed config": detailed_config
        },
        default=fast_config
    )()

    template = jinja_env.get_template("base")

    with open("temp/temp.txt", "w") as config_file:
        config_file.write(template.render(HTTPTemplate=http_template_data))

    subprocess.call(["nano", "temp/temp.txt"])

    if ask_yes_no("Do you want to request a certificate and enable tls?", default="Yes"):
        pass
        # todo certbot
    else:
        pass
        # todo nginx -t and reload nginx


def add_tcp_stream():
    """
    TBD
    """
    print("adding tcp stream")


if __name__ == '__main__':
    # check_root()      # only use in production
    # check_installs()  # only user in production

    show_options(
        prompt=HEADER,
        options={
            "[a] add new server (default)": add_http_stream,
            "[s] add new tcp stream": add_tcp_stream,
            "[h] display help text": lambda: print_error("Not yet implemented!\n"),
            "[test] for testing purposes": lambda: print_success("TEST"),
            "[q] quit": ""
        },
        default=add_http_stream)()
