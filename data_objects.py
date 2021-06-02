from dataclasses import dataclass, field
from typing import Optional, Union
from user_interface import prompt_user, prompt_for_list, ask_yes_no, show_options

import validators

enter_comment = lambda: prompt_user("Do you want to enter a comment?", default='')


def validate_dns_or_ip(addr: str) -> bool:
    return any([addr == 'localhost',
                validators.domain(addr),
                validators.ipv4(addr),
                validators.ipv6(addr)])


def validate_port(port: str) -> bool:
    try:
        return 1 <= int(port) <= 65535
    except ValueError:
        return False


def validate_scheme(scheme: str) -> bool:
    return scheme in ["http", "https"]


@dataclass(frozen=True)
class UpstreamServer:
    addr: str = field(
        default_factory=lambda: prompt_user("Please enter the Server Address",
                                            validator=validate_dns_or_ip,
                                            default='localhost')
    )
    port: str = field(
        default_factory=lambda: prompt_user("Please enter the Port",
                                            validator=validate_port,
                                            default="80")
    )


@dataclass(frozen=True)
class Upstream:
    name: str = field(
        default_factory=lambda: prompt_user(
            "Please enter the name of the backend. This must be unique to this configuration.",
            default="backend")
    )
    servers: list[UpstreamServer] = field(
        default_factory=lambda: prompt_for_list("Configuring Upstream Servers ...",
                                                '... Successfully Configured Upstream Servers',
                                                obj=UpstreamServer)
    )
    load_balancing_algorithm: str = field(
        default_factory=lambda: prompt_user("Do you want to change the load-balancing-algorithm?",
                                            default="# Round Robin")
    )
    comment: Optional[str] = field(
        default_factory=enter_comment
    )


@dataclass(frozen=True)
class ProxyPass:
    scheme: str = field(
        default_factory=lambda: prompt_user("Please enter the Scheme",
                                            validator=validate_scheme,
                                            default="http")
    )
    upstream: str = field(
        default_factory=lambda: prompt_user("Please enter the Name of the Upstream to be used. "
                                            "This has to be a Upstream you previously configured "
                                            "(e.g 'backend', the default name was chosen)")
    )


@dataclass(frozen=True)
class Root:
    root: str = field(
        default_factory=lambda: prompt_user("Please enter the Root File Dir. (e.g /var/www)")
    )


@dataclass(frozen=True)
class Location:
    location_path: str = field(
        default_factory=lambda: prompt_user("Please enter the Location Path (the part after the URL)",
                                            default="/")
    )

    data: Union[ProxyPass, Root, None] = field(
        default_factory=lambda: show_options(prompt="How do you want to configure this location?",
                                             options={
                                                 "[0] Use proxy_pass": ProxyPass,
                                                 "[1] Specify Root Location":
                                                     lambda: f'root {prompt_user("Please enter the Path (e.g /var/www)")}',
                                                 "[2] Use 'try_files $uri $uri/ =404'":
                                                     lambda: "try_files $uri $uri/ =404"
                                             })()
    )

    max_file_size: str = field(
        default_factory=lambda: prompt_user("Enter the Maximum allowed Filesize for the Request-Body",
                                            default="1MB")
    )
    websocket_support: bool = field(
        default_factory=lambda: not ask_yes_no("Do you want to enable Websocket-Support for this Location",
                                               default="No")
    )
    comment: str = field(
        default_factory=enter_comment
    )


@dataclass(frozen=True)
class HTTPServer:
    server_name: str = field(
        default_factory=lambda: prompt_user("Please enter the Name of this HTTP server. "
                                            "Separate multiple by commas (e.g example.com www.example.com)")
    )
    ipv6_support: bool = field(
        default_factory=lambda: ask_yes_no("Do you want to enable IPv6 for this Server",
                                           default="Yes")
    )
    enable_HSTS: bool = field(
        default_factory=lambda: ask_yes_no("Do you want to enable HSTS for this Server",
                                           default="Yes")
    )
    comment: Optional[str] = field(
        default_factory=enter_comment
    )
    locations: list[Location] = field(
        default_factory=lambda: prompt_for_list("Adding Locations to the Server ...",
                                                '... Successfully Configured Locations',
                                                obj=Location)
    )


@dataclass(frozen=True)
class EventBlock:
    pass


@dataclass(frozen=True)
class HTTPBlock:
    upstreams: list[Upstream] = field(
        default_factory=lambda: prompt_for_list("Configuring Upstreams ...",
                                                '... Successfully Configured Upstreams',
                                                obj=Upstream)
    )
    http_servers: list[HTTPServer] = field(
        default_factory=lambda: prompt_for_list("Configuring HTTP-Servers ... ",
                                                '... Successfully Configured HTTP Servers',
                                                obj=HTTPServer)
    )
    websocket_support: bool = True


@dataclass(frozen=True)
class HTTPTemplate:
    config_name: str = field(
        default_factory=lambda: prompt_user("Please enter the Name of this configuration (e.g the Server Name)")
    )
    events: EventBlock = field(default_factory=lambda: EventBlock())
    http: HTTPBlock = field(default_factory=lambda: HTTPBlock())
