<template>
    <div style="display: flex">
        <div style="flex: 1"></div>
            <span class="active">激活等待中...
                <div class="describe">
                    请检查你的邮箱({{email}})，并激活.
                </div>
                <div class="actived">
                    激活后点击 <a href="https://app.changenotify.net">链接</a> 跳转登录.
                </div>
            </span>
        <div style="flex: 1"></div>
    </div>

</template>
  
<script>
export default{
    data(){
        return{
            email:sessionStorage.getItem('email')
        }
    }
}
</script>

<style scoped>
.active{
    margin-top: 100px;
    font-size: 30px;
}
.describe{
    margin-top: 30px;
    font-size: 20px;
    text-align: center
}
.actived{
    margin-top: 10px;
    font-size: 20px;
    text-align: center
}
</style>