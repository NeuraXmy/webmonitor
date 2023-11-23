<template>
    <el-container class="home-container">
      <el-header>
        <div>
            <span>多模态信息舆论监控</span>
        </div>
        <el-button type="primary" plain @click="logout">退出</el-button>
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
                <el-sub-menu index="1">
                <template #title>
                    <span><el-icon><Menu /></el-icon>任务管理</span>
                </template>
                    <el-menu-item index="monitor_list">
                        <span><el-icon><Compass /></el-icon>监控空间列表</span>
                    </el-menu-item>
                </el-sub-menu>
            </el-menu>
        </el-aside>
        <el-main>
            <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
</template>


<script>
import { Menu,Compass } from '@element-plus/icons-vue'
import Cookies from 'universal-cookie';

export default{
    components: { Menu,Compass },
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

</style>