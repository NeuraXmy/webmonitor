<template>
    <el-breadcrumb>
        <el-breadcrumb-item :to="{ path: '/home' }">{{ $t('breadcrumbs.home') }}</el-breadcrumb-item>
        <el-breadcrumb-item>{{ $t('breadcrumbs.spaces') }}</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
        <span>
            {{$t('tabs.addMonitorURL')}}
        </span>
        <el-form ref="MonitorRef" :rules="MonitorRules" :model="addMonitorForm" label-width="80px" class="form_style">
            <el-form-item :label="$t('label.url')" prop="url">
                <el-col :span="10">
                    <el-input v-model="addMonitorForm.url" :placeholder="$t('placeholders.monitorUrl')"></el-input>
                </el-col>
                <el-col :span="3" style="margin-left: 10px;">
                    <el-select v-model="add_space_name" :placeholder="$t('tabs.MonitorTag')">
                        <el-option
                            v-for="item in spaces"
                            :key="item.index"
                            :label="item.name"
                            :value="item.id"
                        />
                    </el-select>
                </el-col>
                <el-col :span="1" style="margin-left: 10px;">
                    <el-button type="primary" @click="addMonitorUrl">{{$t('buttons.add')}}</el-button>
                </el-col>
                <el-col :span="2" style="margin-left: 20px;">
                    <el-button type="primary" @click="addMonitor_Edit">{{$t('buttons.edit_add')}}</el-button>
                </el-col>
            </el-form-item>
        </el-form>
    </el-card>
    <el-tabs
        v-model="spacesValue"
        type="card"
        class="demo-tabs"
        editable
        @edit="handleTabsEdit"
        @tab-click="changeSpace"
        style="margin-top: 5px;"
    >
        <el-tab-pane
            v-for="item in spaces"
            :key="item.index"
            :label="item.name"
            :name="item.index"
        >
            <!-- <div class=""><button><el-icon :size="size" :color="color"><Edit /></el-icon></button></div> -->
            
            <el-card>
                <el-row>
                    <el-button type="primary" @click="EditSpace(this.space_id)"><el-icon><Edit /></el-icon>{{ $t('tabs.editSpace') }}</el-button>
                    <el-button type="primary" @click="addMonitorListener"><el-icon><Plus /></el-icon>{{ $t('buttons.addMonitor') }}</el-button>
                </el-row>
                <el-row>
                    <el-table v-loading="loading" :data="MonitorList" style="width: 100%">
                        <el-table-column prop="id" label="ID" width="50" />
                        <el-table-column prop="name" :label="$t('tableColumns.name')" width="70" />
                        <el-table-column prop="url" :label="$t('tableColumns.url')" width="230" />
                        <el-table-column prop="last_check_time" :label="$t('tableColumns.lastCheckTime')" width="170" />
                        <el-table-column prop="last_check_state" :label="$t('tableColumns.lastCheckState')" width="170" />
                        <el-table-column prop="last_24h_check_count" :label="$t('tableColumns.last24hCheckCount')" width="130" />
                        <el-table-column prop="last_24h_notification_count" :label="$t('tableColumns.last24hNotificationCount')" width="155" />
                        <el-table-column fixed="right" prop="paused" :label="$t('tableColumns.paused')" width="80" >
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
                                    >{{$t('buttons.edit')}}</el-button
                                >
                                <el-button
                                    size="small"
                                    type="danger"
                                    @click="DeleteWatch(scope.row)"
                                    >{{$t('buttons.delete')}}</el-button
                                >
                                <el-button
                                    size="small"
                                    type="info"
                                    @click="RefreshWatch(scope.row)"
                                    >{{$t('buttons.refresh')}}</el-button
                                >
                                <el-button
                                    size="small"
                                    type="success"
                                    @click="WatchHistory(scope.row)"
                                    >{{$t('buttons.History')}}</el-button
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
        </el-tab-pane>
    </el-tabs>
    <el-dialog
      v-model="addSpace"
      :title="$t('buttons.addSpace')"
      width="40%"
    >
      <el-form ref="addSpaceRef" :rules="addSpaceRules" :model="addSpaceForm" label-width="80px" class="form_style">
          <el-form-item :label="$t('label.nickname')" prop="name">
              <el-col :span="20">
                  <el-input v-model="addSpaceForm.name" :placeholder="$t('placeholders.nickname')"></el-input>
              </el-col>
          </el-form-item>
          <el-form-item :label="$t('label.spaceDec')" prop="desc">
              <el-col :span="20">
                  <el-input v-model="addSpaceForm.desc" :placeholder="$t('placeholders.spaceDescription')"></el-input>
              </el-col>
          </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addSpace = false">{{ $t('buttons.cancel') }}</el-button>
          <el-button type="primary" @click="addSpaceList">
            {{ $t('buttons.confirm') }}
          </el-button>
        </span>
      </template>
    </el-dialog>
    <el-dialog
      v-model="okEditSpace"
      :title="$t('buttons.editSpace')"
      width="40%"
    >
      <el-form ref="addSpaceRef" :rules="addSpaceRules" :model="addSpaceForm" label-width="80px" class="form_style">
          <el-form-item :label="$t('label.nickname')" prop="name">
              <el-col :span="20">
                  <el-input v-model="addSpaceForm.name" :placeholder="$t('placeholders.nickname')"></el-input>
              </el-col>
          </el-form-item>
          <el-form-item :label="$t('label.spaceDec')" prop="desc">
              <el-col :span="20">
                  <el-input v-model="addSpaceForm.desc" :placeholder="$t('placeholders.spaceDescription')"></el-input>
              </el-col>
          </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="okEditSpace = false">{{ $t('buttons.cancel') }}</el-button>
          <el-button type="primary" @click="EditSpaceConfirm">
            {{ $t('buttons.confirm') }}
          </el-button>
        </span>
      </template>
    </el-dialog>
    <el-dialog
        v-model="okDeleteSpace"
        width="30%"
        align-center
        >
        <span>{{ $t('messages.deleteSpaceConfirm') }}</span>
        <template #footer>
            <span class="dialog-footer">
            <el-button @click="okDeleteSpace = false">{{ $t('buttons.cancel') }}</el-button>
            <el-button type="primary" @click="ConfirmDeleteSpace">
                {{ $t('buttons.confirm') }}
            </el-button>
            </span>
        </template>
    </el-dialog>
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
        v-model="okquota_exceeded"
        width="30%"
        align-center
        >
        <span>{{ $t('messages.quotaExceeded') }}</span>
    </el-dialog>
