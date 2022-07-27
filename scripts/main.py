from scripts import simple_collectible, lend, agreement, utils
import time


def main():
    """Script to deploy and interact NFT and lend contracts"""

    # assign accounts
    owner = utils.get_account(1)
    borrower = utils.get_account(2)

    # mint NFT
    simple_collectible.deploy()
    source_token_id = simple_collectible.create(owner)

    # make nft lendable
    lend.deploy()
    lend.approve(source_token_id, owner)
    token_id = lend.make_token_lendable(source_token_id, owner)
    lend.get_token_data(token_id)

    # lend.owner_transfer(token_id, utils.get_account(), utils.get_account(1))

    # make agreement
    agreement.deploy()
    agreement.approve_lend(token_id, owner)
    agreement_id = agreement.make_agreement(token_id, 0.1, 2, 30, 14, owner)

    # borrow from agreement
    agreement.borrow(agreement_id, borrower)
    lend.get_token_data(token_id)

    # call on borrowed nft
    result = lend.call_on_nft_powers(token_id, borrower)
    print(f"RESULT {result}")

    # pay rent
    agreement.pay_rent(agreement_id, borrower)
    time.sleep(4)

    # return borrowed from agreement
    agreement.return_borrowed(agreement_id, owner)

    # release NFT
    lend.release_nft(token_id, owner)
