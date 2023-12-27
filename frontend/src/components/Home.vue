<template>
    <el-container class="home-container">
      <el-header>
        <div>
            <span>{{ $t('name') }}</span>
        </div>
        <div v-if="this.okadmin == 1">
            <el-switch
                v-model="admin"
                class="ml-2"
                style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
                active-text="用户模式"
                inactive-text="管理员模式"
                @change="swap_admin"
            />
        </div>
        <div class="right-panel">
            <el-menu
                :default-active="activeIndex"
                class="el-menu-demo"
                mode="horizontal"
                :ellipsis="false"
                @select="handleSelect"
                active-text-color="#000000"
                text-color="#545c64"
            >
                <el-sub-menu index="2">
                    <template #title><font-awesome-icon icon="fas fa-language" /></template>
                    <el-menu-item index="2-1">English</el-menu-item>
                    <el-menu-item index="2-2">简体中文</el-menu-item>
                </el-sub-menu>
                <el-menu-item index="1">
                    <el-button type="primary" plain @click="logout">{{$t('back')}}</el-button>
                </el-menu-item>
            </el-menu>
        </div>
        
      </el-header>
      <el-container>
        <el-aside width="200px">
            <el-menu
                active-text-color="#ffd04b"
                background-color="#545c64"
                class="el-menu-vertical-demo"
                default-active="2"
                text-color="#fff"
                :router="true"
            >
                <!-- <el-sub-menu index="1">
                <template #title>
                    <span><el-icon><Menu /></el-icon>任务管理</span>
                </template> -->
                <el-menu-item index="spaces">
                    <span><el-icon><Compass /></el-icon>{{ $t('home.space') }}</span>
                </el-menu-item>
                <el-menu-item index="monitors">
                    <span><el-icon><Monitor /></el-icon>{{ $t('home.monitor') }}</span>
                </el-menu-item>
                <el-menu-item index="SubscribePackage">
                    <span><el-icon><ShoppingBag /></el-icon>{{ $t('home.subscribe') }}</span>
                </el-menu-item>
                <el-menu-item index="orders">
                    <span><el-icon><ShoppingCart /></el-icon>{{ $t('home.order') }}</span>
                </el-menu-item>
                <el-menu-item index="tools">
                    <span><el-icon><Tools /></el-icon>{{ $t('home.tool') }}</span>
                </el-menu-item>
                <!-- </el-sub-menu> -->
            </el-menu>
        </el-aside>
        <el-main>
            <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
</template>


<script>
import { Menu,Compass,Tools,Monitor,ShoppingBag,ShoppingCart } from '@element-plus/icons-vue'
import Cookies from 'universal-cookie';

export default{
    components: { Menu,Compass,Tools,Monitor,ShoppingBag,ShoppingCart },
    data(){
        return {
            okadmin:1,
            admin:false
        }
    },
    created(){
        this.okadmin = sessionStorage.getItem('role')
        console.log(this.okadmin)
    },
    methods:{
        logout(){
            window.sessionStorage.clear()
            this.$router.push('/login')
            this.setCookie("verify_authenticity_token", "")
        },
        setCookie(name , value){
            // var date= new Date(); 
            // date.setDate(date.getDate()+time); 
            // document.cookie = name + "=" + value + ";expires=" + date; 
            // console.log(document.cookie)
            const cookies = new Cookies();
                const options = {
                secure: true,
                sameSite: 'none',
                };
            cookies.set(name, value, options);
        },
        swap_admin(){
            this.$router.push('/admin')
        },
        handleSelect(val){
            // console.log(val)
            if(val === "2-1") this.$i18n.locale = 'en'
            else this.$i18n.locale = 'zh'
        },
        activeIndex(){
            
        }
    }
}

</script>
<style less="less" scoped>
.home-container{
    height: 100%;
}
.el-header{
    display: flex;
    background-color: #409EFF;
    align-items: center;
    justify-content: space-between;
    color: #fff;
    font-size: 20px;
}
.el-aside{
    background-color: #303133;

}
.el-main{
    background-color: #E4E7ED;
}
.right-panel{
    /* margin-left: -7.5px; */
}
.el-menu-demo{
    background-color: #409EFF;
    /* text-color:#fff;
    active-text-color:#fff; */
}

</style>