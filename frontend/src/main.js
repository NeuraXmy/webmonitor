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

app.mount('#app');

document.addEventListener("drop", function(event) {
    event.preventDefault();
    
    const text = event.dataTransfer.getData("../embed/inject.js");
    console.log(text);
    const url = window.location.href; // 获取当前页面的URL
    
    // 使用Chrome浏览器提供的API将书签添加到书签栏
    chrome.bookmarks.create({
      title: text,
      url: url
    });
  });