</template>

<script>
import { Search,Plus,Delete,Edit } from '@element-plus/icons-vue'
// import { ref, computed } from 'vue';
export default{
    
    components: { Search,Plus,Delete,Edit },
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
            spaces:[
                // {
                //     name: '默认空间',
                //     id: '1',
                //     content: 'Tab 1 content',
                // },
                // {
                //     name: 'Tab 2',
                //     id: '2',
                //     content: 'Tab 2 content',
                // },
            ],
            spacesValue:'',
            loading:false,
            okMonitor:true,
            MonitorSpaceList:[
            //   {id:'',name:'',create_time:'',update_time:''}
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
            EditSpaceID:'',
            okDeleteSpace:false,
            space_id: 1,
            TotalPages: 10,
            queryPage: {
                page:1,
                size:5
            },
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
            okquota_exceeded: false,
            quota_exceeded:false,
            add_space_name:''
        }
    },
    async created(){
        // console.log(sessionStorage.getItem('back_spacesValue'))
        if(sessionStorage.getItem('back_spacesValue') === null) this.spacesValue = 0
        else this.spacesValue = parseInt(sessionStorage.getItem('back_spacesValue'))
        await this.getMonitorSpaceList()
        this.space_id = this.spaces[this.spacesValue].id;
        this.JumpMonitorManage()
    },
    methods:{
        //操作空间（点击删除，增加空间）
        handleTabsEdit(event, tab){
            console.log(event, tab)
            if(tab === 'add'){
                this.addSpace=true
                this.addSpaceForm.name = ''
                this.addSpaceForm.desc = ''
            }
            else if(tab === 'remove'){
                console.log("+++")
                this.DeleteSpace(this.spaces[event].id)
            }
            console.log(this.spacesValue)
        },
        //获取空间信息
        async getMonitorSpaceList(){
            this.spaces = []
            this.loading = true
            const {data: res} = await this.$axios.get('/spaces',
            {
                // params: this.queryPage,
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            this.TotalPages = res.data.total
            console.log(res.data)
            for(let i = 0; i < res.data.items.length; i++){
                this.spaces.push({
                    name: res.data.items[i].name,
                    id: res.data.items[i].id,
                    content: res.data.items[i].desc,
                    index: i
                })
            }
            // this.MonitorSpaceList = res.data.items
            this.loading = false
            console.log(this.MonitorSpaceList)
            // this.JumpMonitorManage()
        },
        //获取某个space下的监控列表
        JumpMonitorManage(val){
            this.space_id=val.id
            window.sessionStorage.setItem('space_id',val.id)
            this.$router.push('/monitor_list')
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
            this.EditSpaceID = row;
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
            this.EditSpaceID = row;
        },
        //确定删除空间
        async ConfirmDeleteSpace(){
            this.okDeleteSpace = false;
            this.loading = true
            const {data: res} = await this.$axios.delete('/space/'+this.EditSpaceID,
            {
                //params:{id: this.EditSpaceID},
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            await this.getMonitorSpaceList();
            this.spacesValue = 0
            this.space_id = this.spaces[0].id;
            this.JumpMonitorManage()
            this.loading = false
        },
        //改变空间
        changeSpace(event){
            console.log(event.index)
            this.space_id = this.spaces[event.index].id;
            this.JumpMonitorManage()
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
        //获得空间页号
        handleCurrentSpaceChange(val){
            this.queryPage.page = val
            this.getMonitorSpaceList()
        },
        //获得空间页数
        handleSizeSpaceChange(val){
            this.queryPage.size = val
            this.getMonitorSpaceList()
        },
        //获取某个space下的监控列表
        async JumpMonitorManage(){
            // this.space_id=sessionStorage.getItem('space_id')
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
            if(this.MonitorList.length > 0){
                if(this.MonitorList[0].quota_exceeded === 1){
                    this.quota_exceeded = true
                    for(let i = 0; i < this.MonitorList.length; i++){
                        this.MonitorList[i].paused = 1
                    }
                }
            }
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
                    this.addMonitorForm.url = ''
                    this.add_space_name = ''
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
            this.addMonitorForm.notification_email = sessionStorage.getItem('email')
            this.addMonitorForm.url = ''
            this.addMonitorForm.trigger_text = ''
            this.addMonitorForm.name = ''
            this.addMonitorForm.time_between_check_days = '0'
            this.addMonitorForm.time_between_check_hours = '1'
            this.addMonitorForm.time_between_check_minutes = '0'
            this.addMonitorForm.time_between_check_seconds = '0'
            this.addMonitorForm.time_between_check_weeks = '0'
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
            if(res.status !== 200){
                this.loading = false
                this.okquota_exceeded = true
                this.quota_exceeded = true
                return  this.$message.error(res.msg)
            }
            this.RefreshMonitorManage(this.space_id)
            this.loading = false
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
            sessionStorage.setItem('back_spacesValue',this.spacesValue)
            sessionStorage.setItem('front','spaces');
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
        //默认新增监控
        async addMonitorUrl(){
            if(this.add_space_name === ''){
                alert("请选择监控标签/空间！");
                return ;
            }
            this.addMonitorForm.desc = ''
            this.addMonitorForm.element = ''
            this.addMonitorForm.include_filters = ''
            this.addMonitorForm.notification_email = sessionStorage.getItem('email')
            this.addMonitorForm.trigger_text = ''
            this.addMonitorForm.name = '默认监控'
            this.addMonitorForm.time_between_check_days = '0'
            this.addMonitorForm.time_between_check_hours = '1'
            this.addMonitorForm.time_between_check_minutes = '0'
            this.addMonitorForm.time_between_check_seconds = '0'
            this.addMonitorForm.time_between_check_weeks = '0'
            this.loading = true
            let data = this.$qs.stringify(this.addMonitorForm)
            const {data: res} = await this.$axios.post('/space/'+this.add_space_name+'/watch',data,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status ===200){
                this.addMonitorForm.url = ''
                this.add_space_name = ''
                this.RefreshMonitorManage(this.space_id)
            }else{
                this.$message.error(res.msg);
            }
            this.loading = false
        },
        //默认新增>编辑
        addMonitor_Edit(){
            if(this.add_space_name === '' || this.addMonitorForm.url === ''){
                alert("请先输入监控网址和选择监控标签/空间！");
                return ;
            }
            this.addMonitor=true;
            this.addMonitorForm.desc = ''
            this.addMonitorForm.element = ''
            this.addMonitorForm.include_filters = ''
            this.addMonitorForm.notification_email = sessionStorage.getItem('email')
            this.addMonitorForm.trigger_text = ''
            this.addMonitorForm.name = '默认监控'
            this.addMonitorForm.time_between_check_days = '0'
            this.addMonitorForm.time_between_check_hours = '1'
            this.addMonitorForm.time_between_check_minutes = '0'
            this.addMonitorForm.time_between_check_seconds = '0'
            this.addMonitorForm.time_between_check_weeks = '0'
            this.value = 'All';
            this.okDisabled = true
        }
    }
}
</script>

<style>
.demo-tabs > .el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
}
.demo-tabs{
    background-color: #ffffff;
}
</style>