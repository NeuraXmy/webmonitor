<template>
  <div v-if="okMonitor">
    <el-breadcrumb :separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>任务管理</el-breadcrumb-item>
        <el-breadcrumb-item>监控空间列表</el-breadcrumb-item>
        <!-- <el-breadcrumb-item>promotion detail</el-breadcrumb-item> -->  
    </el-breadcrumb>
    <el-card>
        <el-row>
            <el-col :span="12">
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
            </el-col>
            <el-col :span="12">
                <div>
                    <el-button type="primary" :icon="Plus" @click="addSpace=true"><el-icon><Plus /></el-icon>新增空间</el-button>
                    
                </div>
                <el-col :span="2">
            </el-col>
            </el-col>
        </el-row>
        <el-row>
            <el-table :data="MonitorSpaceList" style="width: 100%">
                <el-table-column prop="id" label="ID" width="180" />
                <el-table-column prop="name" label="昵称" width="180" />
                <el-table-column prop="create_time" label="创建时间" width="180" />
                <el-table-column prop="update_time" label="更新时间" width="180" />
                <el-table-column prop="edit" label="Edit" width="280">
                    <template #default="scope">
                        <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
                        >Edit</el-button
                        >
                        <el-button
                        size="small"
                        type="danger"
                        @click="handleDelete(scope.$index, scope.row)"
                        >Delete</el-button
                        >
                        <el-button size="small" @click="JumpMonitorManage(scope.row)"
                        >Check</el-button
                        >
                    </template>
                </el-table-column>
            </el-table>
        </el-row>
            <!-- <el-pagination
            v-model:current-page="queryInfo.pnum" 
            v-model:page-size="queryInfo.psize"
            :page-sizes="[1, 2, 5, 10]"
            :small="small"
            :disabled="disabled"
            :background="background"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            /> -->
    </el-card>
    <el-dialog
    v-model="addSpace"
    title="新增空间"
    width="40%"
    :before-close="handleClose"
  >
    <el-form ref="addSpaceRef" :rules="addSpaceRules" :model="addSpaceForm" label-width="80px" class="form_style">
        <el-form-item label="昵称">
            <el-col :span="20">
                <el-input v-model="addSpaceForm.name" placeholder="请输入昵称"></el-input>
            </el-col>
        </el-form-item>
    </el-form>
    <!-- <span>....</span> -->
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="addSpace = false">Cancel</el-button>
        <el-button type="primary" @click="addSpaceList">
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>
  </div>
  <div v-if="!okMonitor">
      <el-breadcrumb :separator-class="el-icon-arrow-right">
          <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>任务管理</el-breadcrumb-item>
          <el-breadcrumb-item @click="this.okMonitor=true">监控空间列表</el-breadcrumb-item>
          <el-breadcrumb-item>空间监控管理</el-breadcrumb-item>
          <!-- <el-breadcrumb-item>promotion detail</el-breadcrumb-item> -->
      </el-breadcrumb>
      <el-card>
        <el-row>
            <el-col :span="2">
                <div>
                    <el-button type="primary" @click="addMonitorListener"><el-icon><Plus /></el-icon>增加</el-button>
                </div>
            </el-col>
            <el-col :span="2">
                <div>
                    <!-- <el-button type="primary" @click="addMonitorUrl" ><el-icon><Plus /></el-icon>增加网页</el-button> -->
                    <!-- <el-button type="primary" @dragstart="handleDragStart" draggable="true" ><el-icon><Plus /></el-icon>增加网页</el-button> -->
                    <a :href='generateUrl' title="将我拖动到书签栏">拖到书签栏</a>
                    <!-- <button draggable="true" @dragstart="onBookmarkDragStart">小书签</button> -->

                </div>
            </el-col>
            <!-- <el-col :span="2">
                <div>
                    <el-button type="success"><el-icon><Delete /></el-icon>删除</el-button>
                </div>
            </el-col> -->
        </el-row>
        <el-row>
            <el-table :data="MonitorList" style="width: 100%">
                <el-table-column prop="id" label="ID" width="50" />
                <el-table-column prop="name" label="昵称" width="100" />
                <el-table-column prop="url" label="网址" width="250" />
                <el-table-column prop="create_time" label="创建时间" width="200" />
                <el-table-column prop="update_time" label="更新时间" width="200" />
                <el-table-column prop="last_check_time" label="检查时间" width="200" />
                <el-table-column prop="edit" label="Edit" width="240">
                    <template #default="scope">
                        <el-button size="small" @click="WatchEdit(scope.row)"
                        >Edit</el-button
                        >
                        <el-button
                        size="small"
                        type="danger"
                        @click="DeleteWatch(scope.row)"
                        >Delete</el-button
                        >
                        <el-button
                        size="small"
                        type="info"
                        @click="RefreshWatch(scope.row)"
                        >Refresh</el-button
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
            :before-close="handleClose"
        >
            <!-- <el-form ref="addMonitorRef" :rules="addMonitorRules" :model="addMonitorForm" label-width="80px" class="form_style"> -->
            <el-form :model="addMonitorForm" label-width="80px" class="form_style">
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
                        <el-select v-model="this.addMonitorForm.include_filters" placeholder="Select" size="large">
                            <el-option
                            v-for="item in options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                            />
                        </el-select>
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
            :before-close="handleClose"
        >
            <!-- <el-form ref="addMonitorRef" :rules="addMonitorRules" :model="addMonitorForm" label-width="80px" class="form_style"> -->
            <el-form :model="addMonitorForm" label-width="80px" class="form_style">
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
                        <el-select v-model="addMonitorForm.include_filters" placeholder="Select" size="large">
                            <el-option
                            v-for="item in options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                            />
                        </el-select>
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
                <el-form-item label="通知邮箱">
                    <el-col :span="20">
                        <el-input v-model="addMonitorForm.notification_email"></el-input>
                    </el-col>
                </el-form-item>
            </el-form>
            <!-- <span>....</span> -->
            <template #footer>
            <span class="dialog-footer">
                <el-button @click="EditMonitor = false">Cancel</el-button>
                <el-button type="primary" @click="WatchEditConfirm">
                Confirm
                </el-button>
            </span>
            </template>
        </el-dialog>
    </div>
