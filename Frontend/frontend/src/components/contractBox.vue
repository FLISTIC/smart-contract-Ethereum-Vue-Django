<template>
    <div class="column is-3">
        <!-- <router-link v-bind:to="contract.get_absolute_url" class="button is-dark mt-4"> -->
        <div class="box scale ">
            <figure class="image mb-4">
                <img v-bind:src="contract.get_thumbnail">
            </figure>

            <h3 class="is-size-4 h3">{{ contract.name }}</h3>
            <p v-if = "contract.smartcontract_id == 1" class="is-size-6 ">Контракт: аукцион </p>
            <p v-else class="is-size-6 ">Контракт: донат</p>
            <p class="is-size-6 ">Адрес: </p>
            <a  v-bind:href="'https://rinkeby.etherscan.io/address/'+contract.address" class="is-size-7 hhr" >{{ contract.address }} </a>
            <p class="is-size-6 ">Описание: {{ contract.description }} </p>
            <p class="is-size-6 ">{{ contract.price }} ETH</p>
            <router-link v-bind:to="contract.get_absolute_url" class="button is-dark mt-4"> Участвовать </router-link>  
             
        </div>
    </div>
</template>

<script>
export default {
    name: 'contractBox',
    props: {
        contract: Object
    }
}
</script>

<style scoped>
.hhr{
    color:rgb(34, 142, 93);
}
.hhr:hover{
    color:rgb(28, 104, 70);
}
.h3{
    font-weight: bold;
    color:rgb(214,214,214);
}
.p{
    color:rgb(214,214,214);
}
.image {
    margin-top: -1.25rem;
    margin-left: -1.25rem;
    margin-right: -1.25rem;
  }
.box{
  border:none;
  border-radius: 15px;
}
.box:hover{
  border:none;
}
.box{
  background-color: rgb(39,39,39);
  
}
.scale {
        transition: 0.1s; /* Время эффекта */
        }
.scale:hover {
        transform: scale(1.07); /* Увеличиваем масштаб */
        box-shadow: 0 0 15px rgba(0,0,0,0.5); /* Параметры тени */
}
</style>