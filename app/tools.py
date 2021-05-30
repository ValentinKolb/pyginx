import os
import subprocess

from app.user_interface import exit_error, ask_yes_no


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