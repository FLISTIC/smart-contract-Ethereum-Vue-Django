<template >
  <div class="container" style="max-width:100%;min-height: 800px; padding:0;padding-bottom:5rem; background-color: rgb(54, 54, 54);padding-buttom:5rem">

    <div class="text-center" style="margin-top:2rem;margin-bottom:2rem">
     <h1>
           Создать новый аукцион
        </h1>
        <p>Всего аукционов было создано: <span>#{{ amount }}</span></p>
        <div>
          <span style="color: white">
            <!-- {{data1}} -->
          </span>
        </div>
        <hr>
    </div>
    <div class="b-row" style="padding-top:1rem">
      <div>
        
        <div>
          <label class="label" for="title">
            Название:
          </label>
          <label class="label" for="title" style="color:rgb(148, 148, 148); font-size:13px">
            Введите название аукциона
          </label>

          
          <!-- <b-form-input
            id="title"
            v-model="title"
            type="text"
            placeholder="Введите название аукциона"
          /> -->
          <input type="text" v-model="title" id="title" class="input" >
        </div>
        <div>
          <label class="label" for="startPrice">
            Стартовая цена ETH:
          </label>
          <label class="label" for="title" style="color:rgb(148, 148, 148); font-size:13px">
            Введите стартовую цену аукциона в ETH
          </label>
          <!-- <b-form-input
            id="startPrice"
            v-model="startPrice"
            type="text"
            placeholder="Введите стартовую цену аукциона в ETH"
          /> -->
          <input type="text" v-model="startPrice" id="startPrice" class="input"  >
        </div>
      </div>
    
      <div>
        <label class="label" for="Description">
          Описание аукциона:
        </label>
        <br>
        <textarea
          id="Description"
          v-model="description"
          class="input"
          style="height:150px"
        />
      </div>  
     
    <hr>
      <div>
        <button class="button bbt" 
          :variant="'primary'"
          @click="createAuction"
        >
          {{ createStatus }}
        </button>
        <img
          v-show="isLoad"
          src="https://media.giphy.com/media/2A6xoqXc9qML9gzBUE/giphy.gif"
        >
      </div>
    </div>
    
    
  <smartcontracts style="margin-top:3rem"></smartcontracts>
  </div> 
   
</template>

