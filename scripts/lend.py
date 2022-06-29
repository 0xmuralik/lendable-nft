from scripts.utils import get_account
from brownie import Lend


def main():
    """Entry"""


def deploy():
    """Deploy Lending contract"""
    account = get_account
    lend = Lend.deploy({"from": account})
    print(f"Contract deployed at {lend.address}")
