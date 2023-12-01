import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import Register from '../components/Register.vue'
import Admin from '../components/super_admin/Admin.vue'
import Welcome from '../components/Welcome.vue'
import Monitor from '../components/monitor/Monitor.vue'
import Space from '../components/monitor/space.vue'
import SelectMonitor from '../components/monitor/SelectMonitor.vue'
import Activate from '../components/activate/Activate.vue'
import ActivateSuccess from '../components/activate/ActivateSuccess.vue'
import UserList from '../components/super_admin/userlist.vue'
import SpaceList from '../components/super_admin/spacelist.vue'
import MonitorList from '../components/super_admin/monitorlist.vue'
import SpacesManagement from '../components/super_admin/spacesManagement.vue'
import MonitorsManagement from '../components/super_admin/monitorsManagement.vue'
import RecycleUsers from '../components/super_admin/recycleUsers.vue'
import RecycleSpaces from '../components/super_admin/recycleSpaces.vue'
import RecycleMonitors from '../components/super_admin/recycleMonitors.vue'
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
            {path: '/spaces', component: Space }
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
        hidden: true,
        children:[
            {path: '/welcome', component: Welcome },
            {path: '/userlist', component: UserList },
            {path: '/spacelist', component: SpaceList },
            {path: '/monitorlist', component: MonitorList },
            {path: '/spacesManagement', component: SpacesManagement },
            {path: '/monitorsManagement', component: MonitorsManagement },
            {path: '/RecycleUsers', component: RecycleUsers },
            {path: '/RecycleSpaces', component: RecycleSpaces },
            {path: '/RecycleMonitors', component: RecycleMonitors }
        ]
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