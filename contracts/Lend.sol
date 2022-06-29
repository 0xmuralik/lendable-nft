// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract Lend is IERC721Receiver {
    uint256 tokenCounter;
    mapping(uint256 => address) public tokenToLender;
    mapping(uint256 => address) public tokenToBorrower;
    mapping(uint256 => address) public tokenToContract;
    mapping(uint256 => uint256) public tokenIdToSourceTokenId;

    function makeLendable(address NFTContract, uint256 sourceTokenId) public {
        require(isContract(NFTContract));
        ERC721(NFTContract).safeTransferFrom(
            msg.sender,
            address(this),
            sourceTokenId
        );
        tokenIdToSourceTokenId[tokenCounter] = sourceTokenId;
        tokenToContract[tokenCounter] = NFTContract;
        tokenToLender[tokenCounter] = msg.sender;
        tokenCounter = tokenCounter + 1;
    }

    function backToOwner(uint256 tokenId) public {
        ERC721(tokenToContract[tokenId]).safeTransferFrom(
            address(this),
            msg.sender,
            tokenIdToSourceTokenId[tokenId]
        );
        tokenToLender[tokenId] = address(0);
    }

    function borrow(uint256 tokenID) public {
        tokenToBorrower[tokenID] = msg.sender;
    }

    function returnBorrowed(uint256 tokenId) public {
        require(tokenToBorrower[tokenId] == msg.sender);
        tokenToBorrower[tokenId] = address(0);
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
        return tokenToContract[tokenId].call(signature);
    }

    function isContract(address addr) public view returns (bool) {
        uint256 size;
        assembly {
            size := extcodesize(addr)
        }
        return size > 0;
    }
}
