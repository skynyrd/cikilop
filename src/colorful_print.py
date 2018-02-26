from colorama import Fore, Style


def print_green(to_be_printed):
    print(f'{Fore.GREEN}{to_be_printed}{Style.RESET_ALL}')


def print_red(to_be_printed):
    print(f'{Fore.RED}{to_be_printed}{Style.RESET_ALL}')


def print_blue(to_be_printed):
    print(f'{Fore.LIGHTCYAN_EX}{to_be_printed}{Style.RESET_ALL}')
