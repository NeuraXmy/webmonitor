<template>
    <div>
        <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/home' }">{{ $t('orders.home') }}</el-breadcrumb-item>
            <el-breadcrumb-item :to="{ path: '/orders' }">{{ $t('orders.myOrders') }}</el-breadcrumb-item>
            <el-breadcrumb-item>{{ $t('orders.payment_detail') }}</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-row>
                <el-table v-loading="loading" :data="PayList" style="width: 100%">
                    <el-table-column prop="id" label="id" width="100" />
                    <el-table-column prop="name" :label="$t('orders.nickname')" width="150" />
                    <el-table-column prop="create_time" :label="$t('orders.createTime')" width="200" />
                    <el-table-column prop="status" :label="$t('orders.payment_state')" width="200" >
                        <template #default="scope">
                            <span v-if="scope.row.status === 2">{{ $t('orders.payment_success') }}</span>
                            <span v-else>{{ $t('orders.payment_cancel') }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="pay_time" :label="$t('orders.pay_time')" width="200" />
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
</template>

<script>
export default {
    data(){
        return {
            PayList:[
                // {
                //     id:123,
                //     state:"已完成",
                //     create_time:"2023/12/17"
                // }
            ],
            loading:false,
            TotalPages: 10,
            queryPage: {
                page:1,
                size:10
            },
            package_id:null
        }
    },
    created(){
        this.getPayment()
    },
    methods: {
        async getPayment(){
            this.package_id = sessionStorage.getItem('package_id')
            this.loading = true
            const {data: res} = await this.$axios.get('/package/' + this.package_id + '/payment',
            {
                // params: this.queryPage,
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            // console.log(res)
            this.loading = false
            this.TotalPages = res.data.total
            this.PayList = res.data.items
        },
    }
};
</script>