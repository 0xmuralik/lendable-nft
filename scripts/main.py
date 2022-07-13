from scripts import simple_collectible, lend, utils


def main():
    """Script to deploy and interact NFT and lend contracts"""
    simple_collectible.deploy()
    source_token_id = simple_collectible.create()
    lend.deploy()
    lend.approve(source_token_id, utils.get_account())
    token_id = lend.make_token_lendable(source_token_id, utils.get_account())
    lend.get_token_data(token_id)
    source_token_id = simple_collectible.create()
    lend.owner_transfer(token_id, utils.get_account(), utils.get_account(1))
    lend.borrow(token_id, utils.get_account(2))
    lend.get_token_data(token_id)
    result = lend.call_on_nft_powers(token_id, utils.get_account(2))
    print(f"RESULT {result}")
    lend.return_borrowed(token_id, utils.get_account(2))
    lend.release_nft(token_id, utils.get_account(1))
