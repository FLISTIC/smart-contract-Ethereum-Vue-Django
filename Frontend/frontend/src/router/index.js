import { createRouter, createWebHistory } from 'vue-router'

import store from '../store'

import Home from '../views/Home.vue'

import contract from '../views/contract.vue'
import SmartContract from '../views/SmartContract.vue'
import Search from '../views/Search.vue'
import SignUp from '../views/SignUp.vue'
import LogIn from '../views/LogIn.vue'
import MyAccount from '../views/MyAccount.vue'
import Checkout from '../views/Checkout.vue'
import Success from '../views/Success.vue'
// import contract from '@/views/contract.vue'
import createauction from '@/views/createauction.vue'
import smartcontracts from '@/views/smartcontracts.vue'
import createdonation from '@/views/createdonation.vue'
import donations from '@/views/donations.vue'
import about from '@/views/About.vue'




const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  // {
  //   path: '/contract',
  //   name: 'contract',
  //   component: contract
  // },
  {
    path: '/createauction',
    name: 'createauction',
    component: createauction
  },
  {
    path: '/createdonation',
    name: 'createdonation',
    component: createdonation
  },
  {
    path: '/donations',
    name: 'donations',
    component: donations
  },
  {
    path: '/smartcontracts',
    name: 'smartcontracts',
    component: smartcontracts
  },
  {
    path: '/about',
    name: 'About',
    component: about
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    // component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/my-account',
    name: 'MyAccount',
    component: MyAccount,
    meta: {
        requireLogin: true
    }
  },
  {
    path: '/search',
    name: 'Search',
    component: Search
  },
  
  
  {
    path: '/:SmartContract_slug/:contract_slug',
    name: 'contract',
    component: contract
  },
  {
    path: '/:SmartContract_slug',
    name: 'SmartContract',
    component: SmartContract
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({ name: 'LogIn', query: { to: to.path } });
  } else {
    next()
  }
})

export default router
