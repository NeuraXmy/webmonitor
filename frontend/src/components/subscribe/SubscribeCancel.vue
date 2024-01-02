<template>
    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
        <div style="flex: 1;"></div>
        <span class="active"><el-icon size="100px"><Close /></el-icon>支付失败！</span>
        <div style="flex: 1; display: flex; justify-content: center; align-items: center;">
            <div style="margin-top: 20px;">
                <el-button type="primary" @click="Re_order()">重新下单</el-button>
                <el-button type="primary" @click="back_home()">返回主页</el-button>
            </div>
            
        </div>
    </div>
</template>

<script>
import { Close } from '@element-plus/icons-vue'
export default{
    components: { Close },
    methods: {
        back_home(){
            this.$router.push('/home')
        },
        Re_order(){
            this.$router.push('/SubscribePackage')
        }
    }
}

</script>
<style>
.active{
    margin-top: 100px;
    font-size: 30px;
}
</style>