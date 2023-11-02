import { createApp } from 'vue'
// import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import store from './store'
import Plugin from './utils/axios';
import axios from 'axios'
// import icons from './plugins/element.js'
import './assets/css/global.css'
import { Search,Plus } from '@element-plus/icons'
// import { Search,Plus } from '@element-plus/icons-vue'
import IframeMonitor from './components/monitor/IframeMonitor.vue';
import qs from 'qs'

axios.defaults.baseURL = 'http://localhost:23456'

const app = createApp(App)


// icons elementPlusIcons(app);
app.use(router);
app.use(ElementPlus);
app.use(store);
app.use(Plugin);
app.use(Search);
app.use(IframeMonitor);

app.mount('#app')
