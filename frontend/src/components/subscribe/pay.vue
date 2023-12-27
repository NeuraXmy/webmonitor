<template>
    <div>
      <!-- <stripe-checkout
        ref="checkoutRef"
        :pk="publishableKey"
        :session-id="sessionId"
      /> -->
      <button @click="submit">Checkout!</button>
    </div>
</template>

<script>
export default {
    data () {
        this.publishableKey = 'pk_test_51OREOcLtU7FRbXomhUG0ZaECp4eRnRKkqSLHl0AmmkmD3U1OLhyjLLTp3rgKv9m6PtrEljETNfjoPmxX4YxZ44JW00Vvlhhrj1'
        return {
            loading: false,
            sessionId: 'cs_test_a1pUvpL7vaiNbp9P253Nghz2j04bVKCSsvv6MGj7j3dae1Bp17IQwCEsEG', // session id from backend
            stripe: null
        };
    },
    created(){
        this.stripe = Stripe('pk_test_51OREOcLtU7FRbXomhUG0ZaECp4eRnRKkqSLHl0AmmkmD3U1OLhyjLLTp3rgKv9m6PtrEljETNfjoPmxX4YxZ44JW00Vvlhhrj1');
    },
    methods: {
        submit () {
            // You will be redirected to Stripe's secure checkout page
            // this.$refs.checkoutRef.redirectToCheckout();
            this.stripe.redirectToCheckout({ sessionId: 'cs_test_a1pUvpL7vaiNbp9P253Nghz2j04bVKCSsvv6MGj7j3dae1Bp17IQwCEsEG' });
        },
    },
};
</script>