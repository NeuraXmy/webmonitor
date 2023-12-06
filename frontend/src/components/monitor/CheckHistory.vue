<template>
    <div>
        <!-- <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>任务管理</el-breadcrumb-item>
            <el-breadcrumb-item :to="{ path: '/spaces' }">监控空间列表</el-breadcrumb-item>
            <el-breadcrumb-item :to="{ path: '/monitor_list' }">空间监控管理</el-breadcrumb-item>
            <el-breadcrumb-item>监控检查历史</el-breadcrumb-item>
        </el-breadcrumb> -->
        <el-card>
            <div class="common-layout">
                <el-container>
                    <el-header>
                        <el-row>
                            <el-col :span="2">
                                <div>
                                    <el-button type="primary" @click="back"><el-icon><ArrowLeft/></el-icon>返回</el-button>
                                </div>
                            </el-col>
                            <el-col :span="10">
                                <div>{{ watch_url }}</div>
                            </el-col>
                        </el-row>
                    </el-header>
                    <el-main v-loading="loading">
                        <el-timeline>
                            <el-timeline-item
                            v-for="(activity, index) in Histories"
                            :key="index"
                            :timestamp="activity.timestamp"
                            placement="top"
                            :type="activity.type"
                            >
                                <el-card>
                                    <el-collapse v-model="activeNames" @change="handleChange">
                                        <el-collapse-item :title="activity.content" :name="activity.id">
                                            <div style="width: '80%'" v-html="activity.diff"></div>
                                            <!-- <div class="history-wrapper">
                                                <div v-html="activity.diff" class="history"></div>
                                            </div> -->
                                        </el-collapse-item>
                                    </el-collapse>
                                </el-card>
                            </el-timeline-item>
                        </el-timeline>
                    </el-main>
                </el-container>
            </div>
        </el-card>
    </div>
</template>

<script>
import { ArrowLeft } from '@element-plus/icons-vue'
export default{
    
    components: { ArrowLeft },
    data(){
        return {
            Histories:[
                // {
                //     content: 'Event start',
                //     timestamp: '2018-04-15',
                //     type: 'primary',
                //     id: 1,
                //     diff: "<h1>Hello, World!</h1><p>This is an example HTML string.</p>"
                // },
                // {
                //     content: 'Approved',
                //     timestamp: '2018-04-13',
                //     type: 'primary',
                //     id: 2,
                //     diff: "<h1>Hello, World!</h1><p>This is an example HTML string.</p>"
                // },
                // {
                //     content: 'Success',
                //     timestamp: '2018-04-11',
                //     type: 'primary',
                //     id: 3,
                //     diff: "<h1>Hello, World!</h1><p>This is an example HTML string.</p>"
                // },
            ],
            watch_id:'',
            history_id:'',
            history_html:'',
            watch_url:'',
            activeNames:'',
            check_html:[]
        }
    },
    created(){
        this.getHistoryList()
    },
    methods:{
        //获取监控所有监控历史
        async getHistoryList(){
            this.watch_id = sessionStorage.getItem('watch_id')
            this.watch_url = sessionStorage.getItem('watch_url')
            // this.loading = true

            const {data: res} = await this.$axios.get('/watch/' + this.watch_id + '/histories',
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            
            // this.loading = true
            console.log(res.data.items)
            for(let i = 0; i < res.data.items.length; i++){
                this.history_id = res.data.items[i].id
                await this.getHistory()
            }
            
            // console.log(this.loading)
            for(let i = 0; i < res.data.items.length; i++){
                this.Histories.push({
                    content: res.data.items[i].check_state,
                    timestamp: res.data.items[i].check_time,
                    type: 'primary',
                    check_id: res.data.items[i].id,
                    diff: this.check_html[i].diff
                })
                console.log(this.check_html[i].diff)
                console.log(this.Histories)
            }
            // this.loading = false
            // console.log(this.loading)
        },
        //获取所有单个监控的监控信息
        async getHistory(){
            const {data: res} = await this.$axios.get('/watch/' + this.watch_id + '/history/' + this.history_id,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            console.log(res)
            this.check_html.push({
                diff: res.data.content
            })
            console.log(this.check_html)
            this.history_html = res.data.content
        },
        //返回监控页面
        back(){
            this.$router.push('/spaces')
        },
        handleChange(){
            // console.log(this.activeNames)
        }
    }
}
</script>

<style>
.history-wrapper {
    width: 80%;
}
.history{
    width: 80% !important;
    height: 100%;
}
</style>