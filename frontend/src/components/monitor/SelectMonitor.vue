<template>
    <div class="common-layout iframe_style">
        <el-container>
            <el-header>
                <div style="margin-top: 15px;">
                    <span>Language:</span>
                    <el-select v-model="language" placeholder="Select" @change="Changelanguage" style="width: 100px;margin-right: 10px;">
                        <el-option
                            v-for="item in languages"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                    <el-button type="success"  @click="confirm_monitor" >{{ $t('select.add') }}</el-button>
                    <el-button type="primary" @click="RemoveIframe">{{ $t('select.exit') }}</el-button>
                </div>
                <div style="margin-top: 5px;" class="right-align">
                    <span>
                        {{ $t('select.selectElements') }}
                    </span>
                </div>
            </el-header>
            <el-scrollbar>
                <el-container v-loading.fullscreen.lock="fullscreenLoading">
                    <el-aside width="800px">
                        <div class="form_style">
                            <el-form ref="MonitorRef" :rules="MonitorRules" :model="addMonitorForm" label-width="100px" class="form_style">
                                <el-form-item :label="$t('select.monitorElements')">
                                    <el-col :span="20">
                                        <el-input
                                            v-for="(item, index) in filters"
                                            :key="index"
                                            v-model="item.element"
                                            placeholder="Please input"
                                            class="input-with-select"
                                        >
                                            <template #prepend>
                                                <el-select v-model="item.option" placeholder="Select" @change="ChangeElement" style="width: 120px">
                                                    <el-option
                                                        v-for="item in options"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value"
                                                    />
                                                </el-select>
                                            </template>
                                            <template #append>
                                                <el-button @click="deletefilter(index)"><el-icon><Close /></el-icon></el-button>
                                            </template>
                                        </el-input>
                                    </el-col>
                                    <!-- <el-col :span="20">
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
                                    </el-col> -->
                                </el-form-item>
                                <el-form-item :label="$t('select.selectSpace')">
                                    <el-col :span="20">
                                        <!-- <el-input v-model="addMonitorForm.element" placeholder="请输入网址"></el-input> -->
                                        <el-select v-model="space_name" placeholder="Select" @change="ChangeSpace">
                                            <el-option
                                            v-for="item in space_names"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value"
                                            />
                                        </el-select>
                                    </el-col>
                                </el-form-item>
                                <el-form-item :label="$t('monitor.dialogs.addMonitor.monitorName')" prop="name">
                                    <el-col :span="20">
                                        <el-input v-model="addMonitorForm.name" :placeholder="$t('placeholders.monitorName')"></el-input>
                                    </el-col>
                                </el-form-item>
                                <el-form-item :label="$t('monitor.dialogs.addMonitor.monitorDesc')" prop="desc">
                                    <el-col :span="20">
                                        <el-input v-model="addMonitorForm.desc" :placeholder="$t('placeholders.monitorDescription')"></el-input>
                                    </el-col>
                                </el-form-item>
                                <el-form-item :label="$t('monitor.dialogs.addMonitor.url')" prop="url">
                                    <el-col :span="20">
                                        <el-input v-model="addMonitorForm.url" :placeholder="$t('placeholders.monitorUrl')"></el-input>
                                    </el-col>
                                </el-form-item> 
                                <el-form-item :label="$t('monitor.dialogs.addMonitor.keyword')">
                                    <el-col :span="20">
                                        <el-input v-model="addMonitorForm.trigger_text" :placeholder="$t('placeholders.monitorKeywords')"></el-input>
                                    </el-col>
                                </el-form-item>
                                <el-form-item :label="$t('monitor.dialogs.addMonitor.refreshTime')">
                                <el-form-item prop="time_between_check_weeks" style="width:120px;">
                                        <el-input v-model="addMonitorForm.time_between_check_weeks">
                                            <template #append>{{$t('monitor.dialogs.weekly')}}</template>
                                        </el-input>
                                </el-form-item>
                                <el-form-item prop="time_between_check_days" style="width:120px;">
                                        <el-input v-model="addMonitorForm.time_between_check_days">
                                            <template #append>{{$t('monitor.dialogs.day')}}</template>
                                        </el-input>
                                </el-form-item>
                                <el-form-item prop="time_between_check_hours" style="width:120px;">
                                        <el-input v-model="addMonitorForm.time_between_check_hours">
                                            <template #append>{{$t('monitor.dialogs.hour')}}</template>
                                        </el-input>
                                </el-form-item>
                                <el-form-item prop="time_between_check_minutes" style="width:120px;">
                                        <el-input v-model="addMonitorForm.time_between_check_minutes">
                                            <template #append>{{$t('monitor.dialogs.minute')}}</template>
                                        </el-input>
                                </el-form-item>
                                <el-form-item prop="time_between_check_seconds" style="width:120px;">
                                        <el-input v-model="addMonitorForm.time_between_check_seconds">
                                            <template #append>{{$t('monitor.dialogs.second')}}</template>
                                        </el-input>
                                </el-form-item>
                            </el-form-item>
                                <el-form-item :label="$t('monitor.dialogs.addMonitor.notificationEmail')" prop="notification_email">
                                    <el-col :span="20">
                                        <el-input v-model="addMonitorForm.notification_email"></el-input>
                                    </el-col>
                                </el-form-item>
                            </el-form>
                        </div>
                    </el-aside>
                    <el-main>
                        <el-input type="textarea" :rows="20"  v-model="SelectText"></el-input>
                    </el-main>
                </el-container>
            </el-scrollbar>
        </el-container>
        <el-dialog
            v-model="okLogin"
            width="30%"
            align-center
            >
            <span>{{ $t('select.loginPrompt') }}</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button type="primary" @click="RemoveIframe_Login">
                    {{ $t('select.confirm') }}
                </el-button>
                </span>
            </template>
        </el-dialog>
        <el-dialog
            v-model="okAddMonitor"
            width="30%"
            align-center
            >
            <span>{{ $t('select.addSuccess') }}</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button type="success" @click="keepSelect">
                    {{ $t('select.continue') }}
                </el-button>
                <el-button type="primary" @click="RemoveIframe">
                    {{ $t('select.exit') }}
                </el-button>
                </span>
            </template>
        </el-dialog>
        <el-dialog
            v-model="okAddElement"
            width="30%"
            align-center
            >
            <span>{{ $t('select.addElementPrompt') }}</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button type="success" @click="this.okAddElement = false">
                    {{ $t('select.cancel') }}
                </el-button>
                <el-button type="primary" @click="confirm_addelement">
                    {{ $t('select.confirm') }}
                </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
    
