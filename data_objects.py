from dataclasses import dataclass
from typing import Optional

import validators


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
    servers: list[UpstreamServer]
    name: str = "backend"
    load_balancing_algorithm: str = "# use default Round Robin"
    comment: Optional[str] = None


@dataclass(frozen=True)
class ProxyPass:
    upstream: Upstream
    scheme: str = "http"


@dataclass(frozen=True)
class Location:
    proxy_pass: Optional[ProxyPass] = None
    root: Optional[str] = None
    max_file_size: str = "1MB"
    location_path: str = "/"
    comment: str = ""
    websocket_support: bool = True


@dataclass(frozen=True)
class HTTPServer:
    server_name: str
    locations: list[Location]
    ipv6_support: bool = True
    enable_HSTS: bool = True
    comment: Optional[str] = None


@dataclass(frozen=True)
class EventBlock:
    pass


@dataclass(frozen=True)
class HTTPBlock:
    upstreams: list[Upstream]
    http_servers: list[HTTPServer]
    websocket_support: bool = True


@dataclass(frozen=True)
class HTTPTemplate:
    config_name: str
    events: EventBlock
    http: HTTPBlock


_backend_upstream = Upstream(
    name="backend",
    servers=[
        UpstreamServer(
            addr="localhost",
            port="80"
        ),
        UpstreamServer(
            addr="localhost",
            port="81"
        )
    ]
)

_backend_upstream_backup = Upstream(
    name="backend_backup",
    servers=[
        UpstreamServer(
            addr="backup.server",
            port="80"
        ),
        UpstreamServer(
            addr="backup.server",
            port="81"
        )
    ],
    comment="This upstream is used as a backup",
    load_balancing_algorithm="iphash"
)

example_http_template_data = HTTPTemplate(
    config_name="TEST-CONFIG",
    events=EventBlock(),
    http=HTTPBlock(
        upstreams=[
            _backend_upstream,
            _backend_upstream_backup
        ],
        http_servers=[
            HTTPServer(
                server_name="example.com www.example.com",
                ipv6_support=False,
                enable_HSTS=True,
                locations=[
                    Location(
                        location_path="/",
                        max_file_size="20G",
                        proxy_pass=ProxyPass(
                            scheme="http",
                            upstream=_backend_upstream

                        ),
                        root=""
                    ),
                    Location(
                        location_path="/404",
                        max_file_size="1K",
                        proxy_pass=None,
                        root="/var/www/404.html"
                    )

                ],
            )
        ],
        websocket_support=True
    )
)
