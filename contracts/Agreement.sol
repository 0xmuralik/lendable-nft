// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "../interfaces/IERC721Lend.sol";

contract Agreement {
    struct NFT {
        uint256 id;
        address contractAddress;
    }
    struct PARAMS {
        uint256 rent;
        uint256 interval;
        uint256 paidUpTo;
        uint256 expiry;
        bool borrowed;
    }
    mapping(uint256 => NFT) public agreementToNFT;
    mapping(uint256 => PARAMS) public agreementToParams;
    uint256 public counter;

    function makeAgreement(
        uint256 nftId,
        address contractAddress,
        uint256 rent,
        uint256 intervalInDays,
        uint256 validityInDays
    ) public returns (uint256) {
        require(
            IERC721(contractAddress).supportsInterface(
                type(IERC721Lend).interfaceId
            )
        );
        require(msg.sender == IERC721(contractAddress).ownerOf(nftId));
        require(IERC721Lend(contractAddress).borrowedBy(nftId) == address(0));
        NFT memory nft = NFT(nftId, contractAddress);
        PARAMS memory params = PARAMS(
            rent,
            // intervalInDays * 1 days,
            intervalInDays,
            0,
            // validityInDays * 1 days,
            validityInDays,
            false
        );
        agreementToNFT[counter] = nft;
        agreementToParams[counter] = params;
        counter++;
        return counter - 1;
    }

    function borrow(uint256 agreementID) public payable {
        NFT memory nft = agreementToNFT[agreementID];
        PARAMS memory params = agreementToParams[agreementID];
        require(!params.borrowed);
        require(msg.value >= params.rent);
        IERC721Lend(nft.contractAddress).borrow(nft.id, msg.sender);
        payable(IERC721(nft.contractAddress).ownerOf(nft.id)).transfer(
            params.rent
        );
        params.borrowed = true;
        params.expiry = params.expiry + block.timestamp;
        params.paidUpTo = params.interval + block.timestamp;
        agreementToParams[agreementID] = params;
    }

    function payRent(uint256 agreementID) public payable {
        NFT memory nft = agreementToNFT[agreementID];
        require(
            msg.sender == IERC721Lend(nft.contractAddress).borrowedBy(nft.id)
        );
        PARAMS memory params = agreementToParams[agreementID];
        require(
            params.borrowed && params.expiry > params.paidUpTo + params.interval
        );
        require(msg.value >= params.rent);
        payable(IERC721(nft.contractAddress).ownerOf(nft.id)).transfer(
            params.rent
        );
        params.paidUpTo = params.paidUpTo + params.interval;
        agreementToParams[agreementID] = params;
    }

    function returnBorrowed(uint256 agreementID) public payable {
        NFT memory nft = agreementToNFT[agreementID];
        PARAMS memory params = agreementToParams[agreementID];
        require(params.borrowed && params.paidUpTo < block.timestamp);
        require(
            msg.sender == IERC721(nft.contractAddress).ownerOf(nft.id) ||
                msg.sender ==
                IERC721Lend(nft.contractAddress).borrowedBy(nft.id)
        );
        IERC721Lend(nft.contractAddress).returnBorrowed(nft.id);
        delete agreementToNFT[agreementID];
        delete agreementToParams[agreementID];
    }
}
