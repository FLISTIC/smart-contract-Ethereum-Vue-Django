<template>
    <div class="page-SmartContract">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h2 class="is-size-2 has-text-centered">{{ SmartContract.name }}</h2>
            </div>

            <contractBox 
                v-for="contract in SmartContract.contracts"
                v-bind:key="contract.id"
                v-bind:contract="contract" />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

import contractBox from '@/components/contractBox'

export default {
    name: 'SmartContract',
    components: {
        contractBox
    },
    data() {
        return {
            SmartContract: {
                contracts: []
            }
        }
    },
    mounted() {
        this.getSmartContract()
    },
    watch: {
        $route(to, from) {
            if (to.name === 'SmartContract') {
                this.getSmartContract()
            }
        }
    },
    methods: {
        async getSmartContract() {
            const SmartContractSlug = this.$route.params.SmartContract_slug

            this.$store.commit('setIsLoading', true)

            axios
                .get(`/api/v1/contracts/${SmartContractSlug}/`)
                .then(response => {
                    this.SmartContract = response.data

                    document.title = this.SmartContract.name + ' | Djackets'
                })
                .catch(error => {
                    console.log(error)

                    toast({
                        message: 'Что-то пошло не так. Пожалуйста, попробуйте еще раз.',
                        type: 'is-danger',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'bottom-right',
                    })
                })

            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>