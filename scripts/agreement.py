from brownie import Agreement, Lend
from web3 import Web3
from scripts.utils import get_account


def deploy():
    """Deploying agreement contract"""
    account = get_account()
    agreement = Agreement.deploy({"from": account})
    print(f"Agreement contract deployed at {agreement.address}")
    return agreement


def approve_lend(token_id, account):
    """Approve agreement contract to use lendable NFT"""
    lend = Lend[-1]
    agreement = Agreement[-1]
    approve_tx = lend.approveLend(agreement.address, token_id, {"from": account})
    approve_tx.wait(1)
    print(f"Token {token_id} approved for {lend.getLendApproved(token_id)}")


def make_agreement(token_id, rent_in_eth, interval, validity, notice_period, account):
    """make a new agreement for token lending"""
    agreement = Agreement[-1]
    rent = Web3.toWei(rent_in_eth, "ether")
    make_agreement_tx = agreement.makeAgreement(
        token_id,
        Lend[-1].address,
        rent,
        interval,
        validity,
        notice_period,
        {"from": account},
    )
    make_agreement_tx.wait(1)
    agreement_id = make_agreement_tx.return_value
    print(f"New agreement id {agreement_id}")
    print(
        f"Agreement for nft {agreement.agreementToNFT(agreement_id)} with params {agreement.agreementToParams(agreement_id)}"
    )
    return agreement_id


def borrow(agreement_id, account):
    """Borrow lendable NFT from agreement"""
    agreement = Agreement[-1]
    rent = agreement.agreementToParams(agreement_id)[0]
    borrow_tx = agreement.borrow(agreement_id, {"from": account, "value": rent})
    borrow_tx.wait(1)
    print(
        f"Nft {agreement.agreementToNFT(agreement_id)} borrowed by {account.address} with params {agreement.agreementToParams(agreement_id)}"
    )


def pay_rent(agreement_id, account):
    """Pay rent for borrowed NFT"""
    agreement = Agreement[-1]
    rent = agreement.agreementToParams(agreement_id)[0]
    pay_rent_tx = agreement.payRent(agreement_id, {"from": account, "value": rent})
    pay_rent_tx.wait(1)
    print(
        f"Rent for nft {agreement.agreementToNFT(agreement_id)} paid. Upadted params to {agreement.agreementToParams(agreement_id)}"
    )


def return_borrowed(agreement_id, account):
    """return borrowedNFT"""
    agreement = Agreement[-1]
    token_id = agreement.agreementToNFT(agreement_id)[0]
    return_borrowed_tx = agreement.returnBorrowed(agreement_id, {"from": account})
    return_borrowed_tx.wait(1)
    lend = Lend[-1]
    print(f"Returned borrowed NFT. Current borrower {lend.borrowedBy(token_id)}")


def get_params(agreement_id):
    """Get params"""
    agreement = Agreement[-1]
    return agreement.agreementToParams(agreement_id)


def get_nft(agreement_id):
    """Get nft"""
    agreement = Agreement[-1]
    return agreement.agreementToNFT(agreement_id)
