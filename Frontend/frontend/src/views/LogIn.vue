<template>
    <div class="page-log-in">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title gth">Вход</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label class="gth">Никнейм</label>
                        <div class="control">
                            <input type="text" class="input" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label class="gth">Пароль</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button bbt">Войти</button>
                        </div>
                    </div>

                    <hr>

                    <p class="gth">Или <router-link to="/sign-up">кликинтие сюда</router-link> чтобы зарегистрироваться!</p>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'LogIn',
    data() {
        return {
            username: '',
            password: '',
            errors: []
        }
    },
    mounted() {
        document.title = 'Log In | ETH'
    },
    methods: {
        async submitForm() {
            axios.defaults.headers.common["Authorization"] = ""

            localStorage.removeItem("token")

            const formData = {
                username: this.username,
                password: this.password
            }

            await axios
                .post("/api/v1/token/login/", formData)
                .then(response => {
                    
                    const token = response.data.auth_token

                    this.$store.commit('setToken', token)
                    
                    axios.defaults.headers.common["Authorization"] = "Token " + token

                    localStorage.setItem("token", token)

                    const toPath = this.$route.query.to || '/'

                    this.$router.push(toPath)
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    } else {
                        this.errors.push('Что-то пошло не так. Пожалуйста, попробуйте еще раз')
                        
                        console.log(JSON.stringify(error))
                    }
                })
        }
    }
}
</script>


<style scoped>
.gth{
    color: rgb(214,214,214);
}
.bbt{
    background-color: rgb(34, 142, 93);
    color:rgb(214,214,214);
    border:none;
}
.bbt:hover{
    background-color: rgb(20, 121, 75);
    color:rgb(214,214,214);
    border:none;
}
</style>