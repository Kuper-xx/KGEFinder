# Tool Title: Kuper-xx Github Email Finder (KGEFinder.py)
# Date: 2024-20-05
# Author: Kuper-xx
# Version 1.0.0
import requests
import re
from colorama import Fore, Back, Style, init
import pyfiglet
import signal
import sys

# Ctrl + C
def signal_handler(sig, frame):
    print('\n')
    print(f'{Fore.CYAN}[!] Exiting...{Style.RESET_ALL}')
    sys.exit(0)
# Initialize colorama
init(autoreset=True)

def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"{Fore.RED}[!] The username does not exist.")
    
    repos = response.json()
    if not repos:
        raise Exception(f"{Fore.RED}[!] Email not found.")
    
    return repos

def get_commits(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"{Fore.RED}[!] Error. 666")
    
    return response.json()

def extract_email_from_patch(patch_url):
    response = requests.get(patch_url)
    if response.status_code != 200:
        raise Exception(f"{Fore.RED}[!] Error. 777")
    
    patch_content = response.text
    email_match = re.search(r'From:.*<(.+?)>', patch_content)
    if email_match:
        return email_match.group(1)
    else:
        return None
def print_with_border(text):
    border = "=" * len(text)
    print(f"{Fore.GREEN}{border}")
    print(f"{Fore.GREEN}{text}")
    print(f"{Fore.GREEN}{border}")

def check_commits_for_verification(username):
    repos = get_repos(username)
    for repo in repos:
        repo_name = repo['name']
        commits = get_commits(username, repo_name)
        
        for commit in commits:
            if not commit['commit']['verification']['verified']:
                patch_url = f"{commit['html_url']}.patch"
                email = extract_email_from_patch(patch_url)
                if email:
                    print_with_border(f"{Fore.GREEN}[*] Email Found: {email}")
                else:
                    print(f"{Fore.RED}[!] Email not found.")
                return
    
    print(f"{Fore.RED}[!] Email not found.")

if __name__ == "__main__":
    # Register the Ctrl+C signal handler
    signal.signal(signal.SIGINT, signal_handler)
    banner = pyfiglet.figlet_format("KGEFinder.py")
    print(f"{Fore.YELLOW}{banner}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Created by: @Kuper-xx{Style.RESET_ALL}")
    print(f"\n")
    username = input(f"{Fore.YELLOW}[*] Introduce the target Github username: {Style.RESET_ALL}")
    try:
        check_commits_for_verification(username)
    except Exception as e:
        print(e)
