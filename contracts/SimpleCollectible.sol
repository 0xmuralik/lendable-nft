// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SimpleCollectible is ERC721URIStorage, Ownable {
    uint256 public tokenCounter;
    mapping(uint256 => uint256) public powers;

    constructor() ERC721("Phoenix", "PHX") {
        tokenCounter = 0;
    }

    function setPower(uint256 tokenId, uint256 power) public {
        require(ownerOf(tokenId) == msg.sender);
        powers[tokenId] = power;
    }

    function incrementPower(uint256 tokenId) public {
        require(ownerOf(tokenId) == msg.sender);
        powers[tokenId] = powers[tokenId] + 1;
    }

    function createCollectible(string memory _tokenURI)
        public
        returns (uint256)
    {
        uint256 tokenId = tokenCounter;
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, _tokenURI);
        tokenCounter = tokenCounter + 1;
        return tokenId;
    }
}
