<template>
    <div style="display: flex">
        <div style="flex: 1"></div>
            <span class="active">激活成功，将在 {{countdown}} 秒跳转登录.
            </span>
        <div style="flex: 1"></div>
    </div>
</template>
  
<script>
export default{
    data(){
        return{
            countdown:'5',
            timer: null
        }
    },
    created(){
        this.sendCode()
    },
    methods:{
        //倒计时
        sendCode(){
            this.loading();  //启动定时器
            this.timer = setInterval(() =>{
                 //创建定时器
                if(this.countdown === 0){
                    this.clearTimer();  //关闭定时器
                    this.$router.push('/login');
                }else{
                    this.loading();
                }
            },1000);
        },
        loading(){
            //启动定时器
            this.countdown--;  //定时器减1
        },
        clearTimer(){
            //清除定时器
            clearInterval(this.timer);
            this.timer = null;
        }
    },
};
</script>

<style scoped>
.active{
    margin-top: 100px;
    font-size: 30px;
}
</style>