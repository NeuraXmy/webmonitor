import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import Register from '../components/Register.vue'
import Admin from '../components/Admin.vue'
import Welcome from '../components/Welcome.vue'
import Monitor from '../components/monitor/Monitor.vue'
import MonitorManage from '../components/monitor/MonitorManage.vue'
import SelectMonitor from '../components/monitor/SelectMonitor.vue'
import Activate from '../components/activate/Activate.vue'
import ActivateSuccess from '../components/activate/ActivateSuccess.vue'
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
    },
    { 
        path: '/activate',
        component: Activate,
        hidden: true
    },
    { 
        path: '/activate_success',
        component: ActivateSuccess,
        hidden: true
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;

router.beforeEach((to, from, next) => {
    if(to.path === '/login' || to.path === '/register' || to.path === '/activate' || to.path === '/activate_success' || to.path === '/select_monitor') return next()
    const tokenStr = window.sessionStorage.getItem('token')
    if(!tokenStr) return next('/login')
    next()
})