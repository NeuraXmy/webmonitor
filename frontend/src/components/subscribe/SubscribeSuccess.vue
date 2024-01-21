<template>
    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
        <div style="flex: 1;"></div>
        <span class="active"><el-icon size="100px"><Check /></el-icon>{{ $t('orders.payment_success') }}</span>
        <div style="flex: 1; display: flex; justify-content: center; align-items: center;">
            <div style="margin-top: 20px;">
                <el-button type="primary" @click="check_order()">{{ $t('orders.view_order') }}</el-button>
                <el-button type="primary" @click="back_home()">{{ $t('orders.back_home') }}</el-button>
            </div>
            
        </div>
    </div>
</template>

<script>
import { Check } from '@element-plus/icons-vue'
export default{
    components: { Check },
    methods: {
        back_home(){
            this.$router.push('/home')
        },
        check_order(){
            this.$router.push('/orders')
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