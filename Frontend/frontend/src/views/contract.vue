<template>
    <div class="page-contract" style="margin-left: 7rem;margin-right: 7rem">
        <div class='list-card ml-3'>
      <h1 class="text-center" style="margin-top:2rem;margin-bottom:2rem">
           Сделайте свою ставку
        </h1>
      <b-card-group
        columns
        class="mb-2  out_arr"
      >
          <hr>
          <p class="card-text, mt-3">
            Название: {{ contract.name }}
          </p>
          <p class="card-text, mt-3">
            Стартовая цена: {{ contract.price }} ETH
          </p>
          <p class="card-text, mt-3">
            Описание: {{ contract.description }}
          </p>
          <p class="card-text, mt-3">
            Количество учатсников: 0
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
            Завершить аукцион
          </button>
          <img
            v-show="isFin"
            id="isFin"
            src="https://media.giphy.com/media/2A6xoqXc9qML9gzBUE/giphy.gif"
          >
      </b-card-group>
      
    </div>
    </div>
</template>

<script>
import axios from 'axios'
import web3 from '../contracts/web3';
import auction from '../contracts/auctionInstance';
import auctionBox from '../contracts/auctionBoxInstance';
import { toast } from 'bulma-toast'

export default {
    name: 'contract',
    data() {
        return {
            contract: {},
            quantity: 1,
            isLoad: false,
            isBid: false,
            isFin: false,
        }
    },
    mounted() {
        this.getcontract() 
    },
    methods: {
        async getcontract() {
            this.$store.commit('setIsLoading', true)

            const SmartContract_slug = this.$route.params.SmartContract_slug
            const contract_slug = this.$route.params.contract_slug

            await axios
                .get(`/api/v1/contracts/${SmartContract_slug}/${contract_slug}`)
                .then(response => {
                    this.contract = response.data
                    console.log("/////////////////")
                    console.log(this.contract.address)
                    document.title = this.contract.name + ' | ETH'
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
    //   this.auctionAddress = this.auction;
      console.log(this.contract.address)
      this.auctionAddress = this.contract.address;
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
    async addbd() {
            this.$store.commit('setIsLoading', true)
            console.log("///////////////")
            await axios
                .post('/api/v1/contracts/participation/', {"user":"","address":this.contract.address})
                .then(response => {
                    this.contracts = response.data
                })
                .catch(error => {
                    console.log(error)
                })

            this.$store.commit('setIsLoading', false)
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
    }
}
</script>