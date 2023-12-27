<template>
    <div>
        <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/home' }">{{ $t('breadcrumbs.home') }}</el-breadcrumb-item>
            <el-breadcrumb-item>{{ $t('home.monitor') }}</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-row>
                <el-col :span="5">
                    <el-statistic :title="$t('monitor.consumption.thisMonth')" :value="this.checkForm.this_month_check_count" />
                </el-col>
                <el-col :span="5">
                    <el-statistic :title="$t('monitor.consumption.today')" :value="this.checkForm.today_check_count" />
                </el-col>
                <el-col :span="5">
                    <el-statistic :title="$t('monitor.consumption.yesterday')" :value="this.checkForm.yesterday_check_count">
                        <template #suffix>
                        <el-icon style="vertical-align: -0.125em">
                            <ChatLineRound />
                        </el-icon>
                        </template>
                    </el-statistic>
                </el-col>
                <el-col :span="4">
                    <el-statistic :title="$t('monitor.consumption.todayAlerts')" :value="this.checkForm.today_notification_count" />
                </el-col>
            </el-row>
        </el-card>
        <el-card>
          <el-row>
              <el-col :span="2">
                  <div>
                      <el-button type="danger" @click="DeleteMonitors"><el-icon><Delete /></el-icon>{{$t('monitor.actions.deleteMonitors')}}</el-button>
                  </div>
              </el-col>
              <el-col :span="4">
                  <div>
                      <el-button type="success" @click="CloseMonitors"><el-icon><Delete /></el-icon>{{$t('monitor.actions.closeMonitors')}}</el-button>
                  </div>
              </el-col>
          </el-row>
          <el-row>
              <el-table v-loading="loading" :data="MonitorList" style="width: 100%" @selection-change="handleSelectionMonitorsChange">
                    <el-table-column type="selection" width="50" />
                    <el-table-column prop="id" :label="$t('monitor.table.id')" width="50" />
                    <el-table-column prop="name" :label="$t('monitor.table.monitorName')" width="70" />
                    <el-table-column prop="url" :label="$t('monitor.table.url')" width="230" />
                    <el-table-column prop="last_check_time" :label="$t('monitor.table.checkTime')" width="170" />
                    <el-table-column prop="last_check_state" :label="$t('monitor.table.checkStatus')" width="170" />
                    <el-table-column prop="last_24h_check_count" :label="$t('monitor.table.last24hCheckCount')" width="130" />
                    <el-table-column prop="last_24h_notification_count" :label="$t('monitor.table.last24hAlerts')" width="155" />
                    <el-table-column fixed="right" prop="paused" :label="$t('monitor.table.enable')" width="80" >
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
                    <el-table-column fixed="right" prop="edit" label="Edit" width="280">
                      <template #default="scope">
                          <el-button size="small" @click="WatchEdit(scope.row)"
                          >{{$t('monitor.table.edit')}}</el-button
                          >
                          <el-button
                          size="small"
                          type="danger"
                          @click="DeleteWatch(scope.row)"
                          >{{$t('monitor.table.delete')}}</el-button
                          >
                          <el-button
                          size="small"
                          type="info"
                          @click="RefreshWatch(scope.row)"
                          >{{$t('monitor.table.refresh')}}</el-button
                          >
                          <el-button
                            size="small"
                            type="success"
                            @click="WatchHistory(scope.row)"
                            >{{$t('monitor.table.history')}}</el-button
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
            :title="$t('buttons.addMonitor')"
            width="40%"
        >
            <el-form ref="MonitorRef" :rules="MonitorRules" :model="addMonitorForm" label-width="80px" class="form_style">
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
                <el-form-item :label="$t('monitor.dialogs.addMonitor.element')">
                    <el-col :span="20">
                        <el-select v-model="this.value" placeholder="Select" size="large" @change="ChangeElement">
                            <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            />
                        </el-select>
                        <el-input type="textarea" :disabled="okDisabled" :rows="6" v-model="addMonitorForm.include_filters" placeholder="请输入监控元素（XPath/CssSelector）, 例如：                   //*[contains(@class, 'sametext')]"></el-input>
                    </el-col>
                </el-form-item>
                <el-form-item :label="$t('monitor.dialogs.addMonitor.refreshTime')">
                    <el-form-item prop="time_between_check_weeks" style="width:81px;">
                        <el-input v-model="addMonitorForm.time_between_check_weeks">
                            <template #append>{{$t('monitor.dialogs.weekly')}}</template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="time_between_check_days" style="width:81px;">
                        <el-input v-model="addMonitorForm.time_between_check_days">
                            <template #append>{{$t('monitor.dialogs.day')}}</template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="time_between_check_hours" style="width:81px;">
                        <el-input v-model="addMonitorForm.time_between_check_hours">
                            <template #append>{{$t('monitor.dialogs.hour')}}</template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="time_between_check_minutes" style="width:81px;">
                        <el-input v-model="addMonitorForm.time_between_check_minutes">
                            <template #append>{{$t('monitor.dialogs.minute')}}</template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="time_between_check_seconds" style="width:81px;">
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
            <!-- <span>....</span> -->
            <template #footer>
            <span class="dialog-footer">
                <el-button @click="addMonitor = false">{{ $t('buttons.cancel') }}</el-button>
                <el-button type="primary" @click="addMonitorList">
                    {{ $t('buttons.confirm') }}
                </el-button>
            </span>
            </template>
        </el-dialog>
          <el-dialog
            v-model="EditMonitor"
            :title="$t('buttons.editMonitor')"
            width="40%"
        >
            <el-form ref="MonitorRef" :rules="MonitorRules" :model="addMonitorForm" label-width="80px" class="form_style">
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
                <el-form-item :label="$t('monitor.dialogs.addMonitor.element')">
                    <el-col :span="20">
                        <el-select v-model="this.value" placeholder="Select" size="large" @change="ChangeElement">
                            <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            />
                        </el-select>
                        <el-input type="textarea" :disabled="okDisabled" :rows="6" v-model="addMonitorForm.include_filters" placeholder="请输入监控元素（XPath/CssSelector）, 例如：                   //*[contains(@class, 'sametext')]"></el-input>
                    </el-col>
                </el-form-item>
                <el-form-item :label="$t('monitor.dialogs.addMonitor.refreshTime')">
                    <el-form-item prop="time_between_check_weeks" style="width:81px;">
                        <el-input v-model="addMonitorForm.time_between_check_weeks">
                            <template #append>{{$t('monitor.dialogs.weekly')}}</template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="time_between_check_days" style="width:81px;">
                        <el-input v-model="addMonitorForm.time_between_check_days">
                            <template #append>{{$t('monitor.dialogs.day')}}</template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="time_between_check_hours" style="width:81px;">
                        <el-input v-model="addMonitorForm.time_between_check_hours">
                            <template #append>{{$t('monitor.dialogs.hour')}}</template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="time_between_check_minutes" style="width:81px;">
                        <el-input v-model="addMonitorForm.time_between_check_minutes">
                            <template #append>{{$t('monitor.dialogs.minute')}}</template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="time_between_check_seconds" style="width:81px;">
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
            <template #footer>
            <span class="dialog-footer">
                <el-button @click="EditMonitor = false">{{ $t('buttons.cancel') }}</el-button>
                <el-button type="primary" @click="WatchEditConfirm">
                    {{ $t('buttons.confirm') }}
                </el-button>
            </span>
            </template>
        </el-dialog>
        <el-dialog
            v-model="okDeleteWatch"
            width="30%"
            align-center
            >
            <span>{{ $t('messages.deleteSpaceConfirm') }}</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okDeleteWatch = false">{{ $t('buttons.cancel') }}</el-button>
                <el-button type="primary" @click="ConfirmDeleteWatch">
                    {{ $t('buttons.confirm') }}
                </el-button>
                </span>
            </template>
        </el-dialog>
        <el-dialog
            v-model="okReflashWatch"
            width="30%"
            align-center
            >
            <span>{{ $t('messages.refreshWatchSuccess') }}</span>
        </el-dialog>
        <el-dialog
            v-model="okDeleteMonitors"
            width="30%"
            align-center
            :title="$t('monitor.dialogs.cue')"
            >
            <span>{{ $t('monitor.dialogs.confirmDeleteMonitors.message') }}</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okDeleteMonitors = false">{{ $t('monitor.dialogs.confirmDeleteMonitors.cancel') }}</el-button>
                <el-button type="primary" @click="ConfirmDeleteMonitors">
                    {{ $t('monitor.dialogs.confirmDeleteMonitors.confirm') }}
                </el-button>
                </span>
            </template>
        </el-dialog>
        <el-dialog
            v-model="okCloseMonitors"
            width="30%"
            align-center
            :title="$t('monitor.dialogs.cue')"
            >
            <span>{{ $t('monitor.dialogs.confirmCloseMonitors.message') }}</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okCloseMonitors = false">{{ $t('monitor.dialogs.confirmDeleteMonitors.cancel') }}</el-button>
                <el-button type="primary" @click="ConfirmCloseMonitors">
                    {{ $t('monitor.dialogs.confirmDeleteMonitors.confirm') }}
                </el-button>
                </span>
            </template>
        </el-dialog>
        <el-dialog
            v-model="okquota_exceeded"
            width="30%"
            align-center
        >
            <span>{{ $t('monitor.dialogs.quotaExceeded') }}</span>
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
              TotalPages: 10,
              queryPage: {
                page:1,
                size:5
              },
              selectMonitorsRows:'',
              okDeleteMonitors:false,
              selectValue:'',
              searchValue:'',
              checkForm:[],
              okCloseMonitors:false,
              okquota_exceeded:false,
              quota_exceeded:false
          }
      },
      created(){
          this.JumpMonitorManage()
      },
      methods:{
          //获取某个space下的监控列表
          async JumpMonitorManage(){
            //   this.space_id=sessionStorage.getItem('space_id')
              this.loading = true
            //   this.okMonitor=false
              const {data: res} = await this.$axios.get('/user_watches',
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
            //   console.log(res.data)
            //   console.log(this.MonitorList)
            if(this.MonitorList.length > 0){
                if(this.MonitorList[0].quota_exceeded === 1){
                    this.quota_exceeded = true
                    for(let i = 0; i < this.MonitorList.length; i++){
                        this.MonitorList[i].paused = 1
                    }
                }
            }
              this.checkForm = res.data
            //   console.log(this.checkForm.total)
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
                    this.JumpMonitorManage()
                    // this.RefreshMonitorManage(this.space_id)
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
              let data = sessionStorage.getItem('token')
              const {data: res} = await this.$axios.put('/watch/'+this.DeleteWatchID+'/softdelete',data,
              {
                  params:{id: this.DeleteWatchID},
                  headers : {
                      'token': sessionStorage.getItem('token')
                  }
              })
              if(res.status !== 200) return  this.$message.error(res.msg)
            //   this.RefreshMonitorManage(this.space_id)
              this.JumpMonitorManage()
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
                    // this.RefreshMonitorManage(this.space_id)
                    this.JumpMonitorManage()
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
                if(res.status !== 200){
                    this.loading = false
                    this.okquota_exceeded = true
                    this.quota_exceeded = true
                    return  this.$message.error(res.msg)
                }
              
            //   this.RefreshMonitorManage(this.space_id)
              this.JumpMonitorManage()
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
        handleSelectionMonitorsChange(row){
            this.selectMonitorsRows = row
        },
        //触发批量删除监控按钮
        DeleteMonitors(){
            console.log(this.selectMonitorsRows.length)
            if(this.selectMonitorsRows.length > 0){
                this.okDeleteMonitors = true;
            }
        },
        //确定批量删除多个监控
        ConfirmDeleteMonitors(){
            for(let i = 0; i < this.selectMonitorsRows.length; i++){
                this.DeleteWatch(this.selectMonitorsRows[i])
                this.ConfirmDeleteWatch()
            }
            // this.RefreshMonitorManage(this.space_id)
            this.JumpMonitorManage()
            this.okDeleteMonitors = false;
        },
        //获得监控页号
        handleCurrentMonitorChange(val){
            this.queryPage.page = val
            this.JumpMonitorManage()
            // this.RefreshMonitorManage(this.space_id)
        },
        //获得监控页数
        handleSizeMonitorChange(val){
            this.queryPage.size = val
            this.JumpMonitorManage()
            // this.RefreshMonitorManage(this.space_id)
        },
        async searchMonitor(){
            if(this.searchValue !== '' && this.selectValue === ''){
                alert("请先选择搜索项！");
                return ;
            }
            console.log(this.selectValue)
            if(this.selectValue === '2'){
                this.queryPage.url = this.searchValue
                this.queryPage.name = ''
            }else if(this.selectValue === '1'){
                this.queryPage.url = ''
                this.queryPage.name = this.searchValue
            }else{
                this.queryPage.url = ''
                this.queryPage.name = ''
            }
            this.queryPage.page = 1
            this.queryPage.size = 5
            this.JumpMonitorManage();
        },
        //点击检查记录按钮
        WatchHistory(row){
            console.log(row)
            sessionStorage.setItem('watch_id',row.id);
            sessionStorage.setItem('watch_url',row.url);
            sessionStorage.setItem('front','monitors');
            // sessionStorage.setItem('back_spacesValue','')
            this.$router.push('/CheckHistory')
        },
        //关闭监控
        async CloseMonitor(row){
            if(this.quota_exceeded === true){
                this.okquota_exceeded = true;
                for(let i = 0; i < this.MonitorList.length; i++){
                    this.MonitorList[i].paused = 1
                }
                return ;
            }
            console.log(row)
            let data = this.$qs.stringify(row)
            const {data: res} = await this.$axios.post('/watch/'+row.id+'/state',data,
            {
                params: {
                    'pause': row.paused
                },
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status ===200){
                this.JumpMonitorManage()
            }else{
                this.$message.error(res.msg);
            }
        },
        CloseMonitors(){
            console.log(this.selectMonitorsRows.length)
            if(this.selectMonitorsRows.length > 0){
                this.okCloseMonitors = true;
            }
        },
        ConfirmCloseMonitors(){
            for(let i = 0; i < this.selectMonitorsRows.length; i++){
                this.selectMonitorsRows[i].paused = 1
                this.CloseMonitor(this.selectMonitorsRows[i])
            }
            // this.RefreshMonitorManage(this.space_id)
            this.JumpMonitorManage()
            this.okCloseMonitors = false;
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