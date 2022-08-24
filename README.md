# lendable-nft

### Deploy Contracts

    nft=SimpleCollectible.deploy({"from":accounts[0]})
    lend=Lend.deploy("Lend","LEND",{"from":accounts[0]})
    agreement=Agreement.deploy({"from":accounts[0]})

### Create NFT

    create_tx=nft.createCollectible("",{"from":accounts[1]})
    source_id=create_tx.return_value

### Set Approval for NFT

    approve_tx=nft.approve(lend.address,source_id,{"from":accounts[1]})

### Make NFT lendable

    make_lendable_tx=lend.makeLendable(nft.address,source_id,{"from":accounts[1]})
    token_id=make_lendable_tx.return_value

### Set Approval for lendable NFT

    approve_lend_tx=lend.approveLend(agreement.address,token_id,{"from":accounts[1]})

### Create new agreement

     make_agreement_tx=agreement.makeAgreement(token_id,lend.address,0.1,10,30,14,{"from":accounts[1]})
     agreement_id=make_agreement_tx.return_value

### Borrow NFT through agreement

    borrow_tx=agreement.borrow(agreement_id,{"from":accounts[2]})

### Pay rent for NFT

    pay_rent_tx=agreement.payRent(agreement_id,{"from":accounts[2],"value":0.1})

### Return Borrowed NFT

    return_borrow_tx=agreement.returnBorrowed(agreement_id,{"from":accounts[1]})

### Release NFT from lend (unwrap)

    release_nft_tx=lend.releaseNFT(token_id,{"from":accounts[1]})
