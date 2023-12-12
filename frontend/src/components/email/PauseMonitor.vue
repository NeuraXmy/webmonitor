<template>
    <div style="display: flex">
        <div style="flex: 1"></div>
            <span class="active">监控信息
                <div class="describe">
                    <el-table v-loading="loading" :data="MonitorList" style="width: 100%">
                        <el-table-column prop="id" label="ID" width="50" />
                        <el-table-column prop="name" label="监控名" width="70" />
                        <el-table-column prop="url" label="网址" width="230" />
                        <el-table-column prop="last_check_time" label="检查时间" width="170" />
                        <el-table-column prop="last_check_state" label="检查状态" width="170" />
                        <!-- <el-table-column prop="last_24h_check_count" label="24小时检查次数" width="130" />
                        <el-table-column prop="last_24h_notification_count" label="24小时触发警报次数" width="155" /> -->
                        <el-table-column prop="paused" label="是否启用" width="100" >
                            <template #default="scope">
                                <el-switch
                                    v-model="scope.row.paused"
                                    :active-value="0"
                                    :inactive-value="1"
                                    active-color="#02538C"
                                    inactive-color="#B9B9B9"
                                    inline-prompt
                                    active-text="ON"
                                    inactive-text="OFF"
                                    @change="CloseMonitor(scope.row)"/>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
                <div class="actived">
                    
                </div>
            </span>
        <div style="flex: 1"></div>
    </div>

</template>
  
<script>
export default{
    data(){
        return{
            email:sessionStorage.getItem('email'),
            MonitorList:[
                //   {id:'',name:'',url:'',create_time:'',update_time:'',last_check_time:''}
            ],
            loading:false,
            token:'',
            watch_id:''
        }
    },
    created(){
        let params = new URLSearchParams(window.location.search);
        console.log(params)
        // 获取 token 参数的值
        this.token = params.get('token');
        this.getMonitor();
    },
    methods:{
        //获取监控
        async getMonitor(){
            this.MonitorList = []
            this.loading = true
            const {data: res} = await this.$axios.get('/watch/unsubscribe/mail',
            {
                params: {
                    'token': this.token
                },
                headers : {
                    'token': this.token
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            this.loading = false
            console.log(res.data)
            this.MonitorList.push(res.data)
            // console.log(this.MonitorList)
        },
        //关闭监控
        async CloseMonitor(row){
            console.log(row)
            let data = this.token
            const {data: res} = await this.$axios.post('/watch/unsubscribe/mail',data,
            {
                params: {
                    'token': this.token,
                    'pause': row.paused
                },
                headers : {
                    'token': this.token
                }
            })
            if(res.status ===200){
                this.getMonitor()
            }else{
                this.$message.error(res.msg);
            }
        }
    }
}
</script>

<style scoped>
.active{
    margin-top: 100px;
    font-size: 30px;
}
.describe{
    margin-top: 30px;
    font-size: 20px;
    text-align: center
}
.actived{
    margin-top: 10px;
    font-size: 20px;
    text-align: center
}
</style>