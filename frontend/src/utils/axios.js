import axios from 'axios';
import qs from 'qs';

const plugin = {
  install(app) {
    app.config.globalProperties.$axios = axios;
    app.config.globalProperties.$qs = qs;
  },
};

export default plugin;
