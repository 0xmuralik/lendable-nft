from brownie import Lend, SimpleCollectible
from scripts.utils import get_account, encode_function_signature, decode_to_int


# def main():
#     """Entry"""


def deploy():
    """Deploy Lending contract"""
    account = get_account()
    lend = Lend.deploy("Lending", "LEND", {"from": account})
    print(f"Contract deployed at {lend.address}")
    return lend


def approve(source_token_id, account):
    """Approve lend contract for simple collectible"""
    simple_collectible = SimpleCollectible[-1]
    lend = Lend[-1]
    approve_tx = simple_collectible.approve(
        lend.address, source_token_id, {"from": account}
    )
    approve_tx.wait(1)
    # use getApproved(tokenId) to test
    print(
        f"Token {source_token_id} approved for {simple_collectible.getApproved(source_token_id)}"
    )


def make_token_lendable(source_token_id, account):
    """Make NFT Lendable"""
    lend = Lend[-1]
    make_lendable_tx = lend.makeLendable(
        SimpleCollectible[-1].address, source_token_id, {"from": account}
    )
    make_lendable_tx.wait(1)
    print(
        f"Token {source_token_id} made lendable. New token id is {make_lendable_tx.return_value} with owner as {account.address}"
    )
    return make_lendable_tx.return_value


def borrow(token_id, account):
    """Borrow NFT"""
    lend = Lend[-1]
    borrow_tx = lend.borrow(token_id, account, {"from": account})
    borrow_tx.wait(1)
    print(f"Token {token_id} borrowed by {account.address}")


def call_on_nft_powers(token_id, account):
    """call powers function on NFT source contract"""
    lend = Lend[-1]
    # set power
    signature = encode_function_signature("setPower(uint256,uint256)", 0, 100)
    call_tx = lend.callOnNFT(token_id, signature, {"from": account})
    call_tx.wait(1)
    success, result = call_tx.return_value
    if not success:
        print("Call on nft source failed!!!!!!!!!!!!!!")

    # get power
    signature = encode_function_signature("powers(uint256)", 0)
    call_tx = lend.callOnNFT(token_id, signature, {"from": account})
    call_tx.wait(1)
    success, result = call_tx.return_value
    if not success:
        print("Call on nft source failed!!!!!!!!!!!!!!")
    return decode_to_int(result[1:])
    # return result


def call_on_nft(token_id, signature, account):
    """call function on NFT source contract"""
    lend = Lend[-1]
    call_tx = lend.callOnNFT(token_id, signature, {"from": account})
    call_tx.wait(1)
    success, result = call_tx.return_value
    if not success:
        print("Call on nft source failed!!!!!!!!!!!!!!")
        return None
    return result


def return_borrowed(token_id, account):
    """return borrowed NFT"""
    lend = Lend[-1]
    return_borrowed_tx = lend.returnBorrowed(token_id, {"from": account})
    return_borrowed_tx.wait(1)


def release_nft(token_id, account):
    """return nft to original owner"""
    lend = Lend[-1]
    release_nft_tx = lend.releaseNFT(token_id, {"from": account})
    release_nft_tx.wait(1)


def owner_transfer(token_id, from_acc, to_acc):
    """Transfer ownership of lended token"""
    lend = Lend[-1]
    transfer_tx = lend.safeTransferFrom(from_acc, to_acc, token_id)
    transfer_tx.wait(1)


def get_token_data(token_id):
    """Prints all the data regarding that token"""
    lend = Lend[-1]
    print(f"Token ID: {token_id}")
    print(f"Token source id: {lend.tokenIdToSourceTokenId(token_id)}")
    print(f"Token source contract: {lend.tokenToContract(token_id)}")
    print(f"Token owner: {lend.ownerOf(token_id)}")
    print(f"Token borowwer: {lend.tokenToBorrower(token_id)}")
