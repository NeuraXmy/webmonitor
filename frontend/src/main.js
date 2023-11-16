import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import store from './store'
import Plugin from './utils/axios';
import axios from 'axios'
import './assets/css/global.css'
// axios.defaults.baseURL = 'http://localhost:23456'
axios.defaults.baseURL = 'http://192.227.148.27:23456/'

const app = createApp(App)


app.use(router);
app.use(ElementPlus);
app.use(store);
app.use(Plugin);

app.mount('#app');

