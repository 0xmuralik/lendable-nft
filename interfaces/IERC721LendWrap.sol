// SPDX-License-Identifier: UNLICENSED

pragma solidity >0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import "./IERC721Lend.sol";

interface IERC721LendWrap is IERC721Lend, IERC721Receiver {
    function callOnNFT(uint256 tokenId, bytes memory signature)
        external
        returns (bool, bytes memory);
}
