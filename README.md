# Decode_solidity_function
从静态solidity合约中提取所有的方法,现在一半都是通过AST工具去提取合约中具有的方法，现在提供一种从静态文本去识别合约方法的脚本
例子：
'''
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

/**
 * @dev Contract module that helps prevent reentrant calls to a function.
 *
 * Inheriting from `ReentrancyGuard` will make the {nonReentrant} modifier
 * available, which can be applied to functions to make sure there are no nested
 * (reentrant) calls to them.
 *
 * Note that because there is a single `nonReentrant` guard, functions marked as
 * `nonReentrant` may not call one another. This can be worked around by making
 * those functions `private`, and then adding `external` `nonReentrant` entry
 * points to them.
 *
 * TIP: If you would like to learn more about reentrancy and alternative ways
 * to protect against it, check out our blog post
 * https://blog.openzeppelin.com/reentrancy-after-istanbul/[Reentrancy After Istanbul].
 */
abstract contract ReentrancyGuard {
    // Booleans are more expensive than uint256 or any type that takes up a full
    // word because each write operation emits an extra SLOAD to first read the
    // slot's contents, replace the bits taken up by the boolean, and then write
    // back. This is the compiler's defense against contract upgrades and
    // pointer aliasing, and it cannot be disabled.

    // The values being non-zero value makes deployment a bit more expensive,
    // but in exchange the refund on every call to nonReentrant will be lower in
    // amount. Since refunds are capped to a percentage of the total
    // transaction's gas, it is best to keep them low in cases like this one, to
    // increase the likelihood of the full refund coming into effect.
    uint256 private constant _NOT_ENTERED = 1;
    uint256 private constant _ENTERED = 2;

    uint256 private _status;

    constructor() {
        _status = _NOT_ENTERED;
    }

    /**
     * @dev Prevents a contract from calling itself, directly or indirectly.
     * Calling a `nonReentrant` function from another `nonReentrant`
     * function is not supported. It is possible to prevent this from happening
     * by making the `nonReentrant` function external, and make it call a
     * `private` function that does the actual work.
     */
    modifier nonReentrant() {
        // On the first call to nonReentrant, _notEntered will be true
        require(_status != _ENTERED, "ReentrancyGuard: reentrant call");

        // Any calls to nonReentrant after this point will fail
        _status = _ENTERED;

        _;

        // By storing the original value once again, a refund is triggered (see
        // https://eips.ethereum.org/EIPS/eip-2200)
        _status = _NOT_ENTERED;
    }
}
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

/*
 * @dev Provides information about the current execution context, including the
 * sender of the transaction and its data. While these are generally available
 * via msg.sender and msg.data, they should not be accessed in such a direct
 * manner, since when dealing with meta-transactions the account sending and
 * paying for execution may not be the actual sender (as far as an application
 * is concerned).
 *
 * This contract is only required for intermediate, library-like contracts.
 */
abstract contract Context {
    function _msgSender() internal view virtual returns (address) {
        return msg.sender;
    }

    function _msgData() internal view virtual returns (bytes calldata) {
        return msg.data;
    }
}
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

/**
 * @dev These functions deal with verification of Merkle Trees proofs.
 *
 * The proofs can be generated using the JavaScript library
 * https://github.com/miguelmota/merkletreejs[merkletreejs].
 * Note: the hashing algorithm should be keccak256 and pair sorting should be enabled.
 *
 * See `test/utils/cryptography/MerkleProof.test.js` for some examples.
 */
library MerkleProof {
    /**
     * @dev Returns true if a `leaf` can be proved to be a part of a Merkle tree
     * defined by `root`. For this, a `proof` must be provided, containing
     * sibling hashes on the branch from the leaf to the root of the tree. Each
     * pair of leaves and each pair of pre-images are assumed to be sorted.
     */
    function verify(
        bytes32[] memory proof,
        bytes32 root,
        bytes32 leaf
    ) internal pure returns (bool) {
        bytes32 computedHash = leaf;

        for (uint256 i = 0; i < proof.length; i++) {
            bytes32 proofElement = proof[i];

            if (computedHash <= proofElement) {
                // Hash(current computed hash + current element of the proof)
                computedHash = keccak256(abi.encodePacked(computedHash, proofElement));
            } else {
                // Hash(current element of the proof + current computed hash)
                computedHash = keccak256(abi.encodePacked(proofElement, computedHash));
            }
        }

        // Check if the computed hash (root) is equal to the provided root
        return computedHash == root;
    }
}
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

// CAUTION
// This version of SafeMath should only be used with Solidity 0.8 or later,
// because it relies on the compiler's built in overflow checks.

/**
 * @dev Wrappers over Solidity's arithmetic operations.
 *
 * NOTE: `SafeMath` is no longer needed starting with Solidity 0.8. The compiler
 * now has built in overflow checking.
 */
library SafeMath {
    /**
     * @dev Returns the addition of two unsigned integers, with an overflow flag.
     *
     * _Available since v3.4._
     */
    function tryAdd(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        unchecked {
            uint256 c = a + b;
            if (c < a) return (false, 0);
            return (true, c);
        }
    }

    /**
     * @dev Returns the substraction of two unsigned integers, with an overflow flag.
     *
     * _Available since v3.4._
     */
    function trySub(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        unchecked {
            if (b > a) return (false, 0);
            return (true, a - b);
        }
    }

    /**
     * @dev Returns the multiplication of two unsigned integers, with an overflow flag.
     *
     * _Available since v3.4._
     */
    function tryMul(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        unchecked {
            // Gas optimization: this is cheaper than requiring 'a' not being zero, but the
            // benefit is lost if 'b' is also tested.
            // See: https://github.com/OpenZeppelin/openzeppelin-contracts/pull/522
            if (a == 0) return (true, 0);
            uint256 c = a * b;
            if (c / a != b) return (false, 0);
            return (true, c);
        }
    }

    /**
     * @dev Returns the division of two unsigned integers, with a division by zero flag.
     *
     * _Available since v3.4._
     */
    function tryDiv(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        unchecked {
            if (b == 0) return (false, 0);
            return (true, a / b);
        }
    }

    /**
     * @dev Returns the remainder of dividing two unsigned integers, with a division by zero flag.
     *
     * _Available since v3.4._
     */
    function tryMod(uint256 a, uint256 b) internal pure returns (bool, uint256) {
        unchecked {
            if (b == 0) return (false, 0);
            return (true, a % b);
        }
    }

    /**
     * @dev Returns the addition of two unsigned integers, reverting on
     * overflow.
     *
     * Counterpart to Solidity's `+` operator.
     *
     * Requirements:
     *
     * - Addition cannot overflow.
     */
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        return a + b;
    }

    /**
     * @dev Returns the subtraction of two unsigned integers, reverting on
     * overflow (when the result is negative).
     *
     * Counterpart to Solidity's `-` operator.
     *
     * Requirements:
     *
     * - Subtraction cannot overflow.
     */
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        return a - b;
    }

    /**
     * @dev Returns the multiplication of two unsigned integers, reverting on
     * overflow.
     *
     * Counterpart to Solidity's `*` operator.
     *
     * Requirements:
     *
     * - Multiplication cannot overflow.
     */
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        return a * b;
    }

    /**
     * @dev Returns the integer division of two unsigned integers, reverting on
     * division by zero. The result is rounded towards zero.
     *
     * Counterpart to Solidity's `/` operator.
     *
     * Requirements:
     *
     * - The divisor cannot be zero.
     */
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return a / b;
    }

    /**
     * @dev Returns the remainder of dividing two unsigned integers. (unsigned integer modulo),
     * reverting when dividing by zero.
     *
     * Counterpart to Solidity's `%` operator. This function uses a `revert`
     * opcode (which leaves remaining gas untouched) while Solidity uses an
     * invalid opcode to revert (consuming all remaining gas).
     *
     * Requirements:
     *
     * - The divisor cannot be zero.
     */
    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        return a % b;
    }

    /**
     * @dev Returns the subtraction of two unsigned integers, reverting with custom message on
     * overflow (when the result is negative).
     *
     * CAUTION: This function is deprecated because it requires allocating memory for the error
     * message unnecessarily. For custom revert reasons use {trySub}.
     *
     * Counterpart to Solidity's `-` operator.
     *
     * Requirements:
     *
     * - Subtraction cannot overflow.
     */
    function sub(
        uint256 a,
        uint256 b,
        string memory errorMessage
    ) internal pure returns (uint256) {
        unchecked {
            require(b <= a, errorMessage);
            return a - b;
        }
    }

    /**
     * @dev Returns the integer division of two unsigned integers, reverting with custom message on
     * division by zero. The result is rounded towards zero.
     *
     * Counterpart to Solidity's `/` operator. Note: this function uses a
     * `revert` opcode (which leaves remaining gas untouched) while Solidity
     * uses an invalid opcode to revert (consuming all remaining gas).
     *
     * Requirements:
     *
     * - The divisor cannot be zero.
     */
    function div(
        uint256 a,
        uint256 b,
        string memory errorMessage
    ) internal pure returns (uint256) {
        unchecked {
            require(b > 0, errorMessage);
            return a / b;
        }
    }

    /**
     * @dev Returns the remainder of dividing two unsigned integers. (unsigned integer modulo),
     * reverting with custom message when dividing by zero.
     *
     * CAUTION: This function is deprecated because it requires allocating memory for the error
     * message unnecessarily. For custom revert reasons use {tryMod}.
     *
     * Counterpart to Solidity's `%` operator. This function uses a `revert`
     * opcode (which leaves remaining gas untouched) while Solidity uses an
     * invalid opcode to revert (consuming all remaining gas).
     *
     * Requirements:
     *
     * - The divisor cannot be zero.
     */
    function mod(
        uint256 a,
        uint256 b,
        string memory errorMessage
    ) internal pure returns (uint256) {
        unchecked {
            require(b > 0, errorMessage);
            return a % b;
        }
    }
}
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

/**
 * @dev String operations.
 */
library Strings {
    bytes16 private constant _HEX_SYMBOLS = "0123456789abcdef";

    /**
     * @dev Converts a `uint256` to its ASCII `string` decimal representation.
     */
    function toString(uint256 value) internal pure returns (string memory) {
        // Inspired by OraclizeAPI's implementation - MIT licence
        // https://github.com/oraclize/ethereum-api/blob/b42146b063c7d6ee1358846c198246239e9360e8/oraclizeAPI_0.4.25.sol

        if (value == 0) {
            return "0";
        }
        uint256 temp = value;
        uint256 digits;
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }

    /**
     * @dev Converts a `uint256` to its ASCII `string` hexadecimal representation.
     */
    function toHexString(uint256 value) internal pure returns (string memory) {
        if (value == 0) {
            return "0x00";
        }
        uint256 temp = value;
        uint256 length = 0;
        while (temp != 0) {
            length++;
            temp >>= 8;
        }
        return toHexString(value, length);
    }

    /**
     * @dev Converts a `uint256` to its ASCII `string` hexadecimal representation with fixed length.
     */
    function toHexString(uint256 value, uint256 length) internal pure returns (string memory) {
        bytes memory buffer = new bytes(2 * length + 2);
        buffer[0] = "0";
        buffer[1] = "x";
        for (uint256 i = 2 * length + 1; i > 1; --i) {
            buffer[i] = _HEX_SYMBOLS[value & 0xf];
            value >>= 4;
        }
        require(value == 0, "Strings: hex length insufficient");
        return string(buffer);
    }
}
// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v5.0.0) (token/ERC721/IERC721.sol)

pragma solidity ^0.8.13;

import {IERC165} from "./utils/IERC165.sol";

/**
 * @dev Required interface of an ERC-721 compliant contract.
 */
interface IERC721 is IERC165 {
    /**
     * @dev Emitted when `tokenId` token is transferred from `from` to `to`.
     */
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);

    /**
     * @dev Emitted when `owner` enables `approved` to manage the `tokenId` token.
     */
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);

    /**
     * @dev Emitted when `owner` enables or disables (`approved`) `operator` to manage all of its assets.
     */
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);

    /**
     * @dev Returns the number of tokens in ``owner``'s account.
     */
    function balanceOf(address owner) external view returns (uint256 balance);

    /**
     * @dev Returns the owner of the `tokenId` token.
     *
     * Requirements:
     *
     * - `tokenId` must exist.
     */
    function ownerOf(uint256 tokenId) external view returns (address owner);

    /**
     * @dev Safely transfers `tokenId` token from `from` to `to`.
     *
     * Requirements:
     *
     * - `from` cannot be the zero address.
     * - `to` cannot be the zero address.
     * - `tokenId` token must exist and be owned by `from`.
     * - If the caller is not `from`, it must be approved to move this token by either {approve} or {setApprovalForAll}.
     * - If `to` refers to a smart contract, it must implement {IERC721Receiver-onERC721Received}, which is called upon
     *   a safe transfer.
     *
     * Emits a {Transfer} event.
     */
    function safeTransferFrom(address from, address to, uint256 tokenId, bytes calldata data) external;

    /**
     * @dev Safely transfers `tokenId` token from `from` to `to`, checking first that contract recipients
     * are aware of the ERC-721 protocol to prevent tokens from being forever locked.
     *
     * Requirements:
     *
     * - `from` cannot be the zero address.
     * - `to` cannot be the zero address.
     * - `tokenId` token must exist and be owned by `from`.
     * - If the caller is not `from`, it must have been allowed to move this token by either {approve} or
     *   {setApprovalForAll}.
     * - If `to` refers to a smart contract, it must implement {IERC721Receiver-onERC721Received}, which is called upon
     *   a safe transfer.
     *
     * Emits a {Transfer} event.
     */
    function safeTransferFrom(address from, address to, uint256 tokenId) external;

    /**
     * @dev Transfers `tokenId` token from `from` to `to`.
     *
     * WARNING: Note that the caller is responsible to confirm that the recipient is capable of receiving ERC-721
     * or else they may be permanently lost. Usage of {safeTransferFrom} prevents loss, though the caller must
     * understand this adds an external call which potentially creates a reentrancy vulnerability.
     *
     * Requirements:
     *
     * - `from` cannot be the zero address.
     * - `to` cannot be the zero address.
     * - `tokenId` token must be owned by `from`.
     * - If the caller is not `from`, it must be approved to move this token by either {approve} or {setApprovalForAll}.
     *
     * Emits a {Transfer} event.
     */
    function transferFrom(address from, address to, uint256 tokenId) external;

    /**
     * @dev Gives permission to `to` to transfer `tokenId` token to another account.
     * The approval is cleared when the token is transferred.
     *
     * Only a single account can be approved at a time, so approving the zero address clears previous approvals.
     *
     * Requirements:
     *
     * - The caller must own the token or be an approved operator.
     * - `tokenId` must exist.
     *
     * Emits an {Approval} event.
     */
    function approve(address to, uint256 tokenId) external;

    /**
     * @dev Approve or remove `operator` as an operator for the caller.
     * Operators can call {transferFrom} or {safeTransferFrom} for any token owned by the caller.
     *
     * Requirements:
     *
     * - The `operator` cannot be the address zero.
     *
     * Emits an {ApprovalForAll} event.
     */
    function setApprovalForAll(address operator, bool approved) external;

    /**
     * @dev Returns the account approved for `tokenId` token.
     *
     * Requirements:
     *
     * - `tokenId` must exist.
     */
    function getApproved(uint256 tokenId) external view returns (address operator);

    /**
     * @dev Returns if the `operator` is allowed to manage all of the assets of `owner`.
     *
     * See {setApprovalForAll}
     */
    function isApprovedForAll(address owner, address operator) external view returns (bool);
}// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {MRC721} from "./MRC721.sol";
import {IERC721Enumerable} from "./utils/IERC721Enumerable.sol";
import {IERC165} from "./utils/ERC165.sol";

abstract contract Micro3 is MRC721, IERC721Enumerable {
    mapping(address => mapping(uint256 => uint256))
        private _ownedTokens;
    mapping(uint256 => uint256) private _ownedTokensIndex;

    uint256[] private _allTokens;
    mapping(uint256 => uint256) private _allTokensIndex;

    /**
     * @dev An `owner`'s token query was out of bounds for `index`.
     *
     * NOTE: The owner being `address(0)` indicates a global out of bounds index.
     */
    error ERC721OutOfBoundsIndex(address owner, uint256 index);

    /**
     * @dev Batch mint is not allowed.
     */
    error ERC721EnumerableForbiddenBatchMint();

    /**
     * @dev See {IERC165-supportsInterface}.
     */
    function supportsInterface(
        bytes4 interfaceId
    ) public view virtual override(IERC165, MRC721) returns (bool) {
        return
            interfaceId == type(IERC721Enumerable).interfaceId ||
            super.supportsInterface(interfaceId);
    }

    /**
     * @dev See {IERC721Enumerable-tokenOfOwnerByIndex}.
     */
    function tokenOfOwnerByIndex(
        address owner,
        uint256 index
    ) public view virtual returns (uint256) {
        if (index >= balanceOf(owner)) {
            revert ERC721OutOfBoundsIndex(owner, index);
        }
        return _ownedTokens[owner][index];
    }

    /**
     * @dev See {IERC721Enumerable-totalSupply}.
     */
    function totalSupply() public view virtual returns (uint256) {
        return _allTokens.length;
    }

    /**
     * @dev See {IERC721Enumerable-tokenByIndex}.
     */
    function tokenByIndex(uint256 index) public view virtual returns (uint256) {
        if (index >= totalSupply()) {
            revert ERC721OutOfBoundsIndex(address(0), index);
        }
        return _allTokens[index];
    }

    /**
     * @dev See {ERC721-_update}.
     */
    function _update(
        address to,
        uint256 tokenId,
        address auth
    ) internal virtual override returns (address) {
        address previousOwner = super._update(to, tokenId, auth);

        if (previousOwner == address(0)) {
            _addTokenToAllTokensEnumeration(tokenId);
        } else if (previousOwner != to) {
            _removeTokenFromOwnerEnumeration(previousOwner, tokenId);
        }
        if (to == address(0)) {
            _removeTokenFromAllTokensEnumeration(tokenId);
        } else if (previousOwner != to) {
            _addTokenToOwnerEnumeration(to, tokenId);
        }

        return previousOwner;
    }

    /**
     * @dev Private function to add a token to this extension's ownership-tracking data structures.
     * @param to address representing the new owner of the given token ID
     * @param tokenId uint256 ID of the token to be added to the tokens list of the given address
     */
    function _addTokenToOwnerEnumeration(address to, uint256 tokenId) private {
        uint256 length = balanceOf(to) - 1;
        _ownedTokens[to][length] = tokenId;
        _ownedTokensIndex[tokenId] = length;
    }

    /**
     * @dev Private function to add a token to this extension's token tracking data structures.
     * @param tokenId uint256 ID of the token to be added to the tokens list
     */
    function _addTokenToAllTokensEnumeration(uint256 tokenId) private {
        _allTokensIndex[tokenId] = _allTokens.length;
        _allTokens.push(tokenId);
    }

    /**
     * @dev Private function to remove a token from this extension's ownership-tracking data structures. Note that
     * while the token is not assigned a new owner, the `_ownedTokensIndex` mapping is _not_ updated: this allows for
     * gas optimizations e.g. when performing a transfer operation (avoiding double writes).
     * This has O(1) time complexity, but alters the order of the _ownedTokens array.
     * @param from address representing the previous owner of the given token ID
     * @param tokenId uint256 ID of the token to be removed from the tokens list of the given address
     */
    function _removeTokenFromOwnerEnumeration(
        address from,
        uint256 tokenId
    ) private {
        // To prevent a gap in from's tokens array, we store the last token in the index of the token to delete, and
        // then delete the last slot (swap and pop).

        uint256 lastTokenIndex = balanceOf(from);
        uint256 tokenIndex = _ownedTokensIndex[tokenId];

        // When the token to delete is the last token, the swap operation is unnecessary
        if (tokenIndex != lastTokenIndex) {
            uint256 lastTokenId = _ownedTokens[from][lastTokenIndex];

            _ownedTokens[from][tokenIndex] = lastTokenId; // Move the last token to the slot of the to-delete token
            _ownedTokensIndex[lastTokenId] = tokenIndex; // Update the moved token's index
        }

        // This also deletes the contents at the last position of the array
        delete _ownedTokensIndex[tokenId];
        delete _ownedTokens[from][lastTokenIndex];
    }

    /**
     * @dev Private function to remove a token from this extension's token tracking data structures.
     * This has O(1) time complexity, but alters the order of the _allTokens array.
     * @param tokenId uint256 ID of the token to be removed from the tokens list
     */
    function _removeTokenFromAllTokensEnumeration(uint256 tokenId) private {
        // To prevent a gap in the tokens array, we store the last token in the index of the token to delete, and
        // then delete the last slot (swap and pop).

        uint256 lastTokenIndex = _allTokens.length - 1;
        uint256 tokenIndex = _allTokensIndex[tokenId];

        // When the token to delete is the last token, the swap operation is unnecessary. However, since this occurs so
        // rarely (when the last minted token is burnt) that we still do the swap here to avoid the gas cost of adding
        // an 'if' statement (like in _removeTokenFromOwnerEnumeration)
        uint256 lastTokenId = _allTokens[lastTokenIndex];

        _allTokens[tokenIndex] = lastTokenId; // Move the last token to the slot of the to-delete token
        _allTokensIndex[lastTokenId] = tokenIndex; // Update the moved token's index

        // This also deletes the contents at the last position of the array
        delete _allTokensIndex[tokenId];
        _allTokens.pop();
    }

    /**
     * See {ERC721-_increaseBalance}. We need that to account tokens that were minted in batch
     */
    function _increaseBalance(
        address account,
        uint128 amount
    ) internal virtual override {
        if (amount > 0) {
            revert ERC721EnumerableForbiddenBatchMint();
        }
        super._increaseBalance(account, amount);
    }
}
// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v5.0.0) (token/ERC721/ERC721.sol)

pragma solidity ^0.8.13;

import {IERC721} from "./IERC721.sol";
import {IERC721Metadata} from "./utils/IERC721Metadata.sol";
import {ERC721Utils} from "./utils/ERC721Utils.sol";
import {IERC165, ERC165} from "./utils/ERC165.sol";
import {IERC721Errors} from "./utils/IERC721Errors.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/Context.sol";

/**
 * @dev Implementation of https://eips.ethereum.org/EIPS/eip-721[ERC-721] Non-Fungible Token Standard, including
 * the Metadata extension, but not including the Enumerable extension, which is available separately as
 * {ERC721Enumerable}.
 */
abstract contract MRC721 is Context, ERC165, IERC721, IERC721Metadata, IERC721Errors {
    using Strings for uint256;

    // Token name
    string private _name;

    // Token symbol
    string private _symbol;

    mapping(uint256 => address) private _owners;

    mapping(address => uint256) private _balances;

    mapping(uint256 => address) private _tokenApprovals;

    mapping(address => mapping(address => bool)) private _operatorApprovals;

    /**
     * @dev Initializes the contract by setting a `name` and a `symbol` to the token collection.
     */
    function _init(string memory name_, string memory symbol_) internal  {
        _name = name_;
        _symbol = symbol_;
    }

    /**
     * @dev See {IERC165-supportsInterface}.
     */
    function supportsInterface(bytes4 interfaceId) public view virtual override(ERC165, IERC165) returns (bool) {
        return
            interfaceId == type(IERC721).interfaceId ||
            interfaceId == type(IERC721Metadata).interfaceId ||
            super.supportsInterface(interfaceId);
    }

    /**
     * @dev See {IERC721-balanceOf}.
     */
    function balanceOf(address owner) public view virtual returns (uint256) {
        if (owner == address(0)) {
            revert ERC721InvalidOwner(address(0));
        }
        return _balances[owner];
    }

    /**
     * @dev See {IERC721-ownerOf}.
     */
    function ownerOf(uint256 tokenId) public view virtual returns (address) {
        return _requireOwned(tokenId);
    }

    /**
     * @dev See {IERC721Metadata-name}.
     */
    function name() public view virtual returns (string memory) {
        return _name;
    }

    /**
     * @dev See {IERC721Metadata-symbol}.
     */
    function symbol() public view virtual returns (string memory) {
        return _symbol;
    }

    /**
     * @dev See {IERC721Metadata-tokenURI}.
     */
    function tokenURI(uint256 tokenId) public view virtual returns (string memory) {
        _requireOwned(tokenId);

        string memory baseURI = _baseURI();
        return bytes(baseURI).length > 0 ? string.concat(baseURI, tokenId.toString()) : "";
    }

    /**
     * @dev Base URI for computing {tokenURI}. If set, the resulting URI for each
     * token will be the concatenation of the `baseURI` and the `tokenId`. Empty
     * by default, can be overridden in child contracts.
     */
    function _baseURI() internal view virtual returns (string memory) {
        return "";
    }

    /**
     * @dev See {IERC721-approve}.
     */
    function approve(address to, uint256 tokenId) public virtual {
        _approve(to, tokenId, _msgSender());
    }

    /**
     * @dev See {IERC721-getApproved}.
     */
    function getApproved(uint256 tokenId) public view virtual returns (address) {
        _requireOwned(tokenId);

        return _getApproved(tokenId);
    }

    /**
     * @dev See {IERC721-setApprovalForAll}.
     */
    function setApprovalForAll(address operator, bool approved) public virtual {
        _setApprovalForAll(_msgSender(), operator, approved);
    }

    /**
     * @dev See {IERC721-isApprovedForAll}.
     */
    function isApprovedForAll(address owner, address operator) public view virtual returns (bool) {
        return _operatorApprovals[owner][operator];
    }

    /**
     * @dev See {IERC721-transferFrom}.
     */
    function transferFrom(address from, address to, uint256 tokenId) public virtual {
        if (to == address(0)) {
            revert ERC721InvalidReceiver(address(0));
        }
        // Setting an "auth" arguments enables the `_isAuthorized` check which verifies that the token exists
        // (from != 0). Therefore, it is not needed to verify that the return value is not 0 here.
        address previousOwner = _update(to, tokenId, _msgSender());
        if (previousOwner != from) {
            revert ERC721IncorrectOwner(from, tokenId, previousOwner);
        }
    }

    /**
     * @dev See {IERC721-safeTransferFrom}.
     */
    function safeTransferFrom(address from, address to, uint256 tokenId) public {
        safeTransferFrom(from, to, tokenId, "");
    }

    /**
     * @dev See {IERC721-safeTransferFrom}.
     */
    function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory data) public virtual {
        transferFrom(from, to, tokenId);
        ERC721Utils.checkOnERC721Received(_msgSender(), from, to, tokenId, data);
    }

    /**
     * @dev Returns the owner of the `tokenId`. Does NOT revert if token doesn't exist
     *
     * IMPORTANT: Any overrides to this function that add ownership of tokens not tracked by the
     * core ERC-721 logic MUST be matched with the use of {_increaseBalance} to keep balances
     * consistent with ownership. The invariant to preserve is that for any address `a` the value returned by
     * `balanceOf(a)` must be equal to the number of tokens such that `_ownerOf(tokenId)` is `a`.
     */
    function _ownerOf(uint256 tokenId) internal view virtual returns (address) {
        return _owners[tokenId];
    }

    /**
     * @dev Returns the approved address for `tokenId`. Returns 0 if `tokenId` is not minted.
     */
    function _getApproved(uint256 tokenId) internal view virtual returns (address) {
        return _tokenApprovals[tokenId];
    }

    /**
     * @dev Returns whether `spender` is allowed to manage `owner`'s tokens, or `tokenId` in
     * particular (ignoring whether it is owned by `owner`).
     *
     * WARNING: This function assumes that `owner` is the actual owner of `tokenId` and does not verify this
     * assumption.
     */
    function _isAuthorized(address owner, address spender, uint256 tokenId) internal view virtual returns (bool) {
        return
            spender != address(0) &&
            (owner == spender || isApprovedForAll(owner, spender) || _getApproved(tokenId) == spender);
    }

    /**
     * @dev Checks if `spender` can operate on `tokenId`, assuming the provided `owner` is the actual owner.
     * Reverts if `spender` does not have approval from the provided `owner` for the given token or for all its assets
     * the `spender` for the specific `tokenId`.
     *
     * WARNING: This function assumes that `owner` is the actual owner of `tokenId` and does not verify this
     * assumption.
     */
    function _checkAuthorized(address owner, address spender, uint256 tokenId) internal view virtual {
        if (!_isAuthorized(owner, spender, tokenId)) {
            if (owner == address(0)) {
                revert ERC721NonexistentToken(tokenId);
            } else {
                revert ERC721InsufficientApproval(spender, tokenId);
            }
        }
    }

    /**
     * @dev Unsafe write access to the balances, used by extensions that "mint" tokens using an {ownerOf} override.
     *
     * NOTE: the value is limited to type(uint128).max. This protect against _balance overflow. It is unrealistic that
     * a uint256 would ever overflow from increments when these increments are bounded to uint128 values.
     *
     * WARNING: Increasing an account's balance using this function tends to be paired with an override of the
     * {_ownerOf} function to resolve the ownership of the corresponding tokens so that balances and ownership
     * remain consistent with one another.
     */
    function _increaseBalance(address account, uint128 value) internal virtual {
        unchecked {
            _balances[account] += value;
        }
    }

    /**
     * @dev Transfers `tokenId` from its current owner to `to`, or alternatively mints (or burns) if the current owner
     * (or `to`) is the zero address. Returns the owner of the `tokenId` before the update.
     *
     * The `auth` argument is optional. If the value passed is non 0, then this function will check that
     * `auth` is either the owner of the token, or approved to operate on the token (by the owner).
     *
     * Emits a {Transfer} event.
     *
     * NOTE: If overriding this function in a way that tracks balances, see also {_increaseBalance}.
     */
    function _update(address to, uint256 tokenId, address auth) internal virtual returns (address) {
        address from = _ownerOf(tokenId);

        // Perform (optional) operator check
        if (auth != address(0)) {
            _checkAuthorized(from, auth, tokenId);
        }

        // Execute the update
        if (from != address(0)) {
            // Clear approval. No need to re-authorize or emit the Approval event
            _approve(address(0), tokenId, address(0), false);

            unchecked {
                _balances[from] -= 1;
            }
        }

        if (to != address(0)) {
            unchecked {
                _balances[to] += 1;
            }
        }

        _owners[tokenId] = to;

        emit Transfer(from, to, tokenId);

        return from;
    }

    /**
     * @dev Mints `tokenId` and transfers it to `to`.
     *
     * WARNING: Usage of this method is discouraged, use {_safeMint} whenever possible
     *
     * Requirements:
     *
     * - `tokenId` must not exist.
     * - `to` cannot be the zero address.
     *
     * Emits a {Transfer} event.
     */
    function _mint(address to, uint256 tokenId) internal {
        if (to == address(0)) {
            revert ERC721InvalidReceiver(address(0));
        }
        address previousOwner = _update(to, tokenId, address(0));
        if (previousOwner != address(0)) {
            revert ERC721InvalidSender(address(0));
        }
    }

    /**
     * @dev Mints `tokenId`, transfers it to `to` and checks for `to` acceptance.
     *
     * Requirements:
     *
     * - `tokenId` must not exist.
     * - If `to` refers to a smart contract, it must implement {IERC721Receiver-onERC721Received}, which is called upon a safe transfer.
     *
     * Emits a {Transfer} event.
     */
    function _safeMint(address to, uint256 tokenId) internal {
        _safeMint(to, tokenId, "");
    }

    /**
     * @dev Same as {xref-ERC721-_safeMint-address-uint256-}[`_safeMint`], with an additional `data` parameter which is
     * forwarded in {IERC721Receiver-onERC721Received} to contract recipients.
     */
    function _safeMint(address to, uint256 tokenId, bytes memory data) internal virtual {
        _mint(to, tokenId);
        ERC721Utils.checkOnERC721Received(_msgSender(), address(0), to, tokenId, data);
    }

    /**
     * @dev Destroys `tokenId`.
     * The approval is cleared when the token is burned.
     * This is an internal function that does not check if the sender is authorized to operate on the token.
     *
     * Requirements:
     *
     * - `tokenId` must exist.
     *
     * Emits a {Transfer} event.
     */
    function _burn(uint256 tokenId) internal {
        address previousOwner = _update(address(0), tokenId, address(0));
        if (previousOwner == address(0)) {
            revert ERC721NonexistentToken(tokenId);
        }
    }

    /**
     * @dev Transfers `tokenId` from `from` to `to`.
     *  As opposed to {transferFrom}, this imposes no restrictions on msg.sender.
     *
     * Requirements:
     *
     * - `to` cannot be the zero address.
     * - `tokenId` token must be owned by `from`.
     *
     * Emits a {Transfer} event.
     */
    function _transfer(address from, address to, uint256 tokenId) internal {
        if (to == address(0)) {
            revert ERC721InvalidReceiver(address(0));
        }
        address previousOwner = _update(to, tokenId, address(0));
        if (previousOwner == address(0)) {
            revert ERC721NonexistentToken(tokenId);
        } else if (previousOwner != from) {
            revert ERC721IncorrectOwner(from, tokenId, previousOwner);
        }
    }

    /**
     * @dev Safely transfers `tokenId` token from `from` to `to`, checking that contract recipients
     * are aware of the ERC-721 standard to prevent tokens from being forever locked.
     *
     * `data` is additional data, it has no specified format and it is sent in call to `to`.
     *
     * This internal function is like {safeTransferFrom} in the sense that it invokes
     * {IERC721Receiver-onERC721Received} on the receiver, and can be used to e.g.
     * implement alternative mechanisms to perform token transfer, such as signature-based.
     *
     * Requirements:
     *
     * - `tokenId` token must exist and be owned by `from`.
     * - `to` cannot be the zero address.
     * - `from` cannot be the zero address.
     * - If `to` refers to a smart contract, it must implement {IERC721Receiver-onERC721Received}, which is called upon a safe transfer.
     *
     * Emits a {Transfer} event.
     */
    function _safeTransfer(address from, address to, uint256 tokenId) internal {
        _safeTransfer(from, to, tokenId, "");
    }

    /**
     * @dev Same as {xref-ERC721-_safeTransfer-address-address-uint256-}[`_safeTransfer`], with an additional `data` parameter which is
     * forwarded in {IERC721Receiver-onERC721Received} to contract recipients.
     */
    function _safeTransfer(address from, address to, uint256 tokenId, bytes memory data) internal virtual {
        _transfer(from, to, tokenId);
        ERC721Utils.checkOnERC721Received(_msgSender(), from, to, tokenId, data);
    }

    /**
     * @dev Approve `to` to operate on `tokenId`
     *
     * The `auth` argument is optional. If the value passed is non 0, then this function will check that `auth` is
     * either the owner of the token, or approved to operate on all tokens held by this owner.
     *
     * Emits an {Approval} event.
     *
     * Overrides to this logic should be done to the variant with an additional `bool emitEvent` argument.
     */
    function _approve(address to, uint256 tokenId, address auth) internal {
        _approve(to, tokenId, auth, true);
    }

    /**
     * @dev Variant of `_approve` with an optional flag to enable or disable the {Approval} event. The event is not
     * emitted in the context of transfers.
     */
    function _approve(address to, uint256 tokenId, address auth, bool emitEvent) internal virtual {
        // Avoid reading the owner unless necessary
        if (emitEvent || auth != address(0)) {
            address owner = _requireOwned(tokenId);

            // We do not use _isAuthorized because single-token approvals should not be able to call approve
            if (auth != address(0) && owner != auth && !isApprovedForAll(owner, auth)) {
                revert ERC721InvalidApprover(auth);
            }

            if (emitEvent) {
                emit Approval(owner, to, tokenId);
            }
        }

        _tokenApprovals[tokenId] = to;
    }

    /**
     * @dev Approve `operator` to operate on all of `owner` tokens
     *
     * Requirements:
     * - operator can't be the address zero.
     *
     * Emits an {ApprovalForAll} event.
     */
    function _setApprovalForAll(address owner, address operator, bool approved) internal virtual {
        if (operator == address(0)) {
            revert ERC721InvalidOperator(operator);
        }
        _operatorApprovals[owner][operator] = approved;
        emit ApprovalForAll(owner, operator, approved);
    }

    /**
     * @dev Reverts if the `tokenId` doesn't have a current owner (it hasn't been minted, or it has been burned).
     * Returns the owner.
     *
     * Overrides to ownership logic should be done to {_ownerOf}.
     */
    function _requireOwned(uint256 tokenId) internal view returns (address) {
        address owner = _ownerOf(tokenId);
        if (owner == address(0)) {
            revert ERC721NonexistentToken(tokenId);
        }
        return owner;
    }
}// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v5.0.0) (utils/introspection/ERC165.sol)

pragma solidity ^0.8.13;

import {IERC165} from "./IERC165.sol";

/**
 * @dev Implementation of the {IERC165} interface.
 *
 * Contracts that want to implement ERC-165 should inherit from this contract and override {supportsInterface} to check
 * for the additional interface id that will be supported. For example:
 *
 * ```solidity
 * function supportsInterface(bytes4 interfaceId) public view virtual override returns (bool) {
 *     return interfaceId == type(MyInterface).interfaceId || super.supportsInterface(interfaceId);
 * }
 * ```
 */
abstract contract ERC165 is IERC165 {
    /**
     * @dev See {IERC165-supportsInterface}.
     */
    function supportsInterface(bytes4 interfaceId) public view virtual returns (bool) {
        return interfaceId == type(IERC165).interfaceId;
    }
}// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

import {IERC721Receiver} from "./IERC721Receiver.sol";
import {IERC721Errors} from "./IERC721Errors.sol";

/**
 * @dev Library that provide common ERC-721 utility functions.
 *
 * See https://eips.ethereum.org/EIPS/eip-721[ERC-721].
 */
library ERC721Utils {
    /**
     * @dev Performs an acceptance check for the provided `operator` by calling {IERC721-onERC721Received}
     * on the `to` address. The `operator` is generally the address that initiated the token transfer (i.e. `msg.sender`).
     *
     * The acceptance call is not executed and treated as a no-op if the target address is doesn't contain code (i.e. an EOA).
     * Otherwise, the recipient must implement {IERC721Receiver-onERC721Received} and return the acceptance magic value to accept
     * the transfer.
     */
    function checkOnERC721Received(
        address operator,
        address from,
        address to,
        uint256 tokenId,
        bytes memory data
    ) internal {
        if (to.code.length > 0) {
            try IERC721Receiver(to).onERC721Received(operator, from, tokenId, data) returns (bytes4 retval) {
                if (retval != IERC721Receiver.onERC721Received.selector) {
                    // Token rejected
                    revert IERC721Errors.ERC721InvalidReceiver(to);
                }
            } catch (bytes memory reason) {
                if (reason.length == 0) {
                    // non-IERC721Receiver implementer
                    revert IERC721Errors.ERC721InvalidReceiver(to);
                } else {
                    /// @solidity memory-safe-assembly
                    assembly {
                        revert(add(32, reason), mload(reason))
                    }
                }
            }
        }
    }
}// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v5.0.0) (utils/introspection/IERC165.sol)

pragma solidity ^0.8.13;

/**
 * @dev Interface of the ERC-165 standard, as defined in the
 * https://eips.ethereum.org/EIPS/eip-165[ERC].
 *
 * Implementers can declare support of contract interfaces, which can then be
 * queried by others ({ERC165Checker}).
 *
 * For an implementation, see {ERC165}.
 */
interface IERC165 {
    /**
     * @dev Returns true if this contract implements the interface defined by
     * `interfaceId`. See the corresponding
     * https://eips.ethereum.org/EIPS/eip-165#how-interfaces-are-identified[ERC section]
     * to learn more about how these ids are created.
     *
     * This function call must use less than 30 000 gas.
     */
    function supportsInterface(bytes4 interfaceId) external view returns (bool);
}// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v5.0.0) (token/ERC721/extensions/IERC721Enumerable.sol)

pragma solidity ^0.8.13;

import {IERC721} from "../IERC721.sol";

/**
 * @title ERC-721 Non-Fungible Token Standard, optional enumeration extension
 * @dev See https://eips.ethereum.org/EIPS/eip-721
 */
interface IERC721Enumerable is IERC721 {
    /**
     * @dev Returns the total amount of tokens stored by the contract.
     */
    function totalSupply() external view returns (uint256);

    /**
     * @dev Returns a token ID owned by `owner` at a given `index` of its token list.
     * Use along with {balanceOf} to enumerate all of ``owner``'s tokens.
     */
    function tokenOfOwnerByIndex(address owner, uint256 index) external view returns (uint256);

    /**
     * @dev Returns a token ID at a given `index` of all the tokens stored by the contract.
     * Use along with {totalSupply} to enumerate all tokens.
     */
    function tokenByIndex(uint256 index) external view returns (uint256);
}// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v5.0.0) (interfaces/draft-IERC6093.sol)
pragma solidity ^0.8.13;

/**
 * @dev Standard ERC-721 Errors
 * Interface of the https://eips.ethereum.org/EIPS/eip-6093[ERC-6093] custom errors for ERC-721 tokens.
 */
interface IERC721Errors {
    /**
     * @dev Indicates that an address can't be an owner. For example, `address(0)` is a forbidden owner in ERC-20.
     * Used in balance queries.
     * @param owner Address of the current owner of a token.
     */
    error ERC721InvalidOwner(address owner);

    /**
     * @dev Indicates a `tokenId` whose `owner` is the zero address.
     * @param tokenId Identifier number of a token.
     */
    error ERC721NonexistentToken(uint256 tokenId);

    /**
     * @dev Indicates an error related to the ownership over a particular token. Used in transfers.
     * @param sender Address whose tokens are being transferred.
     * @param tokenId Identifier number of a token.
     * @param owner Address of the current owner of a token.
     */
    error ERC721IncorrectOwner(address sender, uint256 tokenId, address owner);

    /**
     * @dev Indicates a failure with the token `sender`. Used in transfers.
     * @param sender Address whose tokens are being transferred.
     */
    error ERC721InvalidSender(address sender);

    /**
     * @dev Indicates a failure with the token `receiver`. Used in transfers.
     * @param receiver Address to which tokens are being transferred.
     */
    error ERC721InvalidReceiver(address receiver);

    /**
     * @dev Indicates a failure with the `operator`’s approval. Used in transfers.
     * @param operator Address that may be allowed to operate on tokens without being their owner.
     * @param tokenId Identifier number of a token.
     */
    error ERC721InsufficientApproval(address operator, uint256 tokenId);

    /**
     * @dev Indicates a failure with the `approver` of a token to be approved. Used in approvals.
     * @param approver Address initiating an approval operation.
     */
    error ERC721InvalidApprover(address approver);

    /**
     * @dev Indicates a failure with the `operator` to be approved. Used in approvals.
     * @param operator Address that may be allowed to operate on tokens without being their owner.
     */
    error ERC721InvalidOperator(address operator);
}

/**
 * @dev Standard ERC-1155 Errors
 * Interface of the https://eips.ethereum.org/EIPS/eip-6093[ERC-6093] custom errors for ERC-1155 tokens.
 */
interface IERC1155Errors {
    /**
     * @dev Indicates an error related to the current `balance` of a `sender`. Used in transfers.
     * @param sender Address whose tokens are being transferred.
     * @param balance Current balance for the interacting account.
     * @param needed Minimum amount required to perform a transfer.
     * @param tokenId Identifier number of a token.
     */
    error ERC1155InsufficientBalance(address sender, uint256 balance, uint256 needed, uint256 tokenId);

    /**
     * @dev Indicates a failure with the token `sender`. Used in transfers.
     * @param sender Address whose tokens are being transferred.
     */
    error ERC1155InvalidSender(address sender);

    /**
     * @dev Indicates a failure with the token `receiver`. Used in transfers.
     * @param receiver Address to which tokens are being transferred.
     */
    error ERC1155InvalidReceiver(address receiver);

    /**
     * @dev Indicates a failure with the `operator`’s approval. Used in transfers.
     * @param operator Address that may be allowed to operate on tokens without being their owner.
     * @param owner Address of the current owner of a token.
     */
    error ERC1155MissingApprovalForAll(address operator, address owner);

    /**
     * @dev Indicates a failure with the `approver` of a token to be approved. Used in approvals.
     * @param approver Address initiating an approval operation.
     */
    error ERC1155InvalidApprover(address approver);

    /**
     * @dev Indicates a failure with the `operator` to be approved. Used in approvals.
     * @param operator Address that may be allowed to operate on tokens without being their owner.
     */
    error ERC1155InvalidOperator(address operator);

    /**
     * @dev Indicates an array length mismatch between ids and values in a safeBatchTransferFrom operation.
     * Used in batch transfers.
     * @param idsLength Length of the array of token identifiers
     * @param valuesLength Length of the array of token amounts
     */
    error ERC1155InvalidArrayLength(uint256 idsLength, uint256 valuesLength);
}// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v5.0.0) (token/ERC721/extensions/IERC721Metadata.sol)

pragma solidity ^0.8.13;

import {IERC721} from "../IERC721.sol";

/**
 * @title ERC-721 Non-Fungible Token Standard, optional metadata extension
 * @dev See https://eips.ethereum.org/EIPS/eip-721
 */
interface IERC721Metadata is IERC721 {
    /**
     * @dev Returns the token collection name.
     */
    function name() external view returns (string memory);

    /**
     * @dev Returns the token collection symbol.
     */
    function symbol() external view returns (string memory);

    /**
     * @dev Returns the Uniform Resource Identifier (URI) for `tokenId` token.
     */
    function tokenURI(uint256 tokenId) external view returns (string memory);
}// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v5.0.0) (token/ERC721/IERC721Receiver.sol)

pragma solidity ^0.8.13;

/**
 * @title ERC-721 token receiver interface
 * @dev Interface for any contract that wants to support safeTransfers
 * from ERC-721 asset contracts.
 */
interface IERC721Receiver {
    /**
     * @dev Whenever an {IERC721} `tokenId` token is transferred to this contract via {IERC721-safeTransferFrom}
     * by `operator` from `from`, this function is called.
     *
     * It must return its Solidity selector to confirm the token transfer.
     * If any other value is returned or the interface is not implemented by the recipient, the transfer will be
     * reverted.
     *
     * The selector can be obtained in Solidity with `IERC721Receiver.onERC721Received.selector`.
     */
    function onERC721Received(
        address operator,
        address from,
        uint256 tokenId,
        bytes calldata data
    ) external returns (bytes4);
}// SPDX-License-Identifier: UNLICENSED

pragma solidity >=0.5.0;

interface IMicroManager {
    function microBridge(address _address) external view returns (bool);

    function treasuryAddress() external view returns (address);

    function microProtocolFee() external view returns (uint256);

    function oracleAddress() external view returns (address);
}
// SPDX-License-Identifier: MIT

pragma solidity >=0.5.0;

interface IPriceOracle {
    function convertUsdToWei(uint256 usdAmount) external view returns (uint256 weiAmount);
}// SPDX-License-Identifier: MIT

pragma solidity ^0.8.4;
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import {IPriceOracle} from "./interfaces/IPriceOracle.sol";
import {IMicroManager} from "./interfaces/IMicroManager.sol";

error PaymentFailed();

contract MicroUtilityV4 {
    using SafeMath for uint256;
    IMicroManager public microManager;
    uint256 private constant STATIC_GAS_LIMIT = 210_000;

    event FeePayout(
        uint256 MicroMintFeeWei,
        address MicroFeeRecipient,
        bool success
    );

    /**
     * PUBLIC FUNCTIONS
     * state changing
     */

    function getMicroFeeWei(uint256 quantity) public view returns (uint256) {
        if (quantity == 0) {
            return 0;
        }
        return
            IPriceOracle(microManager.oracleAddress()).convertUsdToWei(
                microManager.microProtocolFee().mul(quantity)
            );
    }

    function _payoutMicroFee(uint256 microProtocolFee) internal {
        address treasury = microManager.treasuryAddress();
        _payoutRemainder(treasury, microProtocolFee);
        emit FeePayout(microProtocolFee, treasury, true);
    }

    function _setManager(address _manager) internal {
        microManager = IMicroManager(_manager);
    }

    function _payoutRemainder(address recipient, uint256 value) internal {
        if (value > 0) {
            (bool success, ) = payable(recipient).call{
                value: value,
                gas: gasleft() > STATIC_GAS_LIMIT ? STATIC_GAS_LIMIT : gasleft()
            }("");
            if (!success) {
                revert PaymentFailed();
            }
        }
    }
}
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import "../MicroUtilityV4.sol";
import "../erc721/Micro3.sol";

error SaleInactive();
error PurchaseWrongPrice(uint256 correctPrice);
error SoldOut();
error PurchaseTooManyForAddress();
error Canceled();
error IsNotBridge();
error SaleCanNotUpdate();
error InvalidSaleDetail();
error SaleIsNotEnded();
error Unauthorized();
error PresaleMerkleNotApproved();

contract MicroNFTProxyV2 is Micro3, ReentrancyGuard, MicroUtilityV4 {
    using Strings for uint256;
    using SafeMath for uint256;

    uint256 public constant VERSION = 4;
    address public owner;
    string private _baseURL;
    string private _notRevealedURL;
    bool private _initialized;
    uint224 private _currentTokenId;

    struct SaleConfiguration {
        uint64 editionSize;
        uint16 profitSharing;
        address payable fundsRecipient;
        uint256 publicSalePrice;
        uint32 maxSalePurchasePerAddress;
        uint64 publicSaleStart;
        uint64 publicSaleEnd;
        bytes32 presaleMerkleRoot;
        bool cancelable;
    }

    mapping(address => uint256) public totalMintsByAddress;

    SaleConfiguration public saleConfig;

    event CrossMint(
        address indexed _to,
        uint256 _quantity,
        uint256 _srcChainId
    );

    event BridgeIn(address indexed _to, uint256 _dstChainId, uint256 _tokenId);

    event BridgeOut(
        address indexed _from,
        uint256 _dstChainId,
        uint256 _tokenId
    );

    event Purchase(
        address indexed to,
        uint256 indexed quantity,
        uint256 indexed price,
        uint256 firstMintedTokenId
    );

    event OpenMintFinalized(
        address indexed sender,
        uint256 editionSize,
        uint256 timeEnd
    );

    event AddMerkleProof(
        bytes32 indexed merkle
    );

    event CancelSaleEdition(address indexed sender, uint256 lastTimeUpdated);

    event PublicSaleCollection(address indexed sender, uint256 lastTimeUpdated);

    event FundsWithdrawn(
        address indexed sender,
        address indexed fundsRecipient,
        uint256 fund
    );

    modifier onlyOwner() {
        require(owner == _msgSender());
        _;
    }

    modifier onlyBridge() {
        if (!microManager.microBridge(_msgSender())) {
            revert IsNotBridge();
        }
        _;
    }

    modifier onlyCancelable() {
        if (saleConfig.cancelable) {
            revert Canceled();
        }
        _;
    }

    modifier canMintTokens(uint256 quantity) {
        if (
            saleConfig.editionSize != 0 &&
            quantity + _currentTokenId > saleConfig.editionSize
        ) {
            revert SoldOut();
        }
        _;
    }

    modifier onlyPublicSaleActive() {
        if (
            !(saleConfig.publicSaleStart <= block.timestamp &&
                saleConfig.publicSaleEnd > block.timestamp)
        ) {
            revert SaleInactive();
        }
        _;
    }

    function init(bytes memory initPayload) external returns (bool) {
        if (_initialized) {
            revert Unauthorized();
        }
        (
            string memory _url,
            string memory _singleUrl,
            string memory _name,
            string memory _symbol,
            address _owner,
            address _manager
        ) = abi.decode(
                initPayload,
                (string, string, string, string, address, address)
            );
        owner = _owner;
        _setManager(_manager);
        _baseURL = _url;
        _notRevealedURL = _singleUrl;
        _init(_name, _symbol);
        _initialized = true;
        return true;
    }

    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        override
        returns (string memory)
    {
        _requireOwned(tokenId);

        if (bytes(_notRevealedURL).length > 0) {
            return _notRevealedURL;
        }

        return
            bytes(_baseURL).length > 0
                ? string(
                    abi.encodePacked(_baseURL, tokenId.toString(), ".json")
                )
                : "";
    }

    function setBaseURI(string memory _newURI) external onlyOwner {
        _setBaseURI(_newURI);
    }

    function setNotRevealedURI(string memory _newURI) external onlyOwner {
        _notRevealedURL = _newURI;
    }

    /**
     * Owner, Admin FUNCTIONS
     * non state changing
     */

    function transferOwnership(address newOwner) external onlyOwner {
        if(newOwner == address(0)){
            revert Unauthorized();
        }
        _setOwner(newOwner);
    }

    function adminMint(address recipient, uint256 quantity)
        external
        onlyOwner
        canMintTokens(quantity)
        returns (uint256)
    {
        _mintNFTs(recipient, quantity);

        return _currentTokenId;
    }

    function setSaleDetail(bytes memory initPayload)
        external
        onlyCancelable
        onlyOwner
    {
        if (
            saleConfig.publicSaleStart != 0 &&
            block.timestamp > saleConfig.publicSaleStart
        ) {
            revert SaleCanNotUpdate();
        }

        SaleConfiguration memory config = abi.decode(
            initPayload,
            (SaleConfiguration)
        );

        if (
            config.publicSaleStart <= block.timestamp ||
            config.publicSaleEnd <= config.publicSaleStart ||
            config.profitSharing > 50 ||
            config.fundsRecipient == address(0)
        ) {
            revert InvalidSaleDetail();
        }

        saleConfig = SaleConfiguration({
            editionSize: config.editionSize,
            profitSharing: config.profitSharing,
            fundsRecipient: config.fundsRecipient,
            publicSalePrice: config.publicSalePrice,
            maxSalePurchasePerAddress: config.maxSalePurchasePerAddress,
            publicSaleStart: config.publicSaleStart,
            publicSaleEnd: config.publicSaleEnd,
            presaleMerkleRoot: config.presaleMerkleRoot,
            cancelable: false
        });

        emit PublicSaleCollection(_msgSender(), block.timestamp);
    }

    function setMerkleProof(bytes32 _merkle) external onlyCancelable onlyOwner {
        saleConfig.presaleMerkleRoot = _merkle;
        emit AddMerkleProof(_merkle);
    }

    function finalizeOpenEdition() external onlyCancelable onlyOwner {
        saleConfig.editionSize = uint64(_currentTokenId);
        saleConfig.publicSaleEnd = uint64(block.timestamp);
        emit OpenMintFinalized(
            _msgSender(),
            saleConfig.editionSize,
            block.timestamp
        );
    }

    function cancelSaleEdition() external onlyCancelable onlyOwner {
        if (block.timestamp > saleConfig.publicSaleEnd) {
            revert SaleIsNotEnded();
        }
        saleConfig.cancelable = true;
        emit CancelSaleEdition(_msgSender(), block.timestamp);
    }

    /**
     * EXTERNAL FUNCTIONS
     * state changing
     */
    function purchase(uint256 quantity)
        external
        payable
        onlyCancelable
        canMintTokens(quantity)
        onlyPublicSaleActive
        nonReentrant
        returns (uint256)
    {
        if(saleConfig.presaleMerkleRoot != bytes32(0)){
            revert Unauthorized();
        }

        address minter = _msgSender();
        
        uint256 salePrice = saleConfig.publicSalePrice.mul(quantity);

        uint256 protocolFee = getMicroFeeWei(quantity);

        uint256 totalFee = salePrice.add(protocolFee);

        _isMinting(minter, msg.value, totalFee, quantity);

        _payoutMicroFee(protocolFee);

        _payoutFundingRaise(salePrice);

        _payoutRemainder(minter, msg.value.sub(totalFee));

        emit Purchase({
            to: minter,
            quantity: quantity,
            price: saleConfig.publicSalePrice,
            firstMintedTokenId: _currentTokenId
        });

        return _currentTokenId;
    }

    function purchasePresale(uint256 quantity, bytes32[] calldata merkleProof)
        external
        payable
        onlyCancelable
        canMintTokens(quantity)
        onlyPublicSaleActive
        nonReentrant
        returns (uint256)
    {
        address minter = _msgSender();

        if (
            !MerkleProof.verify(
                merkleProof,
                saleConfig.presaleMerkleRoot,
                keccak256(abi.encodePacked(minter))
            )
        ) {
            revert PresaleMerkleNotApproved();
        }

        uint256 salePrice = saleConfig.publicSalePrice.mul(quantity);

        uint256 protocolFee = getMicroFeeWei(quantity);

        uint256 totalFee = salePrice.add(protocolFee);

        _isMinting(minter, msg.value, totalFee, quantity);

        _payoutMicroFee(protocolFee);

        _payoutFundingRaise(salePrice);

        _payoutRemainder(minter, msg.value.sub(totalFee));

        emit Purchase({
            to: minter,
            quantity: quantity,
            price: saleConfig.publicSalePrice,
            firstMintedTokenId: _currentTokenId
        });

        return _currentTokenId;
    }

    function bridgeOut(
        address _from,
        uint64 _dstChainId,
        uint256 _tokenId
    ) external onlyBridge {
        _burn(_tokenId);
        emit BridgeOut(_from, _dstChainId, _tokenId);
    }

    function bridgeIn(
        address _toAddress,
        uint64 _dstChainId,
        uint256 _tokenId
    ) external onlyBridge {
        _safeMint(_toAddress, _tokenId);
        emit BridgeIn(_toAddress, _dstChainId, _tokenId);
    }

    function crossMint(
        address _toAddress,
        address _fundAddress,
        uint256 _quantity,
        uint256 _priceCheck,
        uint64 _srcChainId
    )
        external
        onlyBridge
        canMintTokens(_quantity)
        onlyCancelable
        onlyPublicSaleActive
    {
        if (saleConfig.fundsRecipient != _fundAddress) {
            revert Unauthorized();
        }

        _isMinting(_toAddress, _priceCheck, saleConfig.publicSalePrice.mul(_quantity), _quantity);

        emit CrossMint(_toAddress, _quantity, _srcChainId);
    }

    /**
     * INTERNAL FUNCTIONS
     * state changing
     */
    function _mintNFTs(address recipient, uint256 quantity) internal {
        for (uint256 i; i < quantity; ) {
            _currentTokenId += 1;
            _safeMint(
                recipient,
                uint256(
                    bytes32(
                        abi.encodePacked(
                            uint32(block.chainid),
                            uint224(_currentTokenId)
                        )
                    )
                )
            );
            unchecked {
                ++i;
            }
        }
    }

    function _payoutFundingRaise(uint256 totalPurchase)
        internal
        returns (bool)
    {
        if (saleConfig.fundsRecipient == address(0) || totalPurchase == 0) {
            return false;
        }

        _payoutRemainder(saleConfig.fundsRecipient, totalPurchase);

        emit FundsWithdrawn(
            _msgSender(),
            saleConfig.fundsRecipient,
            totalPurchase
        );

        return true;
    }

    function _isMinting(address toAddress, uint256 payableValue, uint256 totalFee, uint256 quantity)
        internal
    {
        if(quantity == 0) {
            revert Unauthorized();
        }

        if (payableValue < totalFee) {
            revert PurchaseWrongPrice(totalFee);
        }

        if (
            saleConfig.maxSalePurchasePerAddress != 0 &&
            totalMintsByAddress[toAddress].add(quantity) >
            saleConfig.maxSalePurchasePerAddress
        ) {
            revert PurchaseTooManyForAddress();
        }

        _mintNFTs(toAddress, quantity);

        totalMintsByAddress[toAddress] += quantity;
    }

    function _setBaseURI(string memory _newURI) internal {
        _baseURL = _newURI;
    }

    function _setOwner(address newOwner) internal {
        owner = newOwner;
    }
}
'''

