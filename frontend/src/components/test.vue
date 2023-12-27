<template>
    <div>
      <stripe-checkout
        ref="checkoutRef"
        mode="payment"
        :pk="publishableKey"
        :line-items="lineItems"
        :success-url="successURL"
        :cancel-url="cancelURL"
        @loading="v => loading = v"
      />
      <button @click="submit">Pay now!</button>
    </div>
  </template>
  
  <script>
  import { StripeCheckout } from '@vue-stripe/vue-stripe';
  export default {
    components: {
      StripeCheckout,
    },
    data () {
      this.publishableKey = 'pk_test_51OREOcLtU7FRbXomhUG0ZaECp4eRnRKkqSLHl0AmmkmD3U1OLhyjLLTp3rgKv9m6PtrEljETNfjoPmxX4YxZ44JW00Vvlhhrj1';
      return {
        loading: false,
        lineItems: [
          {
            price: 'price_1ORFP8LtU7FRbXomTotanJyd', // The id of the one-time price you created in your Stripe dashboard
            quantity: 1,
          },
        ],
        successURL: 'http://127.0.0.1:5173/package/payment/success',
        cancelURL: 'http://127.0.0.1:5173/package/payment/error',
      };
    },
    methods: {
      submit () {
        // You will be redirected to Stripe's secure checkout page
        this.$refs.checkoutRef.redirectToCheckout();
      },
    },
  };
  </script>