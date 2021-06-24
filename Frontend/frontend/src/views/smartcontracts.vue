<template>

<div class="row" >
  
    <div class="col-sm">
        <h1 style="padding-left:6rem">Все аукционы</h1>
    <div class="layer">
      <div class="routing-left">
    <div v-for="name in names" :key="name" >
            <button class="button butc"  :variant="'primary'" @click="viewsauction(name)" >{{ name }}</button>
      </div>
      </div>
    </div>
    </div>
    
    <div class="col-sm" >
    <div v-show="isShow" class='list-card ml-3'>
      <h1 class="text-center" style="margin-top:2rem;margin-bottom:2rem">
           Сделайте свою ставку
        </h1>
      <b-card-group
        columns
        class="mb-2  out_arr"
      >
          <hr>
          <p class="card-text, mt-3">
            Название: {{ auctionCard[0] }}
          </p>
          <p class="card-text, mt-3">
            Стартовая цена: {{ auctionCard[1] }} ETH
          </p>
          <p class="card-text, mt-3">
            Описание: {{ auctionCard[2] }}
          </p>
          <p class="card-text, mt-3">
            Количество учатсников: {{ bidders }}
          </p>
          <div>
            <form @submit.prevent="handleSubmit()">
                <input class="input"
                  v-model="bidPrice"
                />
            </form>
          </div>
          <button @click="handleSubmit()" class="button bbt mt-2">Сделать ставку</button>
          <img
                    v-show="isBid"
                    id="isBid"
                    src="https://media.giphy.com/media/2A6xoqXc9qML9gzBUE/giphy.gif"
                  >
          <button
            class="button bbt mt-2"
            style="margin-left: 0.25rem;"
            variant="outline-success"
            @click="handleFinalize()"
          >
            {{ finalizeStatus }}
          </button>
          <img
            v-show="isFin"
            id="isFin"
            src="https://media.giphy.com/media/2A6xoqXc9qML9gzBUE/giphy.gif"
          >
      </b-card-group>
      
    </div>
    </div>
</div>
</template>

