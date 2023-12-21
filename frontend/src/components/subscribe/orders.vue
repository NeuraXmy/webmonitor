<template>
    <div>
        <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>我的订单</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-row>
                <el-table v-loading="loading" :data="OrderList" style="width: 100%">
                    <el-table-column prop="id" label="ID" width="50" />
                    <el-table-column prop="create_time" label="创建时间" width="200" />
                    <el-table-column prop="name" label="套餐名称" width="150" />
                    <el-table-column prop="period_type" label="周期" width="150" />
                    <el-table-column prop="period_check_count" label="监控总次数" width="150" />
                    <el-table-column prop="price" label="订单金额" width="150" />
                    <el-table-column prop="check_count_left" label="监控剩余次数" width="150" />
                    <!-- <el-table-column prop="edit" label="操作" width="340">
                        <template #default="scope">
                            <el-button size="small" @click="WatchEdit(scope.row)"
                            >查看详情</el-button
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
        }
    },
    created(){
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
            console.log(res)
            this.loading = false
            this.TotalPages = res.data.total
            this.OrderList = res.data.items
            for(let i = 0; i < this.OrderList.length; i++){
                this.OrderList[i].price /= 100.0
                if(this.OrderList[i].period_type === 0) this.OrderList[i].period_type = "一次性";
                else if(this.OrderList[i].period_type === 1) this.OrderList[i].period_type = "日付";
                else if(this.OrderList[i].period_type === 2) this.OrderList[i].period_type = "月付";
                else if(this.OrderList[i].period_type === 3) this.OrderList[i].period_type = "年付";
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
        }
    }
};
</script>
<style>

</style>