</template>
<script>
import { Search,Plus,Delete } from '@element-plus/icons-vue'
import { ref, computed } from 'vue';
export default{
    
    components: { Search,Plus,Delete },
    data(){
        return {
            okMonitor:true,
            MonitorSpaceList:[
                {
                    id:1,name:'1',create_time:'1',update_time:'1'
                },
                {
                    id:2,name:'1',create_time:'1',update_time:'1'
                },
                {
                    id:3,name:'1',create_time:'1',update_time:'1'
                },
                {
                    id:4,name:'1',create_time:'1',update_time:'1'
                },
                {
                    id:5,name:'1',create_time:'1',update_time:'1'
                }
            ],
            MonitorList:[
                {
                    id:1,name:'1',url:'https://www.baidu.com/',create_time:'1',update_time:'1',last_check_time:'1'
                },
                {
                    id:2,name:'1',url:'https://www.baidu.com/',create_time:'1',update_time:'1',last_check_time:'1'
                },
                {
                    id:3,name:'1',url:'https://www.baidu.com/',create_time:'1',update_time:'1',last_check_time:'1'
                },
                {
                    id:4,name:'1',url:'https://www.baidu.com/',create_time:'1',update_time:'1',last_check_time:'1'
                },
                {
                    id:5,name:'1',url:'https://www.baidu.com/',create_time:'1',update_time:'1',last_check_time:'1'
                }
            ],
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
                    value: 'JSON',
                    label: 'JSON',
                }
            ],
            queryInfo:{
                name:''
                // ,
                // pnum:1,
                // psize:2
            },
            // total:5,
            addSpace:false,
            addSpaceForm:{
                name:''
            },
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
                include_filters:''
            },
            space_id:1,
            watch_id:1,
            EditMonitor:false,
            generateUrl:''
        }
    },
    created(){
        this.getMonitorSpaceList()
        //书签的url
        const filePath = '../embed/inject_js.txt';
        try {
            const response = fetch(filePath);
            const data = response.text();
            this.generateUrl = data;
        } catch (error) {
            console.error(error);
        }
        console.log(this.generateUrl)
    },
    methods:{
        async getMonitorSpaceList(){
            console.log(sessionStorage.getItem('token'))
            const {data: res} = await this.$axios.get('/spaces',
            {
                // params:{},
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.message)
            // this.total=res.data
            this.MonitorSpaceList = res.data
        },
        //根据昵称搜索空间
        searchSpace(){
            this.queryInfo.pnum = 1
            this.getMonitorSpaceList();
        },
        //新增空间
        async addSpaceList(){
            this.addSpace=false
            // const {data: res} = await this.$axios.get('/space/')
        },
        //获取某个space下的监控列表
        async JumpMonitorManage(val){
            
            this.space_id=val.id
            
            this.okMonitor=false
            const {data: res} = await this.$axios.get('/space/'+val.id+'/watches',
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            
            this.MonitorList = res.data
        },
        //用户在某个space下创建监控
        async addMonitorList(){
            this.addMonitor=false
            // let data={
            //     'token': sessionStorage.getItem('token')
            // }
            let data = this.$qs.stringify(this.addMonitorForm)
            const {data: res} = await this.$axios.post('/space/'+this.space_id+'/watch',data,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            
            this.JumpMonitorManage()
        },
        addMonitorListener(){
            this.addMonitor=true
            const currentTime = ref(new Date());
            // 使用 computed 属性来实时更新时间
            const updateTime = computed(() => {
            currentTime.value = new Date();
            });
            console.log(currentTime)
            this.addMonitorForm.create_time=currentTime
            this.addMonitorForm.update_time=currentTime
            this.addMonitorForm.last_check_time=currentTime
        },
        //用户删除监控
        async DeleteWatch(row){
            const {data: res} = await this.$axios.delete('/watch/'+row.id,
            {
                params:{id: row.id},
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.JumpMonitorManage()
        },
        //触发用户修改监控,保存watch_id
        WatchEdit(row){
            this.EditMonitor=true;
            this.watch_id=row.id;
        },
        //用户修改监控
        async WatchEditConfirm(){
            const {data: res} = await this.$axios.put('/watch/'+this.watch_id,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            
            this.JumpMonitorManage()
        },
        //用户立刻刷新监控
        async RefreshWatch(row){
            
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
            
            this.JumpMonitorManage()
        },
        addMonitorUrl(){
            
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