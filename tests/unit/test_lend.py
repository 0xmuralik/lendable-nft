from scripts import simple_collectible, lend, utils
from brownie import ZERO_ADDRESS, reverts, SimpleCollectible, Contract


def test_can_make_lendable():
    """Test for making a token lendable"""
    nft_contract = simple_collectible.deploy()
    lend_contract = lend.deploy()
    source_token_id = simple_collectible.create(utils.get_account())
    lend.approve(source_token_id, utils.get_account())
    lended_token_id = lend.make_token_lendable(source_token_id, utils.get_account())
    assert lend_contract.ownerOf(lended_token_id) == utils.get_account()
    assert nft_contract.ownerOf(source_token_id) == lend_contract.address
    return lend_contract, lended_token_id


def test_can_borrow():
    """Test to borrow a lendable nft"""
    (
        lend_contract,
        lended_token_id,
    ) = test_can_make_lendable()
    lend.borrow(lended_token_id, utils.get_account(1))
    assert lend_contract.borrowedBy(lended_token_id) == utils.get_account(1)
    return lend_contract, lended_token_id


def test_can_call_on_borrowed():
    """Test to call function on borrowed nft"""
    (
        lend_contract,
        lended_token_id,
    ) = test_can_borrow()
    nft = lend_contract.getSourceNFT(lended_token_id)
    signature = utils.encode_function_signature(
        "setPower(uint256,uint256)",
        nft[0],
        100,
    )
    result = lend.call_on_nft(lended_token_id, signature, utils.get_account(1))
    assert result is not None
    signature = utils.encode_function_signature("powers(uint256)", nft[0])
    result = lend.call_on_nft(lended_token_id, signature, utils.get_account(1))
    assert utils.decode_to_int(result[1:]) == 100
    return lend_contract, lended_token_id


def test_can_return():
    """Test to return borrowed"""
    (
        lend_contract,
        lended_token_id,
    ) = test_can_borrow()
    lend.return_borrowed(lended_token_id, utils.get_account(1))
    assert lend_contract.borrowedBy(lended_token_id) == ZERO_ADDRESS
    return lend_contract, lended_token_id


def test_can_release():
    """Test to release a lendable nft"""
    (
        lend_contract,
        lended_token_id,
    ) = test_can_return()
    nft = lend_contract.getSourceNFT(lended_token_id)

    lend.release_nft(lended_token_id, utils.get_account())
    with reverts("ERC721: owner query for nonexistent token"):
        lend_contract.ownerOf(lended_token_id)
    simple_collectible_contract = Contract.from_abi(
        "SimpleCollectible", nft[1], SimpleCollectible.abi
    )
    assert simple_collectible_contract.ownerOf(nft[0]) == utils.get_account()
