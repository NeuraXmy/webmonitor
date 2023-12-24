<template>
     <form @submit.prevent="handleSubmit">
            <div id="payment-element"/>
            <el-button native-type="submit" type="primary" round >Complete</el-button>
    </form>

</template>
  
<script>
import {toRaw} from '@vue/reactivity'
import {loadStripe} from "@stripe/stripe-js";
export default {
	data(){
		return{
		      stripe: undefined,
		      elements:undefined,
		}
	},
	methods:{
        async initStripe() {
            this.stripe = await loadStripe('pk_test_qblFNYngBkEdjEZ16jxxoWSM');
            this.elements = this.stripe.elements({
                theme: 'stripe',
                clientSecret: 'pk_test_qblFNYngBkEdjEZ16jxxoWSM',
                locale:'auto'
            })
            const paymentElement = this.elements.create("payment");
            paymentElement.mount("#payment-element");
        },
	},
	async handleSubmit(e) {
        e.preventDefault();
        let elements=toRaw(this.elements)
        let stripe=toRaw(this.stripe)
        const {error} = await stripe.confirmPayment({
            elements,
            confirmParams: {
            // Make sure to change this to your payment completion page
            return_url: "http://localhost:4242/checkout.html",
            },
            //redirect: 'if_required'如果设置redirect: 'if_required'则不跳转returnUrl
        });
        console.log(error)
    },
    created() {
        this.initStripe()
    },
}
</script>

  