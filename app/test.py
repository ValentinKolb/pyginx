from jinja2 import FileSystemLoader, Environment
from data_objects import example_http_template_data

file_loader = FileSystemLoader("http_templates")
jinja_env = Environment(loader=file_loader, lstrip_blocks=True, trim_blocks=True)

if __name__ == '__main__':
    server_name = input("""Enter the name under which the server should be accessible.
Separate multiple names with commas. (e.g.: example.com www.example.com)
? > """)