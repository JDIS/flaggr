import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins/buefy'
import i18n from './plugins/i18n'
import axios from 'axios'
// @ts-ignore
import curlirize from 'axios-curlirize'

if (process.env.VUE_APP_DEBUG) {
  curlirize(axios)
}

axios.interceptors.request.use((config) => {
  // This appends the backend url after each call, allowing to use it
  // like that: axios.get('status') instead of axios.get(`${process.env.VUE_APP_BACKEND_URL}/status`)
  config.url = `${process.env.VUE_APP_BACKEND_URL}/${config.url}`
  if (process.env.VUE_APP_DEBUG) {
    config.headers.Authorization = `Basic ${(store as any).getters['user/creds']}`
  }

  store.dispatch('network/addRequestInProgress')

  return config;
});

axios.interceptors.response.use((config) => {
  store.dispatch('network/removeRequestInProgress')

  return config;
}, (error) => {
  // If an HTTP call results in an error, set the state accordingly.
  store.dispatch('network/setError')
  store.dispatch('network/removeRequestInProgress')
  console.log('Request error:', error)
  return Promise.reject(error)
});

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  i18n,
  render: (h) => h(App)
}).$mount('#app');
