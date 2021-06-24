<template>
    <div class="page-my-account">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Мой аккаунт</h1>
            </div>
            <hr>
        </div>
      <div class="columns is-multiline">
            <div class="column is-12">
                <h2 class="is-size-2 has-text-centered">Смарт-контракты в которых вы участвовали</h2>
            </div>

            <contractBox 
              v-for="contract in latestcontracts"
              v-bind:key="contract.id"
              v-bind:contract="contract" />
      </div>
      <div class="columns is-multiline">
            <div class="column is-12">
                <h2 class="is-size-2 has-text-centered">Смарт-контракты созданные Вами</h2>
            </div>

            <contractBox 
              v-for="contract in usercontracts"
              v-bind:key="contract.id"
              v-bind:contract="contract" />
      </div>
    
    </div>
</template>

<script>
import axios from 'axios'
import contractBox from '@/components/contractBox'

export default {
    name: 'MyAccount',
    
    data() {
    return {
      latestcontracts: [],
      usercontracts:[]
    }
    },
    components: {
      contractBox
    },
    mounted() {
        this.getLatestcontracts()

        document.title = 'My account | ETH'

        
    },
    methods: {
        async getLatestcontracts() {
      this.$store.commit('setIsLoading', true)

      await axios
        .get('/api/v1/participation-contracts/')
        .then(response => {
          this.latestcontracts = response.data
        })
        .catch(error => {
          console.log(error)
        })
        this.getUsercontracts()
      this.$store.commit('setIsLoading', false)
    },
    async getUsercontracts() {
      this.$store.commit('setIsLoading', true)

      await axios
        .get('/api/v1/user-contracts/')
        .then(response => {
          this.usercontracts = response.data
        })
        .catch(error => {
          console.log(error)
        })

      this.$store.commit('setIsLoading', false)
    }
    }
}
</script>