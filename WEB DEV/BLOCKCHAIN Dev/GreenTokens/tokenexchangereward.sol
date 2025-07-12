// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title TokenExchangeRewards
 * @dev Smart contract for exchanging tokens and providing rewards
 */
contract TokenExchangeRewards is Ownable, ReentrancyGuard {
    using SafeERC20 for IERC20;

    // Token that users will deposit
    IERC20 public depositToken;
    
    // Token that will be given as reward
    IERC20 public rewardToken;
    
    // Reward rate: How many reward tokens per deposit token
    uint256 public rewardRate = 10; // 10 reward tokens per deposit token
    
    // Minimum deposit amount to be eligible for rewards
    uint256 public minimumDeposit = 100 * 10**18; // 100 tokens with 18 decimals
    
    // Coupon voucher system
    struct Coupon {
        string code;
        uint256 discount;
        bool isValid;
    }
    
    // Mapping from coupon code hash to coupon details
    mapping(bytes32 => Coupon) public coupons;
    
    // Mapping to track user deposits
    mapping(address => uint256) public deposits;
    
    // Mapping to track if a user has claimed their reward
    mapping(address => bool) public hasClaimedReward;
    
    // Events
    event TokensDeposited(address indexed user, uint256 amount);
    event RewardClaimed(address indexed user, uint256 amount);
    event CouponRedeemed(address indexed user, string code, uint256 discount);
    event CouponCreated(string code, uint256 discount);
    
    /**
     * @dev Constructor to initialize the contract
     * @param _depositToken Address of the token users will deposit
     * @param _rewardToken Address of the token given as reward
     */
    constructor(address _depositToken, address _rewardToken) {
        depositToken = IERC20(_depositToken);
        rewardToken = IERC20(_rewardToken);
    }
    
    /**
     * @dev Deposit tokens to be eligible for rewards
     * @param amount The amount of tokens to deposit
     */
    function depositTokens(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be greater than 0");
        
        // Transfer tokens from user to contract
        depositToken.safeTransferFrom(msg.sender, address(this), amount);
        
        // Update user's deposit amount
        deposits[msg.sender] += amount;
        
        emit TokensDeposited(msg.sender, amount);
    }
    
    /**
     * @dev Claim rewards based on deposited tokens
     */
    function claimReward() external nonReentrant {
        uint256 userDeposit = deposits[msg.sender];
        require(userDeposit >= minimumDeposit, "Deposit amount too low");
        require(!hasClaimedReward[msg.sender], "Reward already claimed");
        
        // Calculate reward amount
        uint256 rewardAmount = (userDeposit * rewardRate) / 10**18;
        
        // Mark reward as claimed
        hasClaimedReward[msg.sender] = true;
        
        // Transfer reward tokens to user
        rewardToken.safeTransfer(msg.sender, rewardAmount);
        
        emit RewardClaimed(msg.sender, rewardAmount);
    }
    
    /**
     * @dev Create a new coupon (only owner can call)
     * @param code The coupon code
     * @param discount The discount amount/percentage
     */
    function createCoupon(string calldata code, uint256 discount) external onlyOwner {
        bytes32 codeHash = keccak256(abi.encodePacked(code));
        require(!coupons[codeHash].isValid, "Coupon already exists");
        
        coupons[codeHash] = Coupon({
            code: code,
            discount: discount,
            isValid: true
        });
        
        emit CouponCreated(code, discount);
    }
    
    /**
     * @dev Redeem a coupon
     * @param code The coupon code to redeem
     */
    function redeemCoupon(string calldata code) external nonReentrant {
        bytes32 codeHash = keccak256(abi.encodePacked(code));
        require(coupons[codeHash].isValid, "Invalid coupon code");
        
        // Mark coupon as used
        coupons[codeHash].isValid = false;
        
        // Emit event for off-chain processing
        emit CouponRedeemed(msg.sender, code, coupons[codeHash].discount);
    }
    
    /**
     * @dev Update the reward rate (only owner can call)
     * @param newRate The new reward rate
     */
    function updateRewardRate(uint256 newRate) external onlyOwner {
        rewardRate = newRate;
    }
    
    /**
     * @dev Update the minimum deposit amount (only owner can call)
     * @param newMinimum The new minimum deposit amount
     */
    function updateMinimumDeposit(uint256 newMinimum) external onlyOwner {
        minimumDeposit = newMinimum;
    }
    
    /**
     * @dev Withdraw tokens in case of emergency (only owner can call)
     * @param token The token to withdraw
     * @param amount The amount to withdraw
     */
    function emergencyWithdraw(address token, uint256 amount) external onlyOwner {
        IERC20(token).safeTransfer(owner(), amount);
    }
}