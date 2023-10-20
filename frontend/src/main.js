import { createApp } from 'vue'
// import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import store from './store'
import Plugin from './utils/axios';
import axios from 'axios'
import qs from 'qs'

// const axios = require('axios');
// Vue.prototype.$axios = axios
// Vue.prototype.$qs = qs
axios.defaults.baseURL = 'http://localhost:23456'

const app = createApp(App)

app.use(router);
app.use(ElementPlus);
app.use(store);
app.use(Plugin);

app.mount('#app')
