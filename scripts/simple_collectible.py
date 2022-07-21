from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, OPENSEA_URL
from brownie import SimpleCollectible, network


SAMPLE_TOKEN_URI = "https://bafybeifql3m2pnx6tfbiemynmpd5c7uwxfed4f4krhkn7qll4gyz3voub4.ipfs.dweb.link/2104"
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


# def main():
#     """Entry"""
#     deploy()
#     create()
#     set_power(0, 100)


def deploy():
    """Deploy contract"""
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    print(f"Contract deployed at {simple_collectible.address}")
    return simple_collectible


def create(account):
    """Create NFT"""
    simple_collectible = SimpleCollectible[-1]
    create_tx = simple_collectible.createCollectible(
        SAMPLE_TOKEN_URI, {"from": account}
    )
    create_tx.wait(1)
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print(
            f"You can view your nft at {OPENSEA_URL.format(simple_collectible.address,create_tx.return_value)}"
        )
    else:
        print("NFT is deployed")
    return create_tx.return_value


def set_power(token_id, power):
    """Set power to NFT"""
    account = get_account()
    simple_collectible = SimpleCollectible[-1]
    set_power_tx = simple_collectible.setPower(token_id, power, {"from": account})
    set_power_tx.wait(1)
    return simple_collectible.powers(token_id)