识别的结果：
'''
function _msgSender() internal view virtual returns (address) 
function _msgData() internal view virtual returns (bytes calldata) 
function verify( bytes32[] memory proof, bytes32 root, bytes32 leaf ) internal pure returns (bool) 
function tryAdd(uint256 a, uint256 b) internal pure returns (bool, uint256) 
function trySub(uint256 a, uint256 b) internal pure returns (bool, uint256) 
function tryMul(uint256 a, uint256 b) internal pure returns (bool, uint256) 
function tryDiv(uint256 a, uint256 b) internal pure returns (bool, uint256) 
function tryMod(uint256 a, uint256 b) internal pure returns (bool, uint256) 
function add(uint256 a, uint256 b) internal pure returns (uint256) 
function sub(uint256 a, uint256 b) internal pure returns (uint256) 
function mul(uint256 a, uint256 b) internal pure returns (uint256) 
function div(uint256 a, uint256 b) internal pure returns (uint256) 
function mod(uint256 a, uint256 b) internal pure returns (uint256) 
function sub( uint256 a, uint256 b, string memory errorMessage ) internal pure returns (uint256) 
function div( uint256 a, uint256 b, string memory errorMessage ) internal pure returns (uint256) 
function mod( uint256 a, uint256 b, string memory errorMessage ) internal pure returns (uint256) 
function toString(uint256 value) internal pure returns (string memory) 
function toHexString(uint256 value) internal pure returns (string memory) 
function toHexString(uint256 value, uint256 length) internal pure returns (string memory) 
function supportsInterface( bytes4 interfaceId ) public view virtual override(IERC165, MRC721) returns (bool) 
function tokenOfOwnerByIndex( address owner, uint256 index ) public view virtual returns (uint256) 
function totalSupply() public view virtual returns (uint256) 
function tokenByIndex(uint256 index) public view virtual returns (uint256) 
function _update( address to, uint256 tokenId, address auth ) internal virtual override returns (address) 
function _addTokenToOwnerEnumeration(address to, uint256 tokenId) private 
function _addTokenToAllTokensEnumeration(uint256 tokenId) private 
function _removeTokenFromOwnerEnumeration( address from, uint256 tokenId ) private 
function _removeTokenFromAllTokensEnumeration(uint256 tokenId) private 
function _increaseBalance( address account, uint128 amount ) internal virtual override 
function _init(string memory name_, string memory symbol_) internal  
function supportsInterface(bytes4 interfaceId) public view virtual override(ERC165, IERC165) returns (bool) 
function balanceOf(address owner) public view virtual returns (uint256) 
function ownerOf(uint256 tokenId) public view virtual returns (address) 
function name() public view virtual returns (string memory) 
function symbol() public view virtual returns (string memory) 
function tokenURI(uint256 tokenId) public view virtual returns (string memory) 
function _baseURI() internal view virtual returns (string memory) 
function approve(address to, uint256 tokenId) public virtual 
function getApproved(uint256 tokenId) public view virtual returns (address) 
function setApprovalForAll(address operator, bool approved) public virtual 
function isApprovedForAll(address owner, address operator) public view virtual returns (bool) 
function transferFrom(address from, address to, uint256 tokenId) public virtual 
function safeTransferFrom(address from, address to, uint256 tokenId) public 
function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory data) public virtual 
function _ownerOf(uint256 tokenId) internal view virtual returns (address) 
function _getApproved(uint256 tokenId) internal view virtual returns (address) 
function _isAuthorized(address owner, address spender, uint256 tokenId) internal view virtual returns (bool) 
function _checkAuthorized(address owner, address spender, uint256 tokenId) internal view virtual 
function _increaseBalance(address account, uint128 value) internal virtual 
function _update(address to, uint256 tokenId, address auth) internal virtual returns (address) 
function _mint(address to, uint256 tokenId) internal 
function _safeMint(address to, uint256 tokenId) internal 
function _safeMint(address to, uint256 tokenId, bytes memory data) internal virtual 
function _burn(uint256 tokenId) internal 
function _transfer(address from, address to, uint256 tokenId) internal 
function _safeTransfer(address from, address to, uint256 tokenId) internal 
function _safeTransfer(address from, address to, uint256 tokenId, bytes memory data) internal virtual 
function _approve(address to, uint256 tokenId, address auth) internal 
function _approve(address to, uint256 tokenId, address auth, bool emitEvent) internal virtual 
function _setApprovalForAll(address owner, address operator, bool approved) internal virtual 
function _requireOwned(uint256 tokenId) internal view returns (address) 
function supportsInterface(bytes4 interfaceId) public view virtual returns (bool) 
function checkOnERC721Received( address operator, address from, address to, uint256 tokenId, bytes memory data ) internal 
function onERC721Received( address operator, address from, uint256 tokenId, bytes calldata data ) external returns (bytes4); }// SPDX-License-Identifier: UNLICENSED  pragma solidity >=0.5.0;  interface IMicroManager 
function getMicroFeeWei(uint256 quantity) public view returns (uint256) 
function _payoutMicroFee(uint256 microProtocolFee) internal 
function _setManager(address _manager) internal 
function _payoutRemainder(address recipient, uint256 value) internal 
function init(bytes memory initPayload) external returns (bool) 
function tokenURI(uint256 tokenId) public view virtual override returns (string memory) 
function setBaseURI(string memory _newURI) external onlyOwner 
function setNotRevealedURI(string memory _newURI) external onlyOwner 
function transferOwnership(address newOwner) external onlyOwner 
function adminMint(address recipient, uint256 quantity) external onlyOwner canMintTokens(quantity) returns (uint256) 
function setSaleDetail(bytes memory initPayload) external onlyCancelable onlyOwner 
function setMerkleProof(bytes32 _merkle) external onlyCancelable onlyOwner 
function finalizeOpenEdition() external onlyCancelable onlyOwner 
function cancelSaleEdition() external onlyCancelable onlyOwner 
function purchase(uint256 quantity) external payable onlyCancelable canMintTokens(quantity) onlyPublicSaleActive nonReentrant returns (uint256) 
function purchasePresale(uint256 quantity, bytes32[] calldata merkleProof) external payable onlyCancelable canMintTokens(quantity) onlyPublicSaleActive nonReentrant returns (uint256) 
function bridgeOut( address _from, uint64 _dstChainId, uint256 _tokenId ) external onlyBridge 
function bridgeIn( address _toAddress, uint64 _dstChainId, uint256 _tokenId ) external onlyBridge 
function crossMint( address _toAddress, address _fundAddress, uint256 _quantity, uint256 _priceCheck, uint64 _srcChainId ) external onlyBridge canMintTokens(_quantity) onlyCancelable onlyPublicSaleActive 
function _mintNFTs(address recipient, uint256 quantity) internal 
function _payoutFundingRaise(uint256 totalPurchase) internal returns (bool) 
function _isMinting(address toAddress, uint256 payableValue, uint256 totalFee, uint256 quantity) internal 
function _setBaseURI(string memory _newURI) internal 
function _setOwner(address newOwner) internal 
'''
