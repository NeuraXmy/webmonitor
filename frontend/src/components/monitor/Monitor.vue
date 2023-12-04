<template>
    <div>
        <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>任务管理</el-breadcrumb-item>
            <el-breadcrumb-item :to="{ path: '/spaces' }">监控空间列表</el-breadcrumb-item>
            <el-breadcrumb-item>空间监控管理</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
          <el-row>
              <el-col :span="2">
                  <div>
                      <el-button type="primary" @click="addMonitorListener"><el-icon><Plus /></el-icon>增加</el-button>
                  </div>
              </el-col>
          </el-row>
          <el-row>
              <el-table v-loading="loading" :data="MonitorList" style="width: 100%">
                  <el-table-column prop="id" label="ID" width="50" />
                  <el-table-column prop="name" label="监控名" width="80" />
                  <el-table-column prop="url" label="网址" width="270" />
                  <!-- <el-table-column prop="update_time" label="更新时间" width="200" /> -->
                  <el-table-column prop="last_check_time" label="检查时间" width="200" />
                  <el-table-column prop="last_check_state" label="检查状态" width="200" />
                  <el-table-column prop="edit" label="Edit" width="340">
                      <template #default="scope">
                          <el-button size="small" @click="WatchEdit(scope.row)"
                          >编辑</el-button
                          >
                          <el-button
                          size="small"
                          type="danger"
                          @click="DeleteWatch(scope.row)"
                          >删除</el-button
                          >
                          <el-button
                          size="small"
                          type="info"
                          @click="RefreshWatch(scope.row)"
                          >刷新</el-button
                          >
                          <el-button
                          size="small"
                          type="success"
                          @click="WatchHistory(scope.row)"
                          >检查记录</el-button
                          >
                      </template>
                  </el-table-column>
              </el-table>
              <el-pagination
                    v-model:current-page="queryPage.page"
                    v-model:page-size="queryPage.size"
                    :page-sizes="[5, 10, 20, 50]"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="TotalPages"
                    @size-change="handleSizeMonitorChange"
                    @current-change="handleCurrentMonitorChange"
                    />
          </el-row>
        </el-card>
        <el-dialog
              v-model="addMonitor"
              title="新增监控网址"
              width="40%"
          >
              <el-form ref="MonitorRef" :rules="MonitorRules" :model="addMonitorForm" label-width="80px" class="form_style">
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
                          <el-input v-model="addMonitorForm.url" placeholder="请输入网址（http://或https://开头）"></el-input>
                      </el-col>
                  </el-form-item>
                  <el-form-item label="关键词">
                      <el-col :span="20">
                          <el-input v-model="addMonitorForm.trigger_text" placeholder="请输入监控关键词"></el-input>
                      </el-col>
                  </el-form-item>
                  <el-form-item label="监控元素">
                      <el-col :span="20">
                          <el-select v-model="this.value" placeholder="Select" size="large" @change="ChangeElement">
                              <el-option
                              v-for="item in options"
                              :key="item.value"
                              :label="item.label"
                              :value="item.value"
                              />
                          </el-select>
                          <el-input type="textarea" :disabled="okDisabled" :rows="6" v-model="addMonitorForm.include_filters" placeholder="请输入监控元素（XPath/CssSelector）, 例如：xpath://body/div/span[contains(@class,example-class]"></el-input>
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
              <!-- <span>....</span> -->
              <template #footer>
              <span class="dialog-footer">
                  <el-button @click="addMonitor = false">取消</el-button>
                  <el-button type="primary" @click="addMonitorList">
                  确定
                  </el-button>
              </span>
              </template>
          </el-dialog>
          <el-dialog
              v-model="EditMonitor"
              title="编辑监控信息"
              width="40%"
          >
              <el-form  ref="MonitorRef" :rules="MonitorRules" :model="addMonitorForm" label-width="80px" class="form_style">
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
                          <el-input v-model="addMonitorForm.url" placeholder="请输入网址（http://或https://开头）"></el-input>
                      </el-col>
                  </el-form-item>
                  <el-form-item label="关键词">
                      <el-col :span="20">
                          <el-input v-model="addMonitorForm.trigger_text" placeholder="请输入监控关键词"></el-input>
                      </el-col>
                  </el-form-item>
                  <el-form-item label="监控元素">
                      <el-col :span="20">
                          <el-select v-model="value" placeholder="Select" size="large" @change="ChangeElement">
                              <el-option
                              v-for="item in options"
                              :key="item.value"
                              :label="item.label"
                              :value="item.value"
                              />
                          </el-select>
                          <el-input type="textarea" :disabled="okDisabled" :rows="6" v-model="addMonitorForm.include_filters" placeholder="请输入监控元素（XPath/CssSelector）, 例如：xpath://body/div/span[contains(@class,example-class]"></el-input>
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
              <template #footer>
              <span class="dialog-footer">
                  <el-button @click="EditMonitor = false">取消</el-button>
                  <el-button type="primary" @click="WatchEditConfirm">
                  确定
                  </el-button>
              </span>
              </template>
          </el-dialog>
        <el-dialog
            v-model="okDeleteWatch"
            width="30%"
            align-center
            >
            <span>是否删除监控？</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okDeleteWatch = false">取消</el-button>
                <el-button type="primary" @click="ConfirmDeleteWatch">
                    确定
                </el-button>
                </span>
            </template>
        </el-dialog>
        <el-dialog
            v-model="okReflashWatch"
            width="30%"
            align-center
            >
            <span>刷新监控成功</span>
        </el-dialog>
      </div>
  </template>
  <script>
  import { Search,Plus,Delete } from '@element-plus/icons-vue'
  import { ref, computed } from 'vue';
  export default{
      
      components: { Search,Plus,Delete },
      data(){
          const vaildateEmail = (rule, value, callback) => {
            let EmailReg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
            console.log("++++")
            if(EmailReg.test(value)){
                return callback()
            } 
            return callback(new Error('请输入有效的邮箱'))
          }
          const vaildateUrl = (rule, value, callback) => {
            let UrlReg = /^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z0-9\u00a1-\uffff][a-z0-9\u00a1-\uffff_-]{0,62})?[a-z0-9\u00a1-\uffff]\.)+(?:[a-z\u00a1-\uffff]{2,}\.?))(?::\d{2,5})?(?:[/?#]\S*)?$/i
            console.log("++++")
            if(UrlReg.test(value)){
                return callback()
            } 
            return callback(new Error('请输入有效的网址'))
          }
          return {
            
              MonitorList:[
                //   {id:'',name:'',url:'',create_time:'',update_time:'',last_check_time:''}
              ],
              value:'',
              options:[
                  {
                      value: '1',label: 'All',
                  },
                  {
                      value: '2',label: 'XPath/CssSelector',
                  }
              ],
              addMonitor:false,
              addMonitorForm:{
                  name:'',
                  desc:'',
                  url:'',
                  element:'',
                  time_between_check_weeks:'',
                  time_between_check_days:'',
                  time_between_check_hours:'',
                  time_between_check_minutes:'',
                  time_between_check_seconds:'',
                  notification_email:'',
                  include_filters:'',
                  trigger_text:''
              },
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
              space_id: 1,
              watch_id: 1,
              EditMonitor: false,
              generateUrl: '',
              okDeleteWatch: false,
              DeleteWatchID: '',
              okReflashWatch: false,
              okDisabled: false,
              loading: false,
              iframe_url: '',
              TotalPages: 10,
              queryPage: {
                page:1,
                size:5
              }
          }
      },
      created(){
          this.JumpMonitorManage()
        //   this.getBookmark()
      },
      methods:{
        //获取某个space下的监控列表
        async JumpMonitorManage(){
            this.space_id=sessionStorage.getItem('space_id')
            this.loading = true
        //   this.okMonitor=false
            console.log("11111")
            const {data: res} = await this.$axios.get('/space/'+this.space_id+'/watches',
            {
                params: this.queryPage,
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            this.loading = false
            this.TotalPages = res.data.total
            this.MonitorList = res.data.items
            console.log(res.data)
        },
        //刷新监控列表
        async RefreshMonitorManage(val){
            this.space_id = val
            const {data: res} = await this.$axios.get('/space/'+this.space_id+'/watches',
            {
                params: this.queryPage,
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.TotalPages = res.data.total
            this.MonitorList = res.data.items
        },
        //用户在某个space下创建监控
        addMonitorList(){
        this.$refs.MonitorRef.validate(async valid => {
            console.log(valid)
            if(!valid) return 
            this.addMonitor=false
            this.loading = true
            let data = this.$qs.stringify(this.addMonitorForm)
            const {data: res} = await this.$axios.post('/space/'+this.space_id+'/watch',data,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status ===200){
                this.RefreshMonitorManage(this.space_id)
            }else{
                this.$message.error(res.msg);
            }
            this.loading = false
        })
        },
        addMonitorListener(){
            this.addMonitor=true
            this.addMonitorForm.desc = ''
            this.addMonitorForm.element = ''
            this.addMonitorForm.include_filters = ''
            this.addMonitorForm.notification_email = ''
            this.addMonitorForm.url = ''
            this.addMonitorForm.trigger_text = ''
            this.addMonitorForm.name = ''
            this.addMonitorForm.time_between_check_days = '1'
            this.addMonitorForm.time_between_check_hours = '0'
            this.addMonitorForm.time_between_check_minutes = '0'
            this.addMonitorForm.time_between_check_seconds = '0'
            this.addMonitorForm.time_between_check_weeks = ''
        },
        //用户确定删除监控
        async ConfirmDeleteWatch(){
            this.okDeleteWatch = false;
            this.loading = true
            const {data: res} = await this.$axios.delete('/watch/'+this.DeleteWatchID,
            {
                params:{id: this.DeleteWatchID},
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.RefreshMonitorManage(this.space_id)
            this.loading = false
        },
        DeleteWatch(row){
        this.okDeleteWatch = true;
        this.DeleteWatchID = row.id;
        },
        //触发用户修改监控,保存watch_id并且获取监控信息
        async WatchEdit(row){
            this.loading = true
        //   this.EditMonitor=true;
            this.watch_id=row.id;
            const {data: res} = await this.$axios.get('/watch/'+this.watch_id,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.EditMonitor=true;
            this.loading = false
            this.addMonitorForm = res.data
            if(this.addMonitorForm.include_filters === ''){
            this.value = 'All';
            this.okDisabled = true
            }else{
            this.value = 'XPath/CssSelector';
            this.okDisabled = false
            }
            console.log(res.data);
        },
        //用户修改监控
        WatchEditConfirm(){
        this.$refs.MonitorRef.validate(async valid => {
            console.log(valid)
            if(!valid) return 
            this.EditMonitor=false
            this.loading = true
            let data = this.$qs.stringify(this.addMonitorForm)
            const {data: res} = await this.$axios.put('/watch/'+this.watch_id,data,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status ===200){
                // this.EditMonitor=false
                // this.loading = true
                this.RefreshMonitorManage(this.space_id)
            }else{
                this.$message.error(res.message);
            }
            this.loading = false
        })
        },
        //用户立刻刷新监控
        async RefreshWatch(row){
            this.loading = true
            let data={
                'token': sessionStorage.getItem('token')
            }
            const {data: res} = await this.$axios.post('/watch/'+row.id+'/check',data,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            
            this.RefreshMonitorManage(this.space_id)
            this.loading = false
            this.okReflashWatch = true
        },
        //改变多选框
        ChangeElement(){
        console.log(this.value)
        if(this.value === '1'){
            this.okDisabled = true
            this.addMonitorForm.include_filters = ""
        }else if(this.value === '2'){
            this.okDisabled = false
        }else if(this.value === 'JSONPath'){
            // this.addMonitorForm.include_filters=this.Element.jsonPath;
        }
        },
        async getBookmark(){
            const {data: res} = await this.$axios.get('/bookmark/inject.js',
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            // console.log(res.data)
            this.iframe_url = res.data
            // console.log(this.iframe_url)
        },
        //获得监控页号
        handleCurrentMonitorChange(val){
            this.queryPage.page = val
            this.RefreshMonitorManage(this.space_id)
        },
        //获得监控页数
        handleSizeMonitorChange(val){
            this.queryPage.size = val
            this.RefreshMonitorManage(this.space_id)
        },
        //点击检查记录按钮
        WatchHistory(row){
            console.log(row)
            sessionStorage.setItem('watch_id',row.id);
            sessionStorage.setItem('watch_url',row.url);
            this.$router.push('/CheckHistory')
        }
      }
  }
  
  </script>
  <style>
  .input-with-select .el-input-group__prepend {
    background-color: var(--el-fill-color-blank);
  }
  .el-table{
      margin-top: 10px;
  }
  .el-pagination{
      margin-top: 10px;
  }
  </style>