import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import Plugin from './utils/axios';
import axios from 'axios'
import './assets/css/global.css'
// import { far } from '@fortawesome/free-regular-svg-icons'
import { faArrowUp,faLanguage } from "@fortawesome/free-solid-svg-icons";
import { library } from "@fortawesome/fontawesome-svg-core";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import i18n from './components/language'

// axios.defaults.baseURL = 'http:/192.227.148.27:23456'
axios.defaults.baseURL = 'https://app.changenotify.net/api/'

library.add(faLanguage);

const app = createApp(App)


app.use(router);
app.use(ElementPlus);
app.use(Plugin);
app.use(i18n);
app.component("font-awesome-icon", FontAwesomeIcon)

app.mount('#app');