</template>
  
<script>
import { Close } from '@element-plus/icons-vue'
export default{
      
    components: { Close },
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
            languages:[
                {
                    value: 1,
                    label: 'English',
                },
                {
                    value: 2,
                    label: '简体中文',
                }
            ],
            language:2,
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
            Element:[

            ],
            MonitorRules:{
                  name:[
                      {required:true, message: '请输入昵称', trigger:'blur'},
                  ],
                  desc:[
                      {message: '请输入描述', trigger:'blur'}
                  ],
                  url:[
                      {required:true, validator: vaildateUrl, trigger:'blur'}
                  ],
                  element:[
                      {required:true, message: '请输入元素', trigger:'blur'}
                  ],
                  notification_email:[
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
            okAddMonitor: false,
            filters:[
                // {
                //     option: 'XPath',
                //     element: '123',
                //     xpath: '123',
                //     cssSelector: '234'
                // }
            ],
            okAddElement:false
        }
    },
    created(){
        this.value = 'XPath'
        this.fullscreenLoading = true
        window.parent.postMessage({msg: "start"}, '*');
    },
    mounted(){
        window.addEventListener("message", (e) => {
            // console.log(e.data)
            // console.log(e.data.baseURI);
            // this.verify_authenticity_token = e.data.verify_authenticity_token;
            this.verify_authenticity_token = this.getCookie('verify_authenticity_token')

            if(this.verify_authenticity_token === ""){
                this.okLogin = true
                this.fullscreenLoading = false
            }
            this.Element = e.data;
            this.addMonitorForm.url = e.data.baseURI;
            this.SelectText = e.data.selectText;
            if(e.data.xpath === '' || e.data.xpath === undefined){
                this.getUser();
                this.getMonitorSpaceList();
            }else{
                let ok = true
                for(let i = 0; i < this.filters.length; i ++){
                    if(this.filters[i].xpath.indexOf(e.data.xpath) !== -1){
                        ok = false;
                        break;
                    }
                }
                // console.log(e.data.xpath)
                if(ok){
                    // if(this.okLogin === true) return ;
                    this.okAddElement = true;
                }
                
            }
        });
    },
    methods:{
        //获取token
        getCookie(name){
            // console.log(document.cookie)
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
            // console.log(this.space_id)
        },
        ChangeElement(event){
            // console.log(event)
            for(let i = 0; i < this.filters.length; i ++){
                console.log(this.filters[i].option)
                if(event === this.filters[i].option && event === 'XPath'){
                    this.filters[i].element = this.filters[i].xpath
                }else if(event === this.filters[i].option && event === 'CssSelector'){
                    this.filters[i].element = this.filters[i].cssSelector
                }
            }
        },
        //确定添加该元素
        confirm_addelement(){
            this.okAddElement = false
            this.filters.push({
                option: 'XPath',
                element: this.Element.xpath,
                xpath: this.Element.xpath,
                cssSelector: this.Element.selector
            });
        },
        //删除单个元素
        deletefilter(event){
            // console.log(event)
            this.filters.splice(event, 1);
        },
        async confirm_monitor(){
            if(this.filters.length === 0){
                alert("请在添加之前选择监控元素！")
            }
            this.addMonitorForm.include_filters = ''
            for(let i = 0; i < this.filters.length; i++){
                if(this.filters[i].option === 'XPath')
                    this.addMonitorForm.include_filters = this.addMonitorForm.include_filters + this.filters[i].xpath + '\n';
                if(this.filters[i].option === 'CssSelector')
                    this.addMonitorForm.include_filters = this.addMonitorForm.include_filters + this.filters[i].cssSelector + '\n';
            }
            // console.log(this.addMonitorForm.include_filters)
            // console.log(document.cookie)
            this.$refs.MonitorRef.validate(async valid => {
                if(!valid) return 
                // console.log(this.addMonitorForm)
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
            }
            this.fullscreenLoading = false
            // this.$message.success(res.msg)
            for(let i = 0; i < res.data.items.length; i ++){
                this.space_names.push({
                    value: res.data.items[i].id,
                    label: res.data.items[i].name
                })
            }
            this.space_name = res.data.items[0].id
            this.space_id = res.data.items[0].id
            this.addMonitorForm.time_between_check_days = '0'
            this.addMonitorForm.time_between_check_hours = '1'
            this.addMonitorForm.time_between_check_minutes = '0'
            this.addMonitorForm.time_between_check_seconds = '0'
            this.addMonitorForm.time_between_check_weeks = '0'
            // console.log(res.data)
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
            this.filters = []
        },
        //改变语言类型
        Changelanguage(){
            if(this.language === 1) this.$i18n.locale = 'en'
            else this.$i18n.locale = 'zh'
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
.right-align {
  float: right;
}
</style>