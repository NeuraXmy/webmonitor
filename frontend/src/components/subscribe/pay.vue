<template>
    <div>
        <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/home' }">{{ $t('orders.home') }}</el-breadcrumb-item>
            <el-breadcrumb-item :to="{ path: '/orders' }">我的订单</el-breadcrumb-item>
            <el-breadcrumb-item>支付详单</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-row>
                <el-table v-loading="loading" :data="PayList" style="width: 100%">
                    <el-table-column prop="id" label="id" width="100" />
                    <el-table-column prop="name" label="昵称" width="150" />
                    <el-table-column prop="create_time" label="创建时间" width="200" />
                    <el-table-column prop="status" label="支付状态" width="100" >
                        <template #default="scope">
                            <span v-if="scope.row.status === 2">支付成功</span>
                            <span v-else>支付失败</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="pay_time" label="消费时间" width="200" />
                    <!-- <el-table-column prop="period_type" :label="$t('orders.period')" width="60" /> -->
                    <!-- <el-table-column prop="edit" label="操作" width="100">
                        <template #default="scope">
                            <el-button size="small" @click="this.okUnsubscribe = true, this.UnsubscribeID = scope.row.id"
                                >立即停用</el-button
                            >
                        </template> 
                    </el-table-column> -->
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
            console.log(res)
            this.loading = false
            this.TotalPages = res.data.total
            this.PayList = res.data.items
        },
    }
};
</script>