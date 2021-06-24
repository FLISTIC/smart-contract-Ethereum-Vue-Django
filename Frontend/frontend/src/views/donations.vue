<template>
<div class=" row" >
    <div id="all"  class="col-sm">
        <h1 style="padding-left:6rem">Все донаты</h1>
    <div v-for="name in names" :key="name" >
            <button class="button butc"  :variant="'primary'" @click="viewsdonation(name)" >{{ name }}</button>
    </div>
    </div>
    <div class="col-sm">
    <div v-show="isShow" class='list-card '>
      <h1 class="text-center" style="margin-top:2rem;margin-bottom:2rem">
           Задонатить
        </h1>
      <b-card-group
        columns
        class="mb-2 out_arr"
      >
      <hr>
          <p class="card-text, mt-3">
            Название: {{ donationCard[0] }}
          </p>
          <p class="card-text, mt-3">
            Сумма сборов: {{ donationCard[1] }} ETH
          </p>
          <p class="card-text, mt-3">
            Описание: {{ donationCard[2] }}
          </p>
          <p class="card-text, mt-3">
            Количество учатсников: {{ bidders }}
          </p>
          <div>
            <form @submit.prevent="handleSubmit()">
              <b-input-group>
                <input class="input"
                  v-model="bidPrice"
                />
                <b-input-group-append>
                  <button style="border: none;margin-top:0.5rem;background-color: rgb(34,142,93); color: #fff" class="btn">Задонатить</button>
                  <img
                    v-show="isBid"
                    id="isBid"
                    src="https://media.giphy.com/media/2A6xoqXc9qML9gzBUE/giphy.gif"
                  >
                </b-input-group-append>
              </b-input-group>
            </form>
          </div>
          <b-button
            style="border: none;margin-top:0.5rem;background-color: rgb(34,142,93); color: #fff"
            class="mt-3 btn"
            variant="outline-success"
            @click="handleFinalize()"
          >
            {{ finalizeStatus }}
          </b-button>
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

<script>
import web3 from '../contracts/web3';
import donation from '../contracts/donationInstance';
import donationBlock from '../contracts/donationBlockInstance';