<script>
import axios from 'axios'
import web3 from '../contracts/web3';
import auction from '../contracts/auctionInstance';
import auctionBox from '../contracts/auctionBoxInstance';
import smartcontracts from '@/views/smartcontracts'
import PictureInput from 'vue-picture-input'
export default {
  name: 'createauction',
  components: {
      smartcontracts,
      PictureInput
    },
  data() {
    return {
      title: '',
      startPrice: '',
      description: '',
      title1: '',
      startPrice2: '',
      description3: '',
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
      createStatus: 'Создать',
    };
  },
  beforeMount() {
    // get auctionBox method: returnAllAuctions()
    auctionBox.methods
      .returnAllAuctions()
      .call()
      .then((auctions) => {
       console.log(auctions[0])
      const auctionInstance = auction(auctions[0]);
        this.amount = auctions.length;
        this.auctions=auctions; 
        return auctionInstance.methods.returnContents().call();
      })
        .then((lists) => {
          console.log(lists);
          this.auctionAddress = auctions[0];
          const auctionlists = lists;
          this.auctionCard = auctionlists;
          this.amount += 1;
        })
        .catch((err) => {
          console.log(err);
        });
  },
  
  methods: {
    createAuction() {
      // Получение адреса создателя
      web3.eth.getAccounts().then((accounts) => {
        // конвертация эфира в газ 
        const startPrice = web3.utils.toWei(this.startPrice, 'ether');
        // создание аукциона и помещение его в AuctionBlock
        this.isLoad = true;
        
        
        return auctionBox.methods.createAuction(this.title, startPrice, this.description)
          .send({ from: accounts[0] });
      }).then(() => {
        // инициализация формы
        this.isLoad = false;
        return auctionBox.methods.returnAllAuctions().call();
      }).then((auctions) => {
        const index = auctions.length - 1;
        // Получение адрвеса контракта
        this.auctionAddress = auctions[index];
        // настройка адреса для инициализации
        const auctionInstance = auction(auctions[index]);
        return auctionInstance.methods.returnContents().call();
      })
        .then((lists) => {
          //console.log(lists);
          const auctionlists = lists;
          // конвертация газа в эфир
          auctionlists[1] = web3.utils.fromWei(auctionlists[1], 'ether');
          this.auctionCard = auctionlists;
          console.log(this.auctionCard)
          // отображение созданного контракта
          this.isShow = true;
          this.amount += 1;
          console.log("works")
          //добаление аукциона в базу данных
          this.addAuction()
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async addAuction() {
            this.$store.commit('setIsLoading', true)
            await axios
                .post('/api/v1/contracts/contractsadd/', {"SmartContract":1,"name":this.title,"slug":this.translit(this.title),"description":this.description,"price":this.startPrice,"image":"","thumbnail":"","date_added":"","id_create":"","address":this.auctionAddress})
                .then(response => {
                    this.contracts = response.data
                })
                .catch(error => {
                    console.log(error)
                })

            this.$store.commit('setIsLoading', false)
        },
          translit(str)
      {
        var ru=("А-а-Б-б-В-в-Ґ-ґ-Г-г-Д-д-Е-е-Ё-ё-Є-є-Ж-ж-З-з-И-и-І-і-Ї-ї-Й-й-К-к-Л-л-М-м-Н-н-О-о-П-п-Р-р-С-с-Т-т-У-у-Ф-ф-Х-х-Ц-ц-Ч-ч-Ш-ш-Щ-щ-Ъ-ъ-Ы-ы-Ь-ь-Э-э-Ю-ю-Я-я").split("-")   
        var en=("A-a-B-b-V-v-G-g-G-g-D-d-E-e-E-e-E-e-ZH-zh-Z-z-I-i-I-i-I-i-J-j-K-k-L-l-M-m-N-n-O-o-P-p-R-r-S-s-T-t-U-u-F-f-H-h-TS-ts-CH-ch-SH-sh-SCH-sch-'-'-Y-y-'-'-E-e-YU-yu-YA-ya").split("-")   
        var res = '';
        for(var i=0, l=str.length; i<l; i++)
        { 
          var s = str.charAt(i), n = ru.indexOf(s); 
          if(n >= 0) { res += en[n]; } 
          else { if(s===' '){ res+='';} else {res += s;} } 
          } 
          return res;  
      },
    handleSubmit() {
      // конвертируется эфир в газ
      const bidPriceWei = web3.utils.toWei(this.bidPrice, 'ether');
      // возвращает адресс кошелька
      const fromAddress = web3.eth.accounts.givenProvider.selectedAddress;
      // устанавливает адресс в параметре
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
  },
};
</script>

<style>
::-webkit-scrollbar {
    width: 14px; /* ширина для вертикального скролла */
    height: 8px; /* высота для горизонтального скролла */
    background-color: rgb(45, 45, 45);
    overflow-x: hidden;
}

/* ползунок скроллбара */
::-webkit-scrollbar-thumb {
    background-color: rgb(34, 142, 93);
    
    
}

::-webkit-scrollbar-thumb:hover {
    background-color: rgb(214,214,214);
}
.bbt{
  border: none;
  background-color: rgb(34,142,93);
  color: rgb(214,214,214);
}

.bbt:hover{
  background-color: rgb(31, 104, 71);
  color: rgb(214,214,214);
}

h1,
h2,
h4,
h6,
p {
  font-weight: bold;
  color:rgb(214,214,214);
}
.label{
  color:rgb(214,214,214);
  
}
.form-control{
  background-color: rgb(45, 45, 45);
  color: wheat;
  border: 0 none black;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}

/* button {
  background-color: #fea431;
  color: white;
}
button:hover {
  background-color: white; /* Green */
 /* color: #fea431;
  border: #fea431 3px solid;
} */
img {
  width: 32px;
}
#isBid, #isFin {
  height: 32px;
  margin-top: 16px;
  margin-left: 8px;
}
.b-row{
padding-left:5rem;
padding-right:5rem;
padding-bottom: 1rem;
margin-left:4.5rem;
margin-right:4.5rem;
background-color: rgb(39, 39, 39);
border-radius: 5px;
box-shadow: 0 0 10px rgba(0,0,0,0.5);
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
.navbar{
  box-shadow: 0 0 10px rgba(0,0,0,0.5);
}
.input{
  background-color:rgb(45, 45, 45);
  border:none;
  color:white;
}
.input:active{
  background-color:rgb(45, 45, 45);
  border:none;
  color:white;
}
input::-webkit-input-placeholder { color: red; }

.placeholder{
  color:white;
}

.list-card{
  padding-bottom:3rem;
}
</style>