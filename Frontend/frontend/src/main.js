import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
// import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';


// axios.defaults.baseURL = 'https://apidjackets.codewithstein.com'
axios.defaults.baseURL = 'http://127.0.0.1:8000'

createApp(App).use(store).use(router, axios).mount('#app')

createApp(App).use(BootstrapVue);

// new Vue({
//     el:'#root',
//   })
  
//   new Vue({
//     el: '#app',
//     router,
//     store,
//     components: { App },
//     template: '<App/>',
    
//   })



