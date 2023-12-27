<template>
    <div>
        <el-card>
            <div class="common-layout">
                <el-container>
                    <el-header>
                        <el-row>
                            <el-col :span="2">
                                <div>
                                    <el-button type="primary" @click="back"><el-icon><ArrowLeft/></el-icon>{{$t('buttons.back')}}</el-button>
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
                                    <el-collapse v-model="activeNames" @change="handleChange(index)">
                                        <el-collapse-item :title="activity.content" :name="activity.id">
                                            <el-scrollbar>
                                                <div v-html="activity.diff"></div>
                                            </el-scrollbar>
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
            ],
            watch_id:'',
            history_id:'',
            history_html:'',
            watch_url:'',
            activeNames:'',
            check_html:[],
            loading:false
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
            this.loading = true

            const {data: res} = await this.$axios.get('/watch/' + this.watch_id + '/histories',
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            
            this.loading = false
            console.log(res.data.items)
            for(let i = 0; i < res.data.items.length; i++){
                this.Histories.push({
                    content: res.data.items[i].check_state,
                    timestamp: res.data.items[i].check_time,
                    type: 'primary',
                    check_id: res.data.items[i].id,
                    diff: ''
                })
            }
        },
        //获取所有单个监控的监控信息
        async getHistory(){
            this.loading = true
            const {data: res} = await this.$axios.get('/watch/' + this.watch_id + '/history/' + this.history_id,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            console.log(res.data)
            // this.check_html.push({
            //     diff: res.data.content
            // })
            this.loading = false
            // console.log(res.data.content)
            this.history_html = res.data.content
        },
        //返回监控页面
        back(){
            if(sessionStorage.getItem('front') === 'spaces') this.$router.push('/spaces')
            if(sessionStorage.getItem('front') === 'monitors') this.$router.push('/monitors')
        },
        async handleChange(event){
            console.log(event)
            if(this.history_id === this.Histories[event].check_id) return ;
            this.history_id = this.Histories[event].check_id
            // console.log(this.history_id)
            
            await this.getHistory()
            this.Histories[event].diff = this.history_html
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
.scrollbar-flex-content {
  display: flex;
}
</style>