from scripts import utils, lend, agreement, simple_collectible
from web3 import Web3
from brownie import ZERO_ADDRESS, reverts
import time


def test_can_make_agreeement():
    """Test for making a new agreement"""

    owner = utils.get_account(1)
    # mint NFT
    simple_collectible.deploy()
    source_token_id = simple_collectible.create(owner)

    # make nft lendable
    lend_contract = lend.deploy()
    lend.approve(source_token_id, owner)
    token_id = lend.make_token_lendable(source_token_id, owner)
    lend.get_token_data(token_id)

    # make agreement
    agreement.deploy()
    agreement.approve(token_id, owner)
    agreement_id = agreement.make_agreement(token_id, 0.1, 2, 15, owner)

    assert agreement.get_nft(agreement_id) == (token_id, lend_contract.address)
    assert agreement.get_params(agreement_id) == (
        Web3.toWei(0.1, "ether"),
        2,
        0,
        15,
        False,
    )
    return agreement_id, lend_contract


def test_can_borrow():
    """Test to borrow"""
    owner = utils.get_account(1)
    borrower = utils.get_account(2)
    agreement_id, lend_contract = test_can_make_agreeement()
    params_before = agreement.get_params(agreement_id)

    owner_balance_before = owner.balance()
    borrower_balance_before = borrower.balance()

    # borrow and get data
    agreement.borrow(agreement_id, borrower)
    params_after = agreement.get_params(agreement_id)
    nft = agreement.get_nft(agreement_id)

    # check borrower address
    assert lend_contract.borrowedBy(nft[0]) == borrower.address

    # check balances
    assert borrower_balance_before - borrower.balance() == params_after[0]
    assert owner.balance() - owner_balance_before == params_after[0]

    assert params_after[3] > params_before[3]
    assert params_after[2] == params_after[1] + params_after[3] - params_before[3]
    assert params_after[4]

    return agreement_id, lend_contract


def test_can_pay_rent():
    """Test to pay rent"""
    owner = utils.get_account(1)
    borrower = utils.get_account(2)
    agreement_id, lend_contract = test_can_borrow()
    params_before = agreement.get_params(agreement_id)
    owner_balance_before = owner.balance()
    borrower_balance_before = borrower.balance()
    agreement.pay_rent(agreement_id, borrower)
    params_after = agreement.get_params(agreement_id)
    assert params_after[2] - params_before[2] == params_before[1]
    assert borrower_balance_before - borrower.balance() == params_after[0]
    assert owner.balance() - owner_balance_before == params_after[0]
    return agreement_id, lend_contract


def test_can_return_borrowed():
    """Test to return borrowed nft"""
    borrower = utils.get_account(2)
    agreement_id, lend_contract = test_can_borrow()

    nft = agreement.get_nft(agreement_id)
    params = agreement.get_params(agreement_id)
    time.sleep(params[1] + 1)

    agreement.return_borrowed(agreement_id, borrower)

    assert lend_contract.borrowedBy(nft[0]) == ZERO_ADDRESS
    assert agreement.get_nft(agreement_id)[1] == ZERO_ADDRESS
