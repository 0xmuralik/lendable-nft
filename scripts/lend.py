from brownie import Lend, SimpleCollectible
from scripts.utils import get_account, encode_function_signature


def main():
    """Entry"""


def deploy():
    """Deploy Lending contract"""
    account = get_account()
    lend = Lend.deploy({"from": account})
    print(f"Contract deployed at {lend.address}")


def approve(source_token_id):
    """Approve lend contract for simple collectible"""
    account = get_account()
    simple_collectible = SimpleCollectible[-1]
    lend = Lend[-1]
    approve_tx = simple_collectible.approve(
        lend.address, source_token_id, {"from": account}
    )
    approve_tx.wait(1)
    # use getApproved(tokenId) to test
    print(f"Token {source_token_id} approved for {lend.address}")


def make_token_lendable(source_token_id):
    """Make NFT Lendable"""
    account = get_account()
    lend = Lend[-1]
    make_lendable_tx = lend.makeLendable(
        SimpleCollectible[-1].address, source_token_id, {"from": account}
    )
    make_lendable_tx.wait(1)
    print(
        f"Token {source_token_id} made lendable. New token id is {lend.tokenCounter()-1} with owner as {account.address}"
    )


def borrow(token_id):
    """Borrow NFT"""
    account = get_account(1)
    lend = Lend[-1]
    borrow_tx = lend.borrow(token_id, {"from": account})
    borrow_tx.wait(1)
    print(f"Token {token_id} borrowed by {account.address}")


def call_on_nft(token_id):
    """call function on NFT source contract"""
    account = get_account(1)
    lend = Lend[-1]
    # set power
    signature = encode_function_signature(
        "setPower(uint256 tokenId, uint256 power)", 0, 100
    )
    call_tx = lend.callOnNFT(token_id, signature, {"from": account})
    call_tx.wait(1)


def return_borrowed(token_id):
    """return borrowed NFT"""
    account = get_account(1)
    lend = Lend[-1]
    return_borrowed_tx = lend.returnBorrowed(token_id, {"from": account})
    return_borrowed_tx.wait(1)


def release_nft(token_id):
    """return nft to original owner"""
    account = get_account()
    lend = Lend[-1]
    release_nft_tx = lend.releaseNFT(token_id, {"from": account})
    release_nft_tx.wait(1)
