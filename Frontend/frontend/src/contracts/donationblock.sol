
pragma solidity 0.5.3;
import "https://github.com/Carlos-RWI/SafeMath.sol/blob/master/SafeMath.sol";

contract DonationBlock{
    
    Donation[] public donations; 
   
    function createDonation (
        string memory _title,
        uint _requiredamount,
        string memory _description
        ) public{
        // устанавливаем новый экземпляр
        Donation newDonation = new Donation(msg.sender, _title, _requiredamount, _description);
        // помещаем адрес доаната в массив донатов
        donations.push(newDonation);
    }
    
    function returnAlldonations() public view returns(Donation[] memory){
        return donations;
    }
}

contract Donation {
    
    using SafeMath for uint256;
    
    address payable private owner; 
    string title;
    uint requiredamount;
    string description;

    enum State{Default, Running, Finalized}
    State public donationstate;

    uint public Sum;
    address payable public SumBidder;
    mapping(address => uint) public bids;
    
    /** @dev constructor to creat an Donation
      * @param _owner who call createDonation() in DonationBlock contract
      * @param _title the title of the Donation
      * @param _requiredamount the start price of the Donation
      * @param _description the description of the Donation
      */
      
    constructor(
        address payable _owner,
        string memory _title,
        uint _requiredamount,
        string memory _description
        
        ) public {
        // initialize Donation
        owner = _owner;
        title = _title;
        requiredamount = _requiredamount;
        description = _description;
        donationstate = State.Running;
    }
    
    modifier notOwner(){
        require(msg.sender != owner);
        _;
    }
    
    /** @dev Function to place a bid
      * @return true
      */
    
    function placeBid() public payable notOwner returns(bool) {
        require(donationstate == State.Running);
        require(msg.value > 0);
        uint currentBid = bids[msg.sender].add(msg.value);
        bids[msg.sender] = currentBid;
        Sum= currentBid;
        SumBidder = msg.sender;
        
        return true;
    }
    
    function finalizeDonation() public{
        //the owner and bidders can finalize the Donation.
        require(msg.sender == owner || bids[msg.sender] > 0);
        
        address payable recipiant;
        uint value;
        
        // owner can get Sum
        if(msg.sender == owner){
            recipiant = owner;
            value = Sum;
        }
        // SumBidder can get no money
        else {
            recipiant = SumBidder;
            value = 0;
        }
        
        // initialize the value
        bids[msg.sender] = 0;
        recipiant.transfer(value);
        donationstate = State.Finalized;
    }
    
    /** @dev Function to return the contents od the Donation
      * @return the title of the Donation
      * @return the start price of the Donation
      * @return the description of the Donation
      * @return the state of the Donation 
      */    
    
    function returnContents() public view returns(        
        string memory,
        uint,
        string memory,
        State
        ) {
        return (
            title,
            Sum,
            description,
            donationstate
        );
    }
}