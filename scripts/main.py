from scripts import simple_collectible
from scripts import lend


def main():
    """Script to deploy and interact NFT and lend contracts"""
    simple_collectible.deploy()
    source_token_id = simple_collectible.create()
    lend.deploy()
    lend.approve(source_token_id)
    token_id = lend.make_token_lendable(source_token_id)
    lend.get_token_data(token_id)
    lend.borrow(token_id)
    lend.get_token_data(token_id)
    result = lend.call_on_nft(token_id)
    print(f"RESULT {result}")
    lend.return_borrowed(token_id)
    lend.release_nft(token_id)
