// SPDX-License-Identifier: UNLICENSED

pragma solidity >0.8.0;

interface IERC721Lend {
    function borrow(uint256 tokenId, address borrower) external;

    function returnBorrowed(uint256 tokenId) external;

    function borrowedBy(uint256 tokenId) external returns (address);

    function approveLend(address _approved, uint256 _tokenId) external;

    function setLendApprovalForAll(address _operator, bool _approved) external;

    function getLendApproved(uint256 _tokenId) external view returns (address);

    function isLendApprovedForAll(address _owner, address _operator)
        external
        view
        returns (bool);
}
