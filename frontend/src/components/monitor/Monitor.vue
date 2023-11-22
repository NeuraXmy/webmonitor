<template>
    <div v-if="okMonitor">
      <el-breadcrumb>
          <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>任务管理</el-breadcrumb-item>
          <el-breadcrumb-item>监控空间列表</el-breadcrumb-item>
      </el-breadcrumb>
      <el-card>
          <el-row>
              <!-- <el-col :span="12">
                  <div>
                      <el-input
                      v-model="queryInfo.name"
                      placeholder="请输入Name"
                      >
                      <template #append>
                          <el-button @click="searchSpace"><el-icon><Search /></el-icon></el-button>
  
                      </template>  
                      </el-input>
                  </div>
              </el-col> -->
              <el-col :span="4">
                  <div>
                      <el-button type="primary" @click="addSpace=true, this.addSpaceForm.name = '', this.addSpaceForm.desc = ''"><el-icon><Plus /></el-icon>新增空间</el-button>
                      
                  </div>
              </el-col>
              <el-col :span="2">
                  <div>
                      <a :href="iframe_url" title="将我拖动到书签栏">小书签</a>
                  </div>
              </el-col>
          </el-row>
          <el-row>
              <el-table v-loading="loading" :data="MonitorSpaceList" style="width: 100%">
                  <el-table-column prop="id" label="ID" width="100" />
                  <el-table-column prop="name" label="空间名" width="200" />
                  <!-- <el-table-column prop="create_time" label="创建时间" width="350" /> -->
                  <el-table-column prop="update_time" label="更新时间" width="350" />
                  <el-table-column prop="edit" label="Edit" width="200">
                      <template #default="scope">
                          <el-button size="small" @click="JumpMonitorManage(scope.row)"
                          >进入</el-button
                          >
                          <el-button size="small" @click="EditSpace(scope.row)"
                          >编辑</el-button
                          >
                          <el-button
                          size="small"
                          type="danger"
                          @click="DeleteSpace(scope.row)"
                          >删除</el-button
                          >
                      </template>
                  </el-table-column>
              </el-table>
          </el-row>
      </el-card>
      <el-dialog
      v-model="addSpace"
      title="新增空间"
      width="40%"
    >
      <el-form ref="addSpaceRef" :rules="addSpaceRules" :model="addSpaceForm" label-width="80px" class="form_style">
          <el-form-item label="昵称" prop="name">
              <el-col :span="20">
                  <el-input v-model="addSpaceForm.name" placeholder="请输入昵称"></el-input>
              </el-col>
          </el-form-item>
          <el-form-item label="空间说明" prop="desc">
              <el-col :span="20">
                  <el-input v-model="addSpaceForm.desc" placeholder="请输入空间说明"></el-input>
              </el-col>
          </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addSpace = false">取消</el-button>
          <el-button type="primary" @click="addSpaceList">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
    <el-dialog
      v-model="okEditSpace"
      title="编辑空间"
      width="40%"
    >
      <el-form ref="addSpaceRef" :rules="addSpaceRules" :model="addSpaceForm" label-width="80px" class="form_style">
          <el-form-item label="昵称" prop="name">
              <el-col :span="20">
                  <el-input v-model="addSpaceForm.name" placeholder="请输入昵称"></el-input>
              </el-col>
          </el-form-item>
          <el-form-item label="空间说明" prop="desc">
              <el-col :span="20">
                  <el-input v-model="addSpaceForm.desc" placeholder="请输入空间说明"></el-input>
              </el-col>
          </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="okEditSpace = false">取消</el-button>
          <el-button type="primary" @click="EditSpaceConfirm">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
    <el-dialog
            v-model="okDeleteSpace"
            width="30%"
            align-center
            >
            <span>是否删除监控？</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okDeleteSpace = false">取消</el-button>
                <el-button type="primary" @click="ConfirmDeleteSpace">
                    确定
                </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
    <div v-if="!okMonitor">
        <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>任务管理</el-breadcrumb-item>
            <el-breadcrumb-item @click="this.okMonitor=true">监控空间列表</el-breadcrumb-item>
            <el-breadcrumb-item>空间监控管理</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
          <el-row>
              <el-col :span="2">
                  <div>
                      <el-button type="primary" @click="addMonitorListener"><el-icon><Plus /></el-icon>增加</el-button>
                  </div>
              </el-col>
              <!-- <el-col :span="2">
                  <div>
                      <a :href='generateUrl' title="将我拖动到书签栏">拖到书签栏</a>
                      
                  </div>
              </el-col> -->
          </el-row>
          <el-row>
              <el-table v-loading="loading" :data="MonitorList" style="width: 100%">
                  <el-table-column prop="id" label="ID" width="50" />
                  <el-table-column prop="name" label="监控名" width="80" />
                  <el-table-column prop="url" label="网址" width="270" />
                  <!-- <el-table-column prop="update_time" label="更新时间" width="200" /> -->
                  <el-table-column prop="last_check_time" label="检查时间" width="200" />
                  <el-table-column prop="last_check_state" label="检查状态" width="200" />
                  <el-table-column prop="edit" label="Edit" width="240">
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
                      </template>
                  </el-table-column>
              </el-table>
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
                      <el-col :span="4">
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
                  <el-form-item label="通知邮箱" prop="notification_email">
                      <el-col :span="20">
                          <el-input v-model="addMonitorForm.notification_email"></el-input>
                      </el-col>
                  </el-form-item>
              </el-form>
              <!-- <span>....</span> -->
              <template #footer>
              <span class="dialog-footer">
                  <el-button @click="addMonitor = false">Cancel</el-button>
                  <el-button type="primary" @click="addMonitorList">
                  Confirm
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
                      <el-col :span="4">
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
                  <el-form-item label="通知邮箱" prop="notification_email">
                      <el-col :span="20">
                          <el-input v-model="addMonitorForm.notification_email"></el-input>
                      </el-col>
                  </el-form-item>
              </el-form>
              <template #footer>
              <span class="dialog-footer">
                  <el-button @click="EditMonitor = false">Cancel</el-button>
                  <el-button type="primary" @click="WatchEditConfirm">
                  Confirm
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
            // let UrlReg = /^(https|http|ftp)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(:[0-9]{1,5})?(\/[\S]*)?$/
            
            let UrlReg = /^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z0-9\u00a1-\uffff][a-z0-9\u00a1-\uffff_-]{0,62})?[a-z0-9\u00a1-\uffff]\.)+(?:[a-z\u00a1-\uffff]{2,}\.?))(?::\d{2,5})?(?:[/?#]\S*)?$/i
            console.log("++++")
            if(UrlReg.test(value)){
                return callback()
            } 
            return callback(new Error('请输入有效的网址'))
          }
          return {
              okMonitor:true,
              MonitorSpaceList:[
                //   {id:'',name:'',create_time:'',update_time:''}
              ],
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
              addSpace:false,
              addSpaceForm:{
                  name:'',
                  desc:''
              },
              addSpaceRules:{
                  name:[
                      {required:true, message: '请输入昵称', trigger:'blur'},
                  ],
                  desc:[
                      {message: '请输入描述', trigger:'blur'}
                  ]
              },
              okEditSpace:false,
              addMonitor:false,
              EditSpaceID:'',
              okDeleteSpace:false,
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
                  include_filters:''
              },
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
                  ]
              },
              space_id:1,
              watch_id:1,
              EditMonitor:false,
              generateUrl:'',
              okDeleteWatch:false,
              DeleteWatchID:'',
              okReflashWatch:false,
              okDisabled:false,
              loading:false,
              iframe_url:''
          }
      },
      created(){
          this.getMonitorSpaceList()
          this.getBookmark()
      },
      methods:{
          async getMonitorSpaceList(){
              this.loading = true
              const {data: res} = await this.$axios.get('/spaces',
              {
                  headers : {
                      'token': sessionStorage.getItem('token')
                  }
              })
              if(res.status !== 200) return  this.$message.error(res.msg)
              this.$message.success(res.msg)
              
              console.log(res.data)
              this.MonitorSpaceList = res.data.items
              this.loading = false
              console.log(this.MonitorSpaceList)
          },
          //获取某个space下的监控列表
          async JumpMonitorManage(val){
              this.space_id=val.id
              this.loading = true
              this.okMonitor=false
              const {data: res} = await this.$axios.get('/space/'+val.id+'/watches',
              {
                  headers : {
                      'token': sessionStorage.getItem('token')
                  }
              })
              if(res.status !== 200) return  this.$message.error(res.msg)
              this.$message.success(res.msg)
              this.loading = false
              this.MonitorList = res.data.items
              console.log(res.data)
          },
          //刷新监控列表
          async RefreshMonitorManage(val){
              this.space_id = val
            //   this.loading = true
              // this.okMonitor=false
              const {data: res} = await this.$axios.get('/space/'+this.space_id+'/watches',
              {
                  headers : {
                      'token': sessionStorage.getItem('token')
                  }
              })
              if(res.status !== 200) return  this.$message.error(res.msg)
            //   this.loading = false
              this.MonitorList = res.data
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
          //增加空间
          addSpaceList(){
            this.$refs.addSpaceRef.validate(async valid => {
                console.log(valid)
                if(!valid) return 

                this.addSpace=false
                this.loading = true
                let data = this.$qs.stringify(this.addSpaceForm)
                const {data: res} = await this.$axios.post('/space',data,
                {
                    headers : {
                        'token': sessionStorage.getItem('token')
                    }
                })
                if(res.status ===200){
                    this.getMonitorSpaceList()
                }else{
                    this.$message.error(res.msg);
                }
                this.loading = false
            })
          },
          //触发编辑空间按钮
          async EditSpace(row){
              this.EditSpaceID = row.id;
              this.loading = true

              const {data: res} = await this.$axios.get('/space/'+this.EditSpaceID,
              {
                  headers : {
                      'token': sessionStorage.getItem('token')
                  }
              })
              if(res.status !== 200) return  this.$message.error(res.msg)
              this.okEditSpace = true;
              this.loading = false
              this.addSpaceForm = res.data
          },
          //确认编辑空间
          EditSpaceConfirm(){
            this.$refs.addSpaceRef.validate(async valid => {
                console.log(valid)
                if(!valid) return 
                this.okEditSpace=false
                this.loading = true
                let data = this.$qs.stringify(this.addSpaceForm)
                const {data: res} = await this.$axios.put('/space/'+this.EditSpaceID,data,
                {
                    headers : {
                        'token': sessionStorage.getItem('token')
                    }
                })
                if(res.status ===200){
                    this.getMonitorSpaceList()
                }else{
                    this.$message.error(res.msg);
                }
                this.loading = false
            })
          },
          //触发删除空间按钮
          DeleteSpace(row){
            this.okDeleteSpace = true;
            this.EditSpaceID = row.id;
          },
          //确定删除空间
          async ConfirmDeleteSpace(){
            this.okDeleteSpace = false;
            this.loading = true
            const {data: res} = await this.$axios.delete('/space/'+this.EditSpaceID,
            {
                params:{id: this.EditSpaceID},
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.getMonitorSpaceList();
            this.loading = false
          },
          async getBookmark(){
            const {data: res} = await this.$axios.get('/bookmark/inject.js',
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            console.log(res.data)
            this.iframe_url = res.data
            console.log(this.iframe_url)
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