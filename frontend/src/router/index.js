import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue'
import test from '../components/test.vue'
import Home from '../components/Home.vue'
import Register from '../components/Register.vue'
import Admin from '../components/super_admin/Admin.vue'
import Welcome from '../components/Welcome.vue'
import Monitor from '../components/monitor/Monitor.vue'
import Space from '../components/monitor/space.vue'
import SelectMonitor from '../components/monitor/SelectMonitor.vue'
import CheckHistory from '../components/monitor/CheckHistory.vue'
import Activate from '../components/activate/Activate.vue'
import ActivateSuccess from '../components/activate/ActivateSuccess.vue'
import UserList from '../components/super_admin/userlist.vue'
import SpaceList from '../components/super_admin/spacelist.vue'
import MonitorList from '../components/super_admin/monitorlist.vue'
import SpacesManagement from '../components/super_admin/spacesManagement.vue'
import MonitorsManagement from '../components/super_admin/monitorsManagement.vue'
import RecycleUsers from '../components/super_admin/recycle/recycleUsers.vue'
import RecycleSpaces from '../components/super_admin/recycle/recycleSpaces.vue'
import RecycleMonitors from '../components/super_admin/recycle/recycleMonitors.vue'
import Spaces from '../components/monitor/Spaces.vue'
import Monitors from '../components/monitor/Monitors.vue'
import Tools from '../components/monitor/Tools.vue'
import PauseMonitor from '../components/email/PauseMonitor.vue'
import AdminCheckHistory from '../components/super_admin/AdminCheckHistory.vue'
import SubscribePackage from '../components/subscribe/SubscribePackage.vue'
import Orders from '../components/subscribe/orders.vue'
import subscribeManagement from '../components/super_admin/subscribe/subscribeManagement.vue'
import userSubscribe from '../components/super_admin/subscribe/userSubscribe.vue'
import Pay from '../components/subscribe/pay.vue'
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
            {path: '/space', component: Space },
            {path: '/CheckHistory', component: CheckHistory },
            {path: '/spaces', component: Spaces },
            {path: '/monitors', component: Monitors },
            {path: '/tools', component: Tools },
            {path: '/SubscribePackage', component: SubscribePackage },
            {path: '/orders', component: Orders },
            {path: '/pay', component: Pay }
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
            {path: '/RecycleMonitors', component: RecycleMonitors },
            {path: '/AdminCheckHistory', component: AdminCheckHistory },
            {path: '/subscribeManagement', component: subscribeManagement },
            {path: '/userSubscribe', component: userSubscribe }
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
    },
    { 
        path: '/test',
        component: test,
        hidden: true
    },
    { 
        path: '/pause_monitor',
        component: PauseMonitor,
        hidden: true
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;

router.beforeEach((to, from, next) => {
    if(to.path === '/login' || to.path === '/register' || to.path === '/activate' || to.path === '/activate_success' || to.path === '/select_monitor'|| to.path === '/pause_monitor') return next()
    const tokenStr = window.sessionStorage.getItem('token')
    if(!tokenStr) return next('/login')
    next()
})