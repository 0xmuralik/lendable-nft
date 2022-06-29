from brownie import accounts, network, config, Contract

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def get_account(index=None, id=None):
    """Fetch account"""
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {}


def get_contract(contract_name):
    """Deploys if local env and then gets the address of the contract"""
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) == 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type.name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    """Deploy mock contracts"""
    print("Deploying mocks...")
    # account = get_account()
    # link_contract = LinkToken.deploy({"from": account})
    # VRFCoordinatorV2Mock.deploy(1000, 1000000, {"from": account})
    print("Mocks deployed")
