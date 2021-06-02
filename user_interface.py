# USER INTERFACE HELPER FUNCTIONS
import sys
from typing import Callable, TypeVar

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


def prompt_user(prompt: str,
                validator: Callable[[...], bool] = lambda s: s,
                default=None,
                error_phrase: str = "Invalid Input, please enter again") -> ...:
    """
    this function prompts the user to input something. it can be validated against something
    and a default can be specified

    Parameters
    ----------
    prompt : str
        will be printed before the user can enter something
    validator : (...) -> bool
        this function validated the user input. must take one parameter and return a bool
    default :
        if this is not None, the default will be returned if the user enters nothing,
        else nothing counts as invalid except the validator allows it.
        if a default value is specified, it will be added to the prompt
    error_phrase : str
        will be printed if the user enters something invalid

    Returns
    -------
    ... :
        either the default (if specified) or the user input
    """
    _in = input(f'{prompt.strip()} (default: {default!r}) : ' if default else f'{prompt.strip()} : ')
    if validator(_in):
        return _in
    else:
        return default if not _in and default is not None \
            else prompt_user(error_phrase, validator, default, error_phrase)


def prompt_for_list(start_prompt: str,
                    end_prompt: str,
                    obj,
                    enter_additional_prompt: str = None) -> list:
    """
    prompts the user to enter a list of objects. the objects must collect their data on their on in the __init__ method

    Parameters
    ----------
    start_prompt : str
        will be printed
    end_prompt : str
        will be printed at the end of the configuration
    obj : object
        the object the user show enter
    enter_additional_prompt : str
        will be printed to ask the user if an additional object should be entered

    Returns
    -------
    list :
        a list containing all entered objects
    """
    print(start_prompt)
    inputs = []
    while True:
        inputs.append(obj())
        if ask_yes_no(f"Do you want to enter an additional {inputs[0].__class__.__name__} ?"
                      if not enter_additional_prompt else enter_additional_prompt, default="No"):
            print(end_prompt)
            return inputs


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
