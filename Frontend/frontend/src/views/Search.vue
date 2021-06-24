<template>
    <div class="page-search">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Search</h1>

                <h2 class="is-size-5 has-text-white">Поиск по названию: "{{ query }}"</h2>
            </div>

            <contractBox 
                v-for="contract in contracts"
                v-bind:key="contract.id"
                v-bind:contract="contract" />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import contractBox from '@/components/contractBox.vue'

export default {
    name: 'Search',
    components: {
        contractBox
    },
    data() {
        return {
            contracts: [],
            query: ''
        }
    },
    mounted() {
        document.title = 'Search | Djackets'

        let uri = window.location.search.substring(1)
        let params = new URLSearchParams(uri)

        if (params.get('query')) {
            this.query = params.get('query')

            this.performSearch()
        }
    },
    methods: {
        async performSearch() {
            this.$store.commit('setIsLoading', true)

            await axios
                .post('/api/v1/contracts/search/', {'query': this.query})
                .then(response => {
                    this.contracts = response.data
                })
                .catch(error => {
                    console.log(error)
                })

            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>