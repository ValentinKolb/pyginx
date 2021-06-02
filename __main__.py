# https://github.com/hnasr/javascript_playground/tree/master/nginx

import subprocess
from data_objects import HTTPTemplate
from user_interface import *
from jinja2 import Environment, FileSystemLoader

# set up jinja2
file_loader = FileSystemLoader("http_templates")
jinja_env = Environment(loader=file_loader, lstrip_blocks=True, trim_blocks=True)

# global variables
websocket_support = False


def add_http_stream():

    http_template_data = HTTPTemplate()
    template = jinja_env.get_template("base")

    with open(f"temp/{http_template_data.config_name}.conf", "w") as config_file:
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
            "[s] add new tcp stream": lambda: print_error("Not yet implemented!\n"),
            "[h] display help text": lambda: print_error("Not yet implemented!\n"),
            "[q] quit": lambda: None
        },
        default=add_http_stream)()
