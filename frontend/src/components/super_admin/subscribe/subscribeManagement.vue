<template>
    <div>
        <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>套餐管理</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-row>
                <el-table v-loading="loading" :data="OrderList" style="width: 100%">
                        <el-table-column prop="id" label="ID" width="200" />
                        <el-table-column prop="cycle" label="周期" width="150" />
                        <el-table-column prop="price" label="价格" width="150" />
                        <el-table-column prop="monitor_times" label="监控次数" width="200" />
                        <el-table-column prop="edit" label="操作" width="340">
                        <template #default="scope">
                            <el-button size="small" @click="WatchEdit(scope.row)"
                            >查看详情</el-button
                            >
                        </template>
                    </el-table-column>
                </el-table>
            </el-row>
        </el-card>
    </div>
</template>

<script>
export default {
    data(){
        return {
            OrderList:[
                {
                    id:1,
                    cycle:"一次性",
                    price:10,
                    monitor_times:"200"
                },
                {
                    id:2,
                    cycle:"月付",
                    price:10,
                    monitor_times:"300"
                },
                {
                    id:3,
                    cycle:"月付",
                    price:20,
                    monitor_times:"600"
                },
                {
                    id:4,
                    cycle:"月付",
                    price:30,
                    monitor_times:"1000"
                }
            ],
            loading:false
        }
    },
    created(){
        // this.getOrderList()
    },
    methods: {
        async getOrderList(){
            this.loading = true
            const {data: res} = await this.$axios.get('/orders',
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            this.loading = false
            this.OrderList = res.data
        }
    }
};
</script>
<style>

</style>