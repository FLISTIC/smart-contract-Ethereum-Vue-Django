<template>
  <div class="home">
    <section class="hero is-medium is-dark mb-6">
        <div class="hero-body has-text-centered">
            <p class="title mb-2">
                Здесь вы можете создать свой Смарт-контракт
            </p>
            <p class="title mb-6">
                в экосистеме Ethereum
            </p>
            <p class="subtitle">
                Или принять участие в существующих
            </p>
        </div>
    </section>

    <div class="columns is-multiline">
      <div class="column is-12">
          <h2 class="is-size-2 has-text-centered">Все смарт-контракты</h2>
      </div>

      <contractBox 
        v-for="contract in latestcontracts"
        v-bind:key="contract.id"
        v-bind:contract="contract" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'

import contractBox from '@/components/contractBox'

export default {
  name: 'Home',
  data() {
    return {
      latestcontracts: []
    }
  },
  components: {
    contractBox
  },
  mounted() {
    this.getLatestcontracts()

    document.title = 'Home | ETH'
  },
  methods: {
    async getLatestcontracts() {
      this.$store.commit('setIsLoading', true)

      await axios
        .get('/api/v1/latest-contracts/')
        .then(response => {
          this.latestcontracts = response.data
        })
        .catch(error => {
          console.log(error)
        })

      this.$store.commit('setIsLoading', false)
    }
  }
}
</script>