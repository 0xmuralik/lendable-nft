from brownie import network
import pytest
from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.simple_collectible import deploy, create, set_power


def test_can_deploy():
    """Unit test for deploy"""
    # if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    #     pytest.skip()
    simple_collectible = deploy()
    assert simple_collectible.address


def test_can_create():
    """Unit test for creating NFT"""
    # if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    #     pytest.skip()
    simple_collectible = deploy()
    create(get_account())
    assert simple_collectible.ownerOf(0) == get_account()


def test_can_set_power():
    """ "Unit test for setting power"""
    # if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    #     pytest.skip()
    simple_collectible = deploy()
    create(get_account())
    assert simple_collectible.ownerOf(0) == get_account()
    set_power(0, 100)
    assert simple_collectible.powers(0) == 100