export default {
    
  name: 'donations',
  
  data() {
    return {
      title: '',
      startPrice: '',
      description: '',
      amount: 0,
      donationCard: [],
      donationCardDev: [],
      isShow: false,
      isLoad: false,
      isBid: false,
      isFin: false,
      bidPrice: '',
      donationAddress: '',
      bidders: 0,
      finalizeStatus: 'Закрыть донат кошелек',
      createStatus: 'подробнее',
      names:[],
      t:[],
      h: [],
      mas: '',
      count: 0,
    };
  },
  methods: {
    
    viewsdonation(name) {
        // this.isShow = true;
        this.donation = name;
        console.log("HEEEEEEEEEEEEEEEEEY",name);
        const donationInstance = donation(name);
        console.log(donationInstance);
        donationInstance.methods.returnContents().call().then((lists)=>{console.log(lists[0]);
        const donationlists = lists;
          // convert 'wei' to 'ether'
          donationlists[1] = web3.utils.fromWei(donationlists[1], 'ether');
          this.donationCard = donationlists;
          // show up the donation at the bottom of the page
          this.isShow = true; 
          });
    },
    lootmass(mas,count){
        console.log("nice work!");
        this.mass[count]=mas;
        return this.mass;
    },
    handleSubmit() {
      // конвертируется эфир в газ
      const bidPriceWei = web3.utils.toWei(this.bidPrice, 'ether');
      // возвращает адресс кошелька
      const fromAddress = web3.eth.accounts.givenProvider.selectedAddress;
      // устанавливает адресс в параметре
      this.donationAddress = this.donation;
      const selecteddonation = donation(this.donationAddress);
      this.isBid = true;
      // placeBid in donation contract
      selecteddonation.methods
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
        const selecteddonation = donation(this.donationAddress);
        this.isFin = true;
        // finalizedonation in donation contract
        selecteddonation.methods
          .finalizedonation()
          .send({ from: accounts[0] })
          .then(() => {
            this.isFin = false;
            this.finalizeStatus = 'finalized';
          });
      });
    },
    

  },

  beforeMount() {
    // get donationBlock method: returnAlldonations()
    donationBlock.methods 
      .returnAlldonations()
      .call()
      .then( async (donations) => {
        console.log(donations);
        // set the amount of donations
        this.names = donations;
        this.amount = donations.length;
        // for (var i=0;i<donations.length;i++){
        //   const donationInstance = donation(donations[i]);
        //   console.log(i);
        //   // await new Promise(r => setTimeout(r, 50));
        //   donationInstance.methods.returnContents().call().then((lists)=>{ 
        //     this.names[i]= lists[0];
        //     console.log(i+this.names[i]);
        //   // this.mass[i]=lists[i];
        //   // this.mass = lootmass(lists[i],i);
        //   // console.log(i);
        //   // if(i == 10){
        //   //   console.log("heeeeey");
        //   //   console.log(this.mass[i]);
        //   // }
        //   });
        // }
        // await new Promise(r => setTimeout(r, 100));
        // console.log(this.names);
        // this.t= this.names;
        // console.log('hey');
        // const donationInstance = donation(donations[0]);
        // this.names = donations;
        // const t = donationInstance.methods.returnContents().call();
        // console.log(t);
        // for(var i=0; i<donations.length; i++){
    
        // const donationInstance = donation(donations[i]);
        // donationInstance.methods.returnContents().call().then((lists)=>{ this.title[i] = lists[0]; console.log(this.title[i]);});
        // }
        // console.log(this.title);

        
        // // this.names[0] = donationInstance.methods.returnContents().call().then((lists)=>{const mass = lists; return mass;});
        // // console.log(this.names[0]);
        // // console.log(this.names[0].then((lists)=>{const tt = lists; this.t=tt; console.log(tt)}));
        // this.t[i] = donationInstance;
        // }
        // // console.log(this.t[0]);
        // for(var i=0;i<15;i++){
        //     t[i].methods.returnContents().call().then((lists)=>{this.names[i] = lists;console.log(this.names[i])});
        //     console.log(i);
        // }
        
      });
     //console.log(this.names);
    // }).then((sizes)=> {
    //     this.sizes= sizes;
    // });
    
  },
  prpr(){
console.log("///////////////////");
  },
    createdonation() {
      // get accounts
      web3.eth.getAccounts().then((accounts) => {
        // convert 'ether' to 'wei'
        const startPrice = web3.utils.toWei(this.startPrice, 'ether');
        // createdonation in donationBlock contract
        this.isLoad = true;
        return donationBlock.methods.createdonation(this.title, startPrice, this.description)
          .send({ from: accounts[0] });
      }).then(() => {
        // initialize forms
        this.isLoad = false;
        this.title = '';
        this.startPrice = '';
        this.description = '';
        // get the previous donation
        return donationBlock.methods.returnAlldonations().call();
      }).then((donations) => {
        const index = donations.length - 1;
        //console.log(donations[index]);
        // get the contract address of the previous donation
        this.donationAddress = donations[index];
        // set the address as the parameter
        const donationInstance = donation(donations[index]);
        
        //console.log(donationInstance);
        //console.log(donation(this.donationAddress));
        return donationInstance.methods.returnContents().call();
      })
        .then((lists) => {
          //console.log(lists);
          const donationlists = lists;
          // convert 'wei' to 'ether'
          donationlists[1] = web3.utils.fromWei(donationlists[1], 'ether');
          this.donationCard = donationlists;
          // show up the donation at the bottom of the page
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
      this.donationAddress = donations[0];
      const selecteddonation = donation(this.donationAddress);
      this.isBid = true;
      // placeBid in donation contract
      selecteddonation.methods
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
        const selecteddonation = donation(this.donationAddress);
        this.isFin = true;
        // finalizedonation in donation contract
        selecteddonation.methods
          .finalizedonation()
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
.butc{
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
   padding-bottom: 3rem;
}
.col-sm{
    background-color: rgb(39,39,39);
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0,0,0,0.5);
    margin-top: 3rem;
    margin-left: 5rem;
    padding-bottom: 1rem;
    
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
box-shadow: 0 0 10px rgba(0,0,0,0.5);
}
.btn-primary{
    background-color:rgb(39,39,39);
    border:none;
}

</style>
