# USER INTERFACE HELPER FUNCTIONS
import sys

GREEN = "\u001b[32m"

RESET = "\u001b[0m"

HEADER = f"""
{GREEN}   ___     {RESET} _ __ _  _ __ _(_)_ _ __ __
{GREEN}  /   \\  {RESET} | '_ \\ || / _` | | ' \\ \\ /
{GREEN} | {RESET}|\\|{GREEN} | {RESET} | .__/\\_, \\__, |_|_||_/_\\_\\
{GREEN}  \\___/  {RESET} |_|   |__/|___/ {GREEN}............{RESET}
"""


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


def show_options(options: dict[str, ...], prompt=None, default="", allow_no_input=False) -> ...:
    """
    displays options for the user to select one

    Parameters
    ----------
    options : dict
        this dict should contain the different options as keys.
        the should follow the pattern '[letter/word] description'
    prompt : str
        will be printed before the options are displayed
    default : ...
        will be returned if the user entered nothing
    allow_no_input : bool
        allows the user to enter nothing even if default is None

    Returns
    -------
    ... :
        the matching value for the selected key
    """
    parsed_options = {}
    for option in options:
        parsed_options[option[option.find("[") + 1: option.find("]")]] = option

    if prompt:
        print(prompt)
    for option in options:
        print(option)

    while True:
        selection = input("? > ")
        if selection == "" and default:
            return default
        if selection not in parsed_options:
            print_error("Invalid Selection")
        else:
            return options[parsed_options[selection]]


def print_error(msg: str):
    print('✘', msg)


def print_success(msg: str):
    print('✔', msg)
