import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import Register from '../components/Register.vue'
import Admin from '../components/Admin.vue'
import Welcome from '../components/Welcome.vue'
import Monitor from '../components/monitor/Monitor.vue'
import MonitorManage from '../components/monitor/MonitorManage.vue'
import SelectMonitor from '../components/monitor/SelectMonitor.vue'
// import ElementPlus from 'element-plus';
// import '../assets/css/global.css'

const routes = [
    { 
        path: '/',
        component: Login,
        hidden: true
    },
    { 
        path: '/login',
        component: Login,
        hidden: true
    },
    { 
        path: '/home',
        component: Home,
        hidden: true,
        redirect: '/welcome',
        children:[
            {path: '/welcome', component: Welcome },
            {path: '/monitor_list', component: Monitor },
            {path: '/monitor', component: MonitorManage }
            // ,
            // {path: '/select_monitor', component: SelectMonitor }
        ]
    },
    { 
        path: '/select_monitor',
        component: SelectMonitor,
        hidden: true
    },
    { 
        path: '/register',
        component: Register,
        hidden: true
    },
    { 
        path: '/admin',
        component: Admin,
        hidden: true
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;