<script lang=js>
import web3 from '../contracts/web3';
import auction from '../contracts/auctionInstance';
import auctionBox from '../contracts/auctionBoxInstance';
import axios from 'axios'
export default {
    
  name: 'example-1',
  
  data() {
    return {
      title: '',
      startPrice: '',
      description: '',
      amount: 0,
      auctionCard: [],
      auctionCardDev: [],
      isShow: false,
      isLoad: false,
      isBid: false,
      isFin: false,
      bidPrice: '',
      auctionAddress: '',
      bidders: 0,
      finalizeStatus: 'Завершить аукцион',
      createStatus: 'подробнее',
      names:[],
      t:[],
      h: [],
      mas: '',
      count: 0,
    };
  },
  methods: {
    
    viewsauction(name) {
        // this.isShow = true;
        this.auction = name;
        console.log("HEEEEEEEEEEEEEEEEEY",name);
        const auctionInstance = auction(name);
        console.log(auctionInstance);
        auctionInstance.methods.returnContents().call().then((lists)=>{console.log(lists[0]);
        const auctionlists = lists;
          // convert 'wei' to 'ether'
          auctionlists[1] = web3.utils.fromWei(auctionlists[1], 'ether');
          this.auctionCard = auctionlists;
          // show up the auction at the bottom of the page
          this.isShow = true; 
          });
    },
    async addbd() {
            this.$store.commit('setIsLoading', true)
            console.log("///////////////")
            await axios
                .post('/api/v1/contracts/participation/', {"user":"","address":this.auction})
                .then(response => {
                    this.contracts = response.data
                })
                .catch(error => {
                    console.log(error)
                })

            this.$store.commit('setIsLoading', false)
        },
    handleSubmit() {
      // конвертируется эфир в газ
      const bidPriceWei = web3.utils.toWei(this.bidPrice, 'ether');
      // возвращает адресс кошелька
      const fromAddress = web3.eth.accounts.givenProvider.selectedAddress;
      // устанавливает адресс в параметре
      this.auctionAddress = this.auction;
      const selectedAuction = auction(this.auctionAddress);
      this.isBid = true;
      // placeBid in Auction contract
      selectedAuction.methods
        .placeBid()
        .send({
          from: fromAddress,
          value: bidPriceWei,
        })
        .then(() => {
          this.isBid = false;
          // increase the number of bidders
          this.bidders += 1;
          this.bidPrice = '';
          this.addbd()
        });
    },
    
    handleFinalize() {
      // get accounts
      web3.eth.getAccounts().then((accounts) => {
        // set the address as the parameter
        const selectedAuction = auction(this.auctionAddress);
        this.isFin = true;
        // finalizeAuction in Auction contract
        selectedAuction.methods
          .finalizeAuction()
          .send({ from: accounts[0] })
          .then(() => {
            this.isFin = false;
            this.finalizeStatus = 'finalized';
          });
      });
    },
    

  },
  

  beforeMount() {
    // get auctionBox method: returnAllAuctions()
    auctionBox.methods 
      .returnAllAuctions()
      .call()
      .then( async (auctions) => {
        console.log(auctions);
        // set the amount of auctions
        this.names = auctions;
        this.amount = auctions.length;
      });
    
  },
  prpr(){
console.log("///////////////////");
  },
    createAuction() {
      toast({
                message: 'The contract was added to the cart',
                type: 'is-success',
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: 'bottom-right',
            })
      // get accounts
      web3.eth.getAccounts().then((accounts) => {
        // convert 'ether' to 'wei'
        const startPrice = web3.utils.toWei(this.startPrice, 'ether');
        // createAuction in AuctionBox contract
        this.isLoad = true;
        return auctionBox.methods.createAuction(this.title, startPrice, this.description)
          .send({ from: accounts[0] });
      }).then(() => {
        // initialize forms
        this.isLoad = false;
        this.title = '';
        this.startPrice = '';
        this.description = '';
        // get the previous auction
        return auctionBox.methods.returnAllAuctions().call();
      }).then((auctions) => {
        const index = auctions.length - 1;
        //console.log(auctions[index]);
        // get the contract address of the previous auction
        this.auctionAddress = auctions[index];
        // set the address as the parameter
        const auctionInstance = auction(auctions[index]);
        
        //console.log(auctionInstance);
        //console.log(auction(this.auctionAddress));
        return auctionInstance.methods.returnContents().call();
      })
        .then((lists) => {
          //console.log(lists);
          const auctionlists = lists;
          // convert 'wei' to 'ether'
          auctionlists[1] = web3.utils.fromWei(auctionlists[1], 'ether');
          this.auctionCard = auctionlists;
          // show up the auction at the bottom of the page
          this.isShow = true;
          this.amount += 1;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    
    handleSubmit() {
      // конвертируется эфир в газ
      const bidPriceWei = web3.utils.toWei(this.bidPrice, 'ether');
      // возвращает адресс кошелька
      const fromAddress = web3.eth.accounts.givenProvider.selectedAddress;
      // устанавливает адресс в параметре
      this.auctionAddress = auctions[0];
      const selectedAuction = auction(this.auctionAddress);
      this.isBid = true;
      // placeBid in Auction contract
      selectedAuction.methods
        .placeBid()
        .send({
          from: fromAddress,
          value: bidPriceWei,
        })
        .then(() => {
          this.isBid = false;
          // increase the number of bidders
          this.bidders += 1;
          this.bidPrice = '';
        });
    },
    
    handleFinalize() {
      // get accounts
      web3.eth.getAccounts().then((accounts) => {
        // set the address as the parameter
        const selectedAuction = auction(this.auctionAddress);
        this.isFin = true;
        // finalizeAuction in Auction contract
        selectedAuction.methods
          .finalizeAuction()
          .send({ from: accounts[0] })
          .then(() => {
            this.isFin = false;
            this.finalizeStatus = 'finalized';
          });
      });
    },
  
};

</script>

<style >
.input{
  background-color:rgb(45, 45, 45);
  border:none;
  color:white;
}
.butc{
  padding-left: 0.25rem;
  margin-top: 0.25rem;
  background-color:rgb(39, 39, 39);
  border: none;
  color:rgb(34, 142, 93);
}

.butc:hover{
  background-color:rgb(53, 53, 53);
  color:rgb(34, 142, 93);
}



.row{
   margin-right: 4.5rem;
   margin-top:2rem;
}
::-webkit-scrollbar {
    width: 6px; /* ширина для вертикального скролла */
    height: 8px; /* высота для горизонтального скролла */
    background-color: rgb(54, 54, 54);
    
}
.routing-left{
    direction: ltr;
}
/* .col-sm {
    -webkit-box-flex: 1;
    -ms-flex: 1 0 0%;
    flex: 1 1 1%;
} */
.layer {
    overflow: scroll; /* Добавляем полосы прокрутки */
    overflow-x: hidden;
    width: 100%; /* Ширина блока */
    height: 25rem; /* Высота блока */
    padding: 5px; /* Поля вокруг текста */
    direction: rtl;
   } 
.col-sm{
    background-color: rgb(39, 39, 39);
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0,0,0,0.5);
    margin-top: 3rem;
    margin-left: 5rem;
    max-width:30%;
    padding-bottom: 1rem;
    margin-right: 5rem;
}
.namebtn{
    background-color: rgb(39, 39, 39);
     border:none;
}
.namebtn:hover{
color:green;
background-color: rgb(39, 39, 39);
border: none!important;
}
.card-row{
margin-bottom: 3rem;
padding-bottom: 1rem;
margin-left:4.5rem;
margin-right:4.5rem;
background-color: rgb(39, 39, 39);
border-radius: 5px;
/* box-shadow: 0 0 10px rgba(0,0,0,0.5); */
}
.btn-primary{
    background-color:rgb(39,39,39);
    border:none;
}

</style>
