<template>
    <div>
        <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/home' }">{{ $t('orders.home') }}</el-breadcrumb-item>
            <el-breadcrumb-item>{{ $t('orders.myOrders') }}</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-row>
                <el-table v-loading="loading" :data="OrderList" style="width: 100%">
                    <el-table-column prop="is_expired" :label="$t('orders.package_state')" width="90" >
                        <template #default="scope">
                            <el-alert v-if="scope.row.is_expired === false"  type="success" :closable="false" show-icon />
                            <el-alert v-if="scope.row.is_expired === true"  type="error" :closable="false" show-icon />
                        </template>
                    </el-table-column>
                    <el-table-column prop="id" :label="$t('orders.id')" width="50" />
                    <el-table-column prop="create_time" :label="$t('orders.createTime')" width="200" />
                    <el-table-column prop="name" :label="$t('orders.packageName')" width="100" />
                    <el-table-column prop="period_type" :label="$t('orders.period')" width="90" >
                        <template #default="scope">
                            <span v-if="scope.row.period_type === 0">{{ $t('orders.disposable') }}</span>
                            <span v-if="scope.row.period_type === 1">{{ $t('orders.Daily_pay') }}</span>
                            <span v-if="scope.row.period_type === 2">{{ $t('orders.Monthly_pay') }}</span>
                            <span v-if="scope.row.period_type === 3">{{ $t('orders.yearly_pay') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="period_check_count" :label="$t('orders.monitorTotalCount')" width="100" />
                    <el-table-column prop="price" :label="$t('orders.orderAmount')" width="80" />
                    <el-table-column prop="check_count_left" :label="$t('orders.monitorRemainingCount')" width="120" />
                    <el-table-column prop="current_period_end_time" :label="$t('orders.current_period_end_time')" width="200" >
                        <template #default="scope">
                            <span v-if="scope.row.period_type === 0">{{ $t('orders.perpetual') }}</span>
                            <span v-if="scope.row.period_type !== 0">{{ scope.row.current_period_end_time }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="is_last_payment_failed" :label="$t('orders.payment_state')" width="100" >
                        <template #default="scope">
                            <span v-if="scope.row.is_last_payment_failed === 0 && scope.row.need_payment === 1">{{ $t('orders.payment_success') }}</span>
                            <span v-if="scope.row.is_last_payment_failed === 1 && scope.row.need_payment === 1">{{ $t('orders.payment_cancel') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="edit" :label="$t('orders.edit')" width="400">
                        <template #default="scope">
                            <el-button size="primary" link @click="getPayment(scope.row)"
                                >{{ $t('orders.detail') }}</el-button
                            >
                            <el-button v-if="scope.row.period_type !== 0" size="success" link @click="update_payment_method(scope.row)"
                                >{{ $t('orders.change_payment') }}</el-button
                            >
                            <el-button v-if="scope.row.cancel_at_next === 0 && scope.row.period_type !== 0" size="small" type="danger" @click="this.okUnsubscribe = true, this.UnsubscribeID = scope.row.id"
                                >{{ $t('orders.cancel_subscribe') }}</el-button
                            >
                            <el-button v-if="scope.row.cancel_at_next === 1 && scope.row.period_type !== 0" size="small" type="info" @click="this.okResubscribe = true, this.UnsubscribeID = scope.row.id"
                                >{{ $t('orders.recover_subscribe') }}</el-button    
                            >
                        </template> 
                    </el-table-column>
                </el-table>
                <el-pagination
                    v-model:current-page="queryPage.page"
                    v-model:page-size="queryPage.size"
                    :page-sizes="[5, 10, 20, 50]"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="TotalPages"
                    @size-change="handleSizeOrderChange"
                    @current-change="handleCurrentOrderChange"
                />
            </el-row>
        </el-card>
    </div>
    <el-dialog
        v-model="okUnsubscribe"
        width="30%"
        align-center
        >
        <span>{{ $t('orders.Unsubscribe') }}</span>
        <template #footer>
            <span class="dialog-footer">
            <el-button @click="okUnsubscribe = false">{{$t('packages.cancel')}}</el-button>
            <el-button type="primary" @click="Unsubscribe">
                {{$t('packages.confirm')}}
            </el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog
        v-model="okResubscribe"
        width="30%"
        align-center
        >
        <span>{{ $t('orders.Resubscribe') }}</span>
        <template #footer>
            <span class="dialog-footer">
            <el-button @click="okResubscribe = false">{{$t('packages.cancel')}}</el-button>
            <el-button type="primary" @click="Resubscribe">
                {{$t('packages.confirm')}}
            </el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script>
// import { loadStripe } from '@stripe/stripe-js';
export default {
    data(){
        return {
            OrderList:[
                {
                    id:123,
                    cycle:"一次性",
                    price:10,
                    order_state:"已完成",
                    create_time:"2023/12/17"
                }
            ],
            loading:false,
            TotalPages: 10,
            queryPage: {
                page:1,
                size:10
            },
            okUnsubscribe:false,
            UnsubscribeID:'',
            okResubscribe:false,
            stripe:null,
            card:null
        }
    },
    async created(){
        this.getOrderList()
    },
    methods: {
        async getOrderList(){
            this.loading = true
            const {data: res} = await this.$axios.get('/package',
            {
                params: this.queryPage,
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            // console.log(res)
            this.loading = false
            this.TotalPages = res.data.total
            this.OrderList = res.data.items
            for(let i = 0; i < this.OrderList.length; i++){
                this.OrderList[i].price /= 100.0
                //if(this.OrderList[i].period_type === 0) this.OrderList[i].period_type = "一次性";
                // else if(this.OrderList[i].period_type === 1) this.OrderList[i].period_type = "日付";
                // else if(this.OrderList[i].period_type === 2) this.OrderList[i].period_type = "月付";
                // else if(this.OrderList[i].period_type === 3) this.OrderList[i].period_type = "年付";
            }
        },
        //获得套餐页号
        handleCurrentOrderChange(val){
            this.queryPage.page = val
            this.getOrderList()
        },
        //获得套餐页数
        handleSizeOrderChange(val){
            this.queryPage.size = val
            this.getOrderList()
        },
        //退订套餐
        async Unsubscribe(){
            this.loading = true
            this.okUnsubscribe = false;
            let data = sessionStorage.getItem('token')
            const {data: res} = await this.$axios.post('/package/' + this.UnsubscribeID + '/cancel',data,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status === 200){
                // console.log(res)
                this.getOrderList()
                this.loading = false
                
            }else{
                this.$message.error(res.msg);
            }
        },
        //恢复套餐
        async Resubscribe(){
            this.loading = true
            this.okResubscribe = false;
            let data = sessionStorage.getItem('token')
            const {data: res} = await this.$axios.post('/package/' + this.UnsubscribeID + '/resume',data,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status === 200){
                // console.log(res)
                this.getOrderList()
                this.loading = false
            }else{
                this.$message.error(res.msg);
            }
        },
        getPayment(row){
            window.sessionStorage.setItem('package_id',row.id);
            this.$router.push('/pay')
        },
        //更新支付方式
        update_payment_method(row){
            window.sessionStorage.setItem('package_id',row.id);
            this.$router.push('/paymentMethod')
        },
    }
};
</script>
<style>
.el-alert {
  margin: 20px 0 0;
}
.el-alert:first-child {
  margin: 0;
}
</style>