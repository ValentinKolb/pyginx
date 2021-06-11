#!/usr/bin/env python3
from configparser import ConfigParser, ExtendedInterpolation
parser = ConfigParser(interpolation=ExtendedInterpolation())

config_file = "pyginx.d/pyginx.ini"

parser.read(config_file)


print(dict(parser.items("Templates")))
