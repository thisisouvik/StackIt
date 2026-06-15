// Connect to Ethereum provider (e.g., MetaMask)
async function connectWallet() {
    if (window.ethereum) {
      try {
        // Request account access
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        return accounts[0];
      } catch (error) {
        console.error("User denied account access");
        return null;
      }
    } else {
      alert("Please install MetaMask to use this feature");
      return null;
    }
  }
  
  // Token Exchange Contract setup
  const contractAddress = "YOUR_DEPLOYED_CONTRACT_ADDRESS";
  const contractABI = [
    // Include the ABI from your compiled contract here
    // You can get this from the JSON file after compiling your Solidity code
  ];
  
  let tokenExchangeContract;
  let userAccount;
  
  // Initialize the contract
  async function initContract() {
    if (window.ethereum) {
      const web3 = new Web3(window.ethereum);
      userAccount = await connectWallet();
      
      if (userAccount) {
        tokenExchangeContract = new web3.eth.Contract(contractABI, contractAddress);
        updateUI();
      }
    }
  }
  
  // Function to deposit tokens
  async function depositTokens() {
    if (!userAccount || !tokenExchangeContract) return;
    
    const depositAmount = document.getElementById('depositAmount').value;
    const depositTokenAddress = await tokenExchangeContract.methods.depositToken().call();
    const depositTokenContract = new web3.eth.Contract(
      [
        {
          "constant": false,
          "inputs": [
            {
              "name": "_spender",
              "type": "address"
            },
            {
              "name": "_value",
              "type": "uint256"
            }
          ],
          "name": "approve",
          "outputs": [
            {
              "name": "",
              "type": "bool"
            }
          ],
          "payable": false,
          "stateMutability": "nonpayable",
          "type": "function"
        }
      ],
      depositTokenAddress
    );
    
    // Convert amount to Wei (assuming 18 decimals)
    const amountWei = web3.utils.toWei(depositAmount, 'ether');
    
    try {
      // First approve the contract to spend tokens
      await depositTokenContract.methods.approve(contractAddress, amountWei).send({ from: userAccount });
      
      // Then deposit tokens
      await tokenExchangeContract.methods.depositTokens(amountWei).send({ from: userAccount });
      
      alert("Tokens deposited successfully!");
      updateUI();
    } catch (error) {
      console.error("Error depositing tokens:", error);
      alert("Failed to deposit tokens. See console for details.");
    }
  }
  
  // Function to claim rewards
  async function claimReward() {
    if (!userAccount || !tokenExchangeContract) return;
    
    try {
      await tokenExchangeContract.methods.claimReward().send({ from: userAccount });
      alert("Reward claimed successfully!");
      updateUI();
    } catch (error) {
      console.error("Error claiming reward:", error);
      alert("Failed to claim reward. See console for details.");
    }
  }
  
  // Function to redeem a coupon
  async function redeemCoupon() {
    if (!userAccount || !tokenExchangeContract) return;
    
    const couponCode = document.getElementById('couponCode').value;
    
    try {
      await tokenExchangeContract.methods.redeemCoupon(couponCode).send({ from: userAccount });
      alert("Coupon redeemed successfully!");
      updateUI();
    } catch (error) {
      console.error("Error redeeming coupon:", error);
      alert("Failed to redeem coupon. See console for details.");
    }
  }
  
  // Update UI with user's deposit and reward info
  async function updateUI() {
    if (!userAccount || !tokenExchangeContract) return;
    
    try {
      const userDeposit = await tokenExchangeContract.methods.deposits(userAccount).call();
      const hasClaimedReward = await tokenExchangeContract.methods.hasClaimedReward(userAccount).call();
      const minimumDeposit = await tokenExchangeContract.methods.minimumDeposit().call();
      
      document.getElementById('userDeposit').textContent = web3.utils.fromWei(userDeposit, 'ether');
      document.getElementById('hasClaimedReward').textContent = hasClaimedReward ? "Yes" : "No";
      document.getElementById('minimumDeposit').textContent = web3.utils.fromWei(minimumDeposit, 'ether');
    } catch (error) {
      console.error("Error updating UI:", error);
    }
  }
  
  // Initialize when the page loads
  window.addEventListener('load', initContract);