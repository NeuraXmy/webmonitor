<template>
  <!-- <div class="common-layout"> -->
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
                    <el-menu-item index="1-4-1">角色列表</el-menu-item>
                </el-sub-menu>
            </el-menu>
        </el-aside>
        <el-main>Main</el-main>
      </el-container>
    </el-container>
  <!-- </div> -->
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

</style>