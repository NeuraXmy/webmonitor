import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import Register from '../components/Register.vue'
import Admin from '../components/Admin.vue'
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