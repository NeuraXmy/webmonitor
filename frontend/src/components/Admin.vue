<!-- <template>
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
                @open="handleOpen"
                @close="handleClose"
            >
                <el-sub-menu index="1">
                <template #title>
                    <el-icon><location /></el-icon>
                    <span>用户管理</span>
                </template>
                    <el-menu-item index="1-4-1">用户列表</el-menu-item>
                </el-sub-menu>
                <el-sub-menu index="2">
                <template #title>
                    <el-icon><location /></el-icon>
                    <span>权限管理</span>
                </template>
                    <el-menu-item index="1-4-2">角色列表</el-menu-item>
                    <el-menu-item index="1-4-3">权限列表</el-menu-item>
                </el-sub-menu>
            </el-menu>
        </el-aside>
        <el-main>Main</el-main>
      </el-container>
    </el-container>
</template>


<script>
export default{
    methods:{
        logout(){
            window.sessionStorage.clear()
            this.$router.push('/login')
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
    /* div{
        display: flex;
        align-items: center;
    } */
}
.el-aside{
    background-color: #303133;

}
.el-main{
    background-color: #E4E7ED;
}

</style> -->
<template>
    <div>
        <el-container class="home-container">
            <!-- header -->
            <el-header>
                <el-row>
                    <el-col :span="4">
                        <p class="system-name">多模态信息舆论监控</p>
                    </el-col>
                    <el-col :offset="12" :span="8" style="min-width: 150px">
                        <el-dropdown style="float: right; margin: 20px 10px">
                            <!-- <span class="el-dropdown-link" style="color: #fff; cursor: pointer">
                                知否君 &nbsp;&nbsp; <el-icon class="el-icon--right">
                                    <arrow-down />
                                </el-icon>
                            </span> -->
                            <!-- <template #dropdown>
                                <el-dropdown-menu>
                                    <el-dropdown-item @click.native="logout">退出系统</el-dropdown-item>
                                </el-dropdown-menu>
                            </template> -->
                            <el-button type="primary" plain @click="logout">退出</el-button>
                        </el-dropdown>
                        <!-- <el-avatar shape="square" :src="avatar" style="margin: 10px; float: right"></el-avatar> -->
                    </el-col>
                </el-row>
            </el-header>

            <el-container style="overflow: auto">
                <!-- 菜单 -->
                <el-aside>
                    <div class="toggle-button" @click="isCollapse = !isCollapse">
                        <el-icon :size="20">
                            <Expand v-if="isCollapse" />
                            <Fold v-if="!isCollapse" />
                        </el-icon>
                    </div>
                    <el-menu router :default-active="activePath" class="el-menu-vertical-demo" :collapse="isCollapse">
                        <el-menu-item index="/index" @click="saveActiveNav('/index')">
                            <el-icon>
                                <house />
                            </el-icon>
                            <span>首页</span>
                        </el-menu-item>
                        <el-sub-menu index="1">
                            <template #title>
                                <el-icon>
                                    <Setting />
                                </el-icon>
                                <span>系统设置</span>
                            </template>
                            <el-menu-item index="2-1">权限管理</el-menu-item>
                        </el-sub-menu>
                        <el-menu-item index="/user/list" @click="saveActiveNav('/user/list')">
                            <el-icon>
                                <user />
                            </el-icon>
                            <span>用户管理</span>
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <el-container>
                    <el-main>
                        <router-view></router-view>
                    </el-main>
                    <el-footer>Copyright © 2023</el-footer>
                </el-container>
            </el-container>
        </el-container>
    </div>
</template>
<script setup>
import { onBeforeMount, ref } from 'vue';
// import avatar from "../assets/img/avator.jpg"
import { useRouter } from 'vue-router'
const router = useRouter();
// 挂载 DOM 之前
onBeforeMount(() => {
    activePath.value = sessionStorage.getItem("activePath")
        ? sessionStorage.getItem("activePath")
        : "/index"
})
let isCollapse = ref(false);
let activePath = ref("");
// 保存链接的激活状态
const saveActiveNav = (path) => {
    sessionStorage.setItem("activePath", path);
    activePath.value = path;
}
const logout = () => {
    // 清除缓存
    sessionStorage.clear();
    router.push("/login");
}
</script>

<style scoped>
.home-container {
    position: absolute;
    height: 100%;
    top: 0px;
    left: 0px;
    width: 100%;
    background: #f2f3f5;
}

.el-header {
    background: #2661ef;
    padding: 0 10px;
    overflow: hidden;
}

.system-name {
    color: #fff;
    font-size: 18px;
}

.el-aside {
    background: white;
    width: auto !important;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
}

.el-footer {
    color: #cccccc;
    text-align: center;
    line-height: 60px;
}

.el-footer:hover {
    color: #2661ef;
}

.toggle-button {
    background-color: #d9e0e7;
    font-size: 18px;
    line-height: 24px;
    color: #fff;
    text-align: center;
    letter-spacing: 0.2em;
    cursor: pointer;
    color: black;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
}

.el-menu-item.is-active {
    color: #fff !important;
    font-size: 15px;
    font-weight: bold;
    background-color: #2661ef !important;
    border-radius: 2px;
    height: 50px;
    line-height: 50px;
    box-sizing: border-box;
    margin: 2px 5px 0px 2px;
}
</style>