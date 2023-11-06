<template>
    <div class="iframe_style">
        <el-form :model="addMonitorForm" label-width="80px" class="form_style">
            <el-form-item label="空间ID">
                <el-col :span="20">
                    <el-input v-model="space_id" placeholder="请输入空间ID"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="监控名">
                <el-col :span="20">
                    <el-input v-model="addMonitorForm.name" placeholder="请输入昵称"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="监控说明">
                <el-col :span="20">
                    <el-input v-model="addMonitorForm.desc" placeholder="请输入监控说明"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="网址">
                <el-col :span="20">
                    <el-input v-model="addMonitorForm.url" placeholder="请输入网址"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="监控元素">
                <el-col :span="20">
                    <!-- <el-input v-model="addMonitorForm.element" placeholder="请输入网址"></el-input> -->
                    <el-select v-model="value" placeholder="Select" size="large" @change="ChangeElement">
                        <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                        />
                    </el-select>
                </el-col>
                <el-col :span="20">
                    <el-input type="textarea"  v-model="addMonitorForm.include_filters"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="刷新时间">
                <el-col :span="4">
                    <!-- <el-input v-model="addMonitorForm.update_time" disabled></el-input> -->
                    <el-input v-model="addMonitorForm.time_between_check_weeks" placeholder="周"></el-input>
                </el-col>
                <el-col :span="4">
                    <el-input v-model="addMonitorForm.time_between_check_days" placeholder="天"></el-input>
                </el-col>
                <el-col :span="4">
                    <el-input v-model="addMonitorForm.time_between_check_hours" placeholder="时"></el-input>
                </el-col>
                <el-col :span="4">
                    <el-input v-model="addMonitorForm.time_between_check_minutes" placeholder="分"></el-input>
                </el-col>
                <el-col :span="4">
                    <el-input v-model="addMonitorForm.time_between_check_seconds" placeholder="秒"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="通知邮箱">
                <el-col :span="20">
                    <el-input v-model="addMonitorForm.notification_email"></el-input>
                </el-col>
            </el-form-item>
        </el-form>
        <el-button type="primary" @click="confirm_monitor">确定</el-button>
    </div>
</template>
  
<script>
export default{
    data(){
        return {
            space_id:'',
            value:'',
            options:[
                {
                    value: 'XPath',
                    label: 'XPath',
                },
                {
                    value: 'CssSelector',
                    label: 'CssSelector',
                },
                {
                    value: 'JSONPath',
                    label: 'JSONPath',
                }
            ],
            addMonitor:false,
            addMonitorForm:{
                name:'',
                desc:'',
                url:'',
                time_between_check_weeks:'',
                time_between_check_days:'',
                time_between_check_hours:'',
                time_between_check_minutes:'',
                time_between_check_seconds:'',
                notification_email:'',
                include_filters:''
            },
            Element:''
        }
    },
    mounted(){
        window.addEventListener("message", (e) => {
            // console.log(this.addMonitorForm.include_filters);
            this.Element = e.data;
            this.addMonitorForm.url=e.origin;
            if(this.value === ''){
                this.value='XPath';
                this.addMonitorForm.include_filters="xpath:" + e.data.xpath + '\n';
            }else if(this.value=== 'XPath'){
                this.addMonitorForm.include_filters = this.addMonitorForm.include_filters + "xpath:" + e.data.xpath + '\n';
            }else if(this.value === 'CssSelector'){
                this.addMonitorForm.include_filters = this.addMonitorForm.include_filters + "css:" + e.data.selector + '\n' ;
            }else if(this.value === 'JSONPath'){
                this.addMonitorForm.include_filters = this.addMonitorForm.include_filters + "json:" + e.data.jsonPath + '\n' ;
            }
            console.log(e);
        });
    },
    methods:{
        ChangeElement(){
            if(this.value === 'XPath'){
                // this.addMonitorForm.include_filters=this.Element.xpath;
            }else if(this.value === 'CssSelector'){
                // this.addMonitorForm.include_filters=this.Element.selector;
            }else if(this.value === 'JSONPath'){
                // this.addMonitorForm.include_filters=this.Element.jsonPath;
            }
        },
        async confirm_monitor(){
            let data = this.$qs.stringify(this.addMonitorForm)
            const {data: res} = await this.$axios.post('/space/'+this.space_id+'/watch',data,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            
            // this.JumpMonitorManage()
        }
    }
}
</script>
  
<style>
.iframe_style{
    background-color: aliceblue;
}
</style>