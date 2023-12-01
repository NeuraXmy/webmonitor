<template>
    <div class="common-layout iframe_style">
        <el-container v-loading.fullscreen.lock="fullscreenLoading">
        <el-aside width="800px">
            <div class="form_style">
                <el-form ref="MonitorRef" :rules="MonitorRules" :model="addMonitorForm" label-width="80px" class="form_style">
                    <el-form-item label="选择空间">
                        <el-col :span="20">
                            <!-- <el-input v-model="addMonitorForm.element" placeholder="请输入网址"></el-input> -->
                            <el-select v-model="space_name" placeholder="Select" size="large" @change="ChangeSpace">
                                <el-option
                                v-for="item in space_names"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                                />
                            </el-select>
                        </el-col>
                    </el-form-item>
                    <el-form-item label="监控名" prop="name">
                        <el-col :span="20">
                            <el-input v-model="addMonitorForm.name" placeholder="请输入昵称"></el-input>
                        </el-col>
                    </el-form-item>
                    <el-form-item label="监控说明" prop="desc">
                        <el-col :span="20">
                            <el-input v-model="addMonitorForm.desc" placeholder="请输入监控说明"></el-input>
                        </el-col>
                    </el-form-item>
                    <el-form-item label="网址" prop="url">
                        <el-col :span="20">
                            <el-input v-model="addMonitorForm.url" placeholder="请输入网址"></el-input>
                        </el-col>
                    </el-form-item> 
                    <el-form-item label="关键词">
                      <el-col :span="20">
                          <el-input v-model="addMonitorForm.trigger_text" placeholder="请输入监控关键词"></el-input>
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
                            <el-input type="textarea" :rows="6" v-model="addMonitorForm.include_filters"  placeholder="请输入监控元素（XPath/CssSelector）, 例如：xpath://body/div/span[contains(@class,example-class]"></el-input>
                        </el-col>
                    </el-form-item>
                    <el-form-item label="刷新时间">
                      <el-form-item prop="time_between_check_weeks" style="width:81px;">
                            <el-input v-model="addMonitorForm.time_between_check_weeks" placeholder="周"></el-input>
                      </el-form-item>
                      <el-form-item prop="time_between_check_days" style="width:81px;">
                            <el-input v-model="addMonitorForm.time_between_check_days" placeholder="天"></el-input>
                      </el-form-item>
                      <el-form-item prop="time_between_check_hours" style="width:81px;">
                            <el-input v-model="addMonitorForm.time_between_check_hours" placeholder="时"></el-input>
                      </el-form-item>
                      <el-form-item prop="time_between_check_minutes" style="width:81px;">
                            <el-input v-model="addMonitorForm.time_between_check_minutes" placeholder="分"></el-input>
                      </el-form-item>
                      <el-form-item prop="time_between_check_seconds" style="width:81px;">
                            <el-input v-model="addMonitorForm.time_between_check_seconds" placeholder="秒"></el-input>
                      </el-form-item>
                  </el-form-item>
                    <el-form-item label="通知邮箱" prop="notification_email">
                        <el-col :span="20">
                            <el-input v-model="addMonitorForm.notification_email"></el-input>
                        </el-col>
                    </el-form-item>
                </el-form>
                <el-button type="success" @click="confirm_monitor">添加</el-button>
                <el-button type="primary" @click="RemoveIframe">退出</el-button>
            </div>
        </el-aside>
        <el-main>
            <el-input type="textarea" :rows="20"  v-model="SelectText"></el-input>
        </el-main>
        </el-container>
        <el-dialog
            v-model="okLogin"
            width="30%"
            align-center
            >
            <span>用户未登录或上次登录状态过期，请重新登录。</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button type="primary" @click="RemoveIframe_Login">
                    确定
                </el-button>
                </span>
            </template>
        </el-dialog>
        <el-dialog
            v-model="okAddMonitor"
            width="30%"
            align-center
            >
            <span>添加成功</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button type="success" @click="keepSelect">
                    继续
                </el-button>
                <el-button type="primary" @click="RemoveIframe">
                    退出
                </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
    
