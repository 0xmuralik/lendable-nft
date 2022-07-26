// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/IERC721Metadata.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "../interfaces/IERC721Lend.sol";

contract Lend is IERC721Receiver, ERC721URIStorage, IERC721Lend {
    uint256 public tokenCounter;
    mapping(uint256 => address) public tokenToBorrower;
    mapping(uint256 => address) public tokenToContract;
    mapping(uint256 => uint256) public tokenIdToSourceTokenId;

    constructor(string memory name_, string memory symbol_)
        ERC721(name_, symbol_)
    {}

    function makeLendable(address nftContract, uint256 sourceTokenId)
        public
        returns (uint256)
    {
        require(
            IERC721(nftContract).ownerOf(sourceTokenId) == msg.sender &&
                isContract(nftContract)
        );
        IERC721(nftContract).safeTransferFrom(
            msg.sender,
            address(this),
            sourceTokenId
        );
        // mint new token as owner as msg.sender
        _safeMint(msg.sender, tokenCounter);
        if (
            IERC721(nftContract).supportsInterface(
                type(IERC721Metadata).interfaceId
            )
        ) {
            _setTokenURI(
                tokenCounter,
                IERC721Metadata(nftContract).tokenURI(sourceTokenId)
            );
        }
        tokenIdToSourceTokenId[tokenCounter] = sourceTokenId;
        tokenToContract[tokenCounter] = nftContract;
        tokenCounter = tokenCounter + 1;
        return tokenCounter - 1;
    }

    function releaseNFT(uint256 tokenId) public {
        require(
            ownerOf(tokenId) == msg.sender &&
                tokenToBorrower[tokenId] == address(0)
        );
        IERC721(tokenToContract[tokenId]).safeTransferFrom(
            address(this),
            msg.sender,
            tokenIdToSourceTokenId[tokenId]
        );
        _burn(tokenId);
    }

    function borrow(uint256 tokenId, address borrower) public {
        require(_exists(tokenId));
        require(msg.sender == borrower || msg.sender == getApproved(tokenId));
        require(tokenToBorrower[tokenId] == address(0));
        tokenToBorrower[tokenId] = borrower;
    }

    function returnBorrowed(uint256 tokenId) public {
        // BUG: owner can change approved to return borrowed NFT anytime
        require(
            tokenToBorrower[tokenId] == msg.sender ||
                msg.sender == getApproved(tokenId)
        );
        tokenToBorrower[tokenId] = address(0);
    }

    function borrowedBy(uint256 tokenId) public view returns (address) {
        return tokenToBorrower[tokenId];
    }

    function onERC721Received(
        address,
        address,
        uint256,
        bytes calldata
    ) public pure override returns (bytes4) {
        return this.onERC721Received.selector;
    }

    function callOnNFT(uint256 tokenId, bytes memory signature)
        public
        returns (bool, bytes memory)
    {
        if (tokenToBorrower[tokenId] != address(0)) {
            require(msg.sender == tokenToBorrower[tokenId]);
        } else {
            require(msg.sender == ownerOf(tokenId));
        }
        (bool success, bytes memory result) = tokenToContract[tokenId].call(
            signature
        );
        require(success);
        return (success, result);
    }

    function isContract(address addr) public view returns (bool) {
        uint256 size;
        assembly {
            size := extcodesize(addr)
        }
        return size > 0;
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual
        override
        returns (bool)
    {
        return
            interfaceId == type(IERC721Lend).interfaceId ||
            interfaceId == type(IERC721Receiver).interfaceId ||
            super.supportsInterface(interfaceId);
    }
}
