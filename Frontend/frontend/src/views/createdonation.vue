<template >
  <div class="container" style="max-width:100%;min-height: 800px; padding:0; background-color: rgb(54, 54, 54);padding-buttom:5rem">
    
    <div class="text-center" style="margin-top:2rem;margin-bottom:2rem">
     <h1>
           Создать новый донат кошелек
        </h1>
        <p>Всего донатов-кошельков было создано: <span>#{{ amount }}</span></p>
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
            Название
          </label>
          <input
          class="input"  id="title" v-model="title" type="text" placeholder="Введите название донат-кошелька"/>
        </div>
        <div>
          <label class="label" for="requiredamount">
            Финальная сумма доната
          </label>
          <input
            class="input"
            id="requiredamount"
            v-model="requiredamount"
            type="text"
            placeholder="Введите сумму доната"
          />
        </div>
      </div>
    
      <div>
        <label class="label" for="Description">
          Описание доната
        </label>
        <br>
        <textarea
          id="Description"
          class="input"
          v-model="description"
          style="height:150px"
        />
      </div>   
    <hr>
      <div>
        <button class="button bbt" style="border: none;background-color: rgb(34,142,93);"
          :variant="'primary'"
          @click="createDonation"
        >
          {{ createStatus }}
        </button>
        <img
          v-show="isLoad"
          src="https://media.giphy.com/media/2A6xoqXc9qML9gzBUE/giphy.gif"
        >
      </div>
    </div>
    <!-- <div v-show="isShow" class='list-card'>
      <h1 class="text-center" style="margin-top:2rem;margin-bottom:2rem">
           Действующие донаты
        </h1>
      <hr>
      <b-card-group
        columns
        class="mb-2 out_arr"
      >
        <b-card
          :title="donationCard[0]"
          :sub-title="'Стартовая цена:' + donationCard[1] + 'ETH'"
          tag="article"
          style="max-width: 20rem; text-center"
          class="mb-2 card-row"
        >
          <hr>
          <p class="card-text, mt-3">
            Описание: {{ donationCard[2] }}
          </p>
          <p class="card-text, mt-3">
            Количество донатов: {{ bidders }}
          </p>
          <div>
            <form @submit.prevent="handleSubmit()">
              <b-input-group>
                <b-form-input
                  v-model="bidPrice"
                />
                <b-input-group-append>
                  <button style="border: none;margin-top:0.5rem;background-color: rgb(34,142,93); color: #fff" class="btn">Сделать ставку</button>
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
        </b-card>
      </b-card-group>
      
    </div> -->
    
  <donations style="margin-top:2rem"></donations>
  </div> 
   
</template>

<script>
import axios from 'axios'
import web3 from '../contracts/web3';
import donation from '../contracts/donationInstance';
import DonationBlock from '../contracts/donationBlockInstance';
import donations from '@/views/donations'
export default {
  name: 'APP',
  components: {
    donations
  },
  data() {
    return {
      title: '',
      requiredamount: '',
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
      finalizeStatus: 'Закрыть кошеле',
      createStatus: 'Создать',
    };
  },
  beforeMount() {
    // get donationBox method: returnAlldonations()
    DonationBlock.methods
      .returnAlldonations()
      .call()
      .then((donations) => {
       // console.log(donations);
      console.log(donations[0])
      const donationInstance = donation(donations[0]);
      //  console.log(donationInstance);
      
        // set the amount of donations
        this.amount = donations.length;
        this.donations=donations;

        // for(var i=0; i<donations.length; i++){
        // const donationInstance = donation(donations[i]);
        // donationInstance.methods.returnContents().call().then((lists) => {
        // const donationlists = lists;
        // donationlists[1] = web3.utils.fromWei(donationlists[1], 'ether');
        // this.donationCard = donationlists;
        // console.log(donationlists[0]);
        
        // document.getElementById("out_arr").innerHTML;
            
        //     })
        // }

        
        return donationInstance.methods.returnContents().call();
      })
        .then((lists) => {
          console.log(lists);
          this.donationAddress = donations[0];
          const donationlists = lists;
          // donationlists[1] = web3.utils.fromWei(donationlists[1], 'ether');
          
          // console.log(donationlists[0]);
          // convert 'wei' to 'ether'
          // donationlists[1] = web3.utils.fromWei(donationlists[1], 'ether');
          // this.donationCard = donationlists;
          // console.log(this.donationCard)
          // show up the donation at the bottom of the page
          // this.title = donationlists[0];
          this.donationCard = donationlists;
          
          this.isShow = true;
          this.amount += 1;
        })
        .catch((err) => {
          console.log(err);
        });
  },
  methods: {
    createDonation() {
      // get accounts
      web3.eth.getAccounts().then((accounts) => {
        // convert 'ether' to 'wei'
        const requiredamount = web3.utils.toWei(this.requiredamount, 'ether');
        // createdonation in donationblock contract
        this.isLoad = true;
        return DonationBlock.methods.createDonation(this.title, requiredamount, this.description)
          .send({ from: accounts[0] });
      }).then(() => {
        // initialize forms
        // this.isLoad = false;
        // this.title = '';
        // this.requiredamount = '';
        // this.description = '';
        // get the previous donation
        return DonationBlock.methods.returnAlldonations().call();
      }).then((donations) => {
        const index = donations.length - 1;
        //console.log(donations[index]);
        // get the contract address of the previous donation
        this.donationAddress = donations[index];
        // set the address as the parameter
        const donationInstance = donation(donations[index]);
        // const data1 = donationInstance.methods.returnContents(requiredamount).call();
        // console.log(data1);
        //console.log(donationInstance);
        //console.log(donation(this.donationAddress));
        // this.data= donationInstance.methods.returnContents().call();
        // console.log(data);
        return donationInstance.methods.returnContents().call();
      })
        .then((lists) => {
          //console.log(lists);
          const donationlists = lists;
          // convert 'wei' to 'ether'
          donationlists[1] = web3.utils.fromWei(donationlists[1], 'ether');
          this.donationCard = donationlists;
          console.log(this.donationCard)
          // show up the donation at the bottom of the page
          this.isShow = true;
          this.amount += 1;
          this.addDonate()
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async addDonate() {
            this.$store.commit('setIsLoading', true)
            console.log("///////////////")
            await axios
                .post('/api/v1/contracts/contractsadd/', {"SmartContract":2,"name":this.title,"slug":this.translit(this.title),"description":this.description,"price":this.requiredamount,"image":"","thumbnail":"","date_added":"","id_create":"","address":this.donationAddress})
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


/* #app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
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

.list-card{
  padding-bottom:3rem;
}
</style>