</template>
  
<script>
// import '../../embed/chromeExtension';
// import Cookies from 'universal-cookie';
export default{
    data(){
        const vaildateEmail = (rule, value, callback) => {
            let EmailReg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
            if(EmailReg.test(value)){
                return callback()
            } 
            return callback(new Error('请输入有效的邮箱'))
        }
        const vaildateUrl = (rule, value, callback) => {
            let UrlReg = /^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z0-9\u00a1-\uffff][a-z0-9\u00a1-\uffff_-]{0,62})?[a-z0-9\u00a1-\uffff]\.)+(?:[a-z\u00a1-\uffff]{2,}\.?))(?::\d{2,5})?(?:[/?#]\S*)?$/i

            if(UrlReg.test(value)){
                return callback()
            } 
            return callback(new Error('请输入有效的网址'))
        }
        return {
            SelectText:'',
            space_id:'',
            space_name:'',
            space_names:[

            ],
            value:'',
            options:[
                {
                    value: 'XPath',
                    label: 'XPath',
                },
                {
                    value: 'CssSelector',
                    label: 'CssSelector',
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
                include_filters:'',
                trigger_text:''
            },
            Element:'',
            MonitorRules:{
                  name:[
                      {required:true, message: '请输入昵称', trigger:'blur'},
                  ],
                  desc:[
                      {message: '请输入描述', trigger:'blur'}
                  ],
                  url:[
                    //   {required:true, message: '请输入网址', trigger:'blur'}
                      {required:true, validator: vaildateUrl, trigger:'blur'}
                  ],
                  element:[
                      {required:true, message: '请输入元素', trigger:'blur'}
                  ],
                  notification_email:[
                    //   {required:true, message: '请输入元素', trigger:'blur'}
                      {required:true, validator: vaildateEmail, trigger:'blur'}
                  ],
                  include_filters:[
                      {required:true, message: '请输入密码', trigger:'blur'}
                  ],
                  time_between_check_weeks:[
                      {required:true, message: '请输入时间', trigger:'blur'}
                  ],
                  time_between_check_days:[
                      {required:true, message: '请输入时间', trigger:'blur'}
                  ],
                  time_between_check_hours:[
                      {required:true, message: '请输入时间', trigger:'blur'}
                  ],
                  time_between_check_minutes:[
                      {required:true, message: '请输入时间', trigger:'blur'}
                  ],
                  time_between_check_seconds:[
                      {required:true, message: '请输入时间', trigger:'blur'}
                  ]
            },
            verify_authenticity_token:'',
            fullscreenLoading: false,
            okLogin: false,
            okAddMonitor: false
        }
    },
    created(){
        this.value = 'XPath'
        this.fullscreenLoading = true
        window.parent.postMessage({msg: "start"}, '*');
    },
    mounted(){
        window.addEventListener("message", (e) => {
            console.log(e.data)
            console.log(e.data.baseURI);
            // this.verify_authenticity_token = e.data.verify_authenticity_token;
            this.verify_authenticity_token = this.getCookie('verify_authenticity_token')

            if(this.verify_authenticity_token === ""){
                this.okLogin = true
                this.fullscreenLoading = false
            }
            // console.log("-----")
            // console.log(this.verify_authenticity_token);
            // console.log(document)
            
            this.Element = e.data;
            this.addMonitorForm.url = e.data.baseURI;
            this.SelectText = e.data.selectText;
            if(e.data.xpath === ''){
                this.getUser();
                this.getMonitorSpaceList();
            }else if(this.value=== 'XPath'){
                if(this.addMonitorForm.include_filters.indexOf(e.data.xpath) === -1)
                    this.addMonitorForm.include_filters = this.addMonitorForm.include_filters + "xpath:" + e.data.xpath + '\n';
            }else if(this.value === 'CssSelector'){
                if(this.addMonitorForm.include_filters.indexOf(e.data.selector) === -1)
                    this.addMonitorForm.include_filters = this.addMonitorForm.include_filters + "css:" + e.data.selector + '\n' ;
            }else if(this.value === 'JSONPath'){
                // this.addMonitorForm.include_filters = this.addMonitorForm.include_filters + "json:" + e.data.jsonPath + '\n' ;
            }
        });
    },
    methods:{
        //获取token
        getCookie(name){
            console.log(document.cookie)
            var arr = document.cookie.split(";")
            for(var i = 0 ; i < arr.length ; i++){
                var arr2 = arr[i].split("=")
                if(arr2[0].trim() === name){
                    return arr2[1]
                }
            }
        },
        ChangeSpace(){
            this.space_id = this.space_name
            console.log(this.space_id)
        },
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
            console.log(document.cookie)
            this.$refs.MonitorRef.validate(async valid => {
                console.log(this.space_id)
                console.log(valid)
                if(!valid) return 
                console.log(this.addMonitorForm)
                this.fullscreenLoading = true
                let data = this.$qs.stringify(this.addMonitorForm)
                const {data: res} = await this.$axios.post('/space/'+this.space_id+'/watch',data,
                {
                    headers : {
                        'token': this.verify_authenticity_token
                    }
                })
                if(res.status !== 200) return  this.$message.error(res.msg)
                this.fullscreenLoading = false
                this.okAddMonitor = true
            })
        },
        async getMonitorSpaceList(){
            console.log("???")
            if(this.verify_authenticity_token === '') return ;
            const {data: res} = await this.$axios.get('/spaces',
            {
                headers : {
                    'token': this.verify_authenticity_token
                }
            })
            if(res.status !== 200){
                this.okLogin = true
                this.fullscreenLoading = false
                // return this.$message.error(res.msg)
            }
            this.fullscreenLoading = false
            // this.$message.success(res.msg)
            console.log(res.data)
            for(let i = 0; i < res.data.items.length; i ++){
                console.log(res.data.items[i].id)
                this.space_names.push({
                    value: res.data.items[i].id,
                    label: res.data.items[i].name
                })
            }
            this.space_name = res.data.items[0].id
            this.space_id = res.data.items[0].id
            this.addMonitorForm.time_between_check_days = '1'
            this.addMonitorForm.time_between_check_hours = '0'
            this.addMonitorForm.time_between_check_minutes = '0'
            this.addMonitorForm.time_between_check_seconds = '0'
            this.addMonitorForm.time_between_check_weeks = ''
            console.log(res.data)
        //   this.space_names = res.data
        },
        //获取用户邮箱
        async getUser(){
            if(this.verify_authenticity_token === '') return ;
            const {data: res} = await this.$axios.get('/user',
            {
                headers : {
                    'token': this.verify_authenticity_token
                }
            })
            if(res.status !== 200){
                this.okLogin = true
                this.fullscreenLoading = false
                return this.$message.error(res.msg)
            }
            this.addMonitorForm.notification_email = res.data.email
            this.fullscreenLoading = false
            this.$message.success(res.msg)
        },
        async test(){
            const {data: res} = await this.$axios.get('/bookmark/inject.js',
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            console.log(res.data)
        //   this.space_names = res.data
        },
        //移除iframe
        RemoveIframe(){
            window.parent.postMessage({msg: "Remove"}, '*');
        },
        //移除iframe并跳转登录
        RemoveIframe_Login(){
            window.parent.postMessage({msg: "Remove_Login"}, '*');
        },
        //点击“继续”，初始化
        keepSelect(){
            this.okAddMonitor = false, this.addMonitorForm.des =''
            this.addMonitorForm.desc = ''
            this.addMonitorForm.name = ''
            this.addMonitorForm.include_filters =''
            this.addMonitorForm.trigger_text =''
            this.SelectText = ''
        }
          
    }
}
</script>
  
<style>
.iframe_style{
    background-color: aliceblue;
}

.form_style{
    margin-top: 15px;
}
</style>