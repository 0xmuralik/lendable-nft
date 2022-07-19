// SPDX-License-Identifier: UNLICENSED

pragma solidity >0.8.0;

interface IERC721Lend {
    function borrow(uint256 tokenId, address borrower) external;

    function returnBorrowed(uint256 tokenId) external;

    function borrowedBy(uint256 tokenId) external returns (address);
}