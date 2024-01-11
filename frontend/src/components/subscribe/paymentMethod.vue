<template>
    <div>
        <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/home' }">{{ $t('orders.home') }}</el-breadcrumb-item>
            <el-breadcrumb-item :to="{ path: '/orders' }">我的订单</el-breadcrumb-item>
            <el-breadcrumb-item>更换支付</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card v-loading="loading">
            <el-container>
                <el-header>
                    <el-row>
                        <el-col :span="2">
                            <div>
                                <el-button type="primary" @click="back"><el-icon><ArrowLeft/></el-icon>{{$t('buttons.back')}}</el-button>
                            </div>
                        </el-col>
                    </el-row>
                </el-header>
                <el-main>
                    <h4>修改卡号</h4>
                    <form id="payment-form" style="margin-bottom: 20px;">
                        <div id="card-element"></div>
                        <el-button style="margin-top: 20px;" type="primary" plain @click="this.okRevisePayment = true" >保存</el-button>
                    </form>
                </el-main>
            </el-container>
        </el-card>
    </div>
    <el-dialog
        v-model="okRevisePayment"
        width="30%"
        align-center
        >
        <span>是否修改续费卡号。</span>
        <template #footer>
            <span class="dialog-footer">
            <el-button @click="okRevisePayment = false">{{$t('packages.cancel')}}</el-button>
            <el-button type="primary" @click="update_payment_method">
                {{$t('packages.confirm')}}
            </el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script>
import { ArrowLeft } from '@element-plus/icons-vue'

export default{
    components: { ArrowLeft },
    data(){
        return {
            loading:false,
            stripe:null,
            card:null,
            package_id:null,
            payment:{
                payment_method:null
            },
            okRevisePayment:false
        }
    },
    async created(){
        const stripePromise = Stripe('pk_test_51OMSmYD2kZi8DEOLsHme4tqTNhV6JZRAcF5dLsdxxGUTb6hXb4OTXXF1em8PVncr2A0Hogb7yxFQ8YNaF99gjeQ100UuAvtJLQ');
        this.stripe = await stripePromise;
        //创建卡号元素
        const elements = this.stripe.elements();
        this.card = elements.create('card');
        this.card.mount('#card-element');
    },
    methods: {
        // async handlePayment(){
        //     const form = document.getElementById('payment-form');
        //     form.addEventListener('submit', async (event) => {
        //         event.preventDefault();

        //         // Create a PaymentMethod using the card Element
        //         const { paymentMethod, error } = await this.stripe.createPaymentMethod({
        //             type: 'card',
        //             card: this.card,
        //         });

        //         if (error) {
        //             console.error(error);
        //             // alert(error.message);
        //         } else {
        //             console.log(paymentMethod.id);
        //             // Perform further actions with the paymentMethod, e.g., send it to your server
        //         }
        //     });
        // },
        async update_payment_method(){
            this.okRevisePayment = false
            this.loading = true
            const { paymentMethod, error } = await this.stripe.createPaymentMethod({
                type: 'card',
                card: this.card,
            });

            if (error) {
                // console.error(error);
                alert(error.message);
            } else {
                // console.log(paymentMethod.id);
                this.package_id = sessionStorage.getItem('package_id')
                this.payment.payment_method = paymentMethod.id
                let data = this.$qs.stringify(this.payment)
                const {data: res} = await this.$axios.put('/package/' + this.package_id + '/payment_method',data,
                {
                    headers : {
                        'token': sessionStorage.getItem('token')
                    }
                })
                // console.log(res)
                if(res.status === 200){
                    // console.log(res)
                    alert("修改成功！");
                }else{
                    this.$message.error(res.msg);
                }
            }
            this.loading = false
        },
        back(){
            this.$router.push('/orders')
        }
    }
};
</script>
<style>

</style>