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
            <el-pagination
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
            />
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
            <!-- <el-col :span="2">
                <div>
                    <el-button type="success"><el-icon><Delete /></el-icon>删除</el-button>
                </div>
            </el-col> -->
        </el-row>
        <el-row>
            <el-table :data="MonitorList" style="width: 100%">
                <el-table-column prop="id" label="ID" width="180" />
                <el-table-column prop="name" label="昵称" width="180" />
                <el-table-column prop="url" label="网址" width="200" />
                <el-table-column prop="create_time" label="创建时间" width="180" />
                <el-table-column prop="update_time" label="更新时间" width="180" />
                <el-table-column prop="last_check_time" label="检查时间" width="180" />
                <el-table-column prop="edit" label="Edit" width="140">
                    <template #default="scope">
                        <!-- <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
                        >Edit</el-button
                        > -->
                        <el-button
                        size="small"
                        type="danger"
                        @click="DeleteWatch(scope.row)"
                        >Delete</el-button
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
                <el-form-item label="刷新时间">
                    <el-col :span="4">
                        <!-- <el-input v-model="addMonitorForm.update_time" disabled></el-input> -->
                        <el-input v-model="addMonitorForm.time_between_check_weeks" placeholder="周"></el-input>
                    </el-col>
                    <el-col :span="4">
                        <!-- <el-input v-model="addMonitorForm.update_time" disabled></el-input> -->
                        <el-input v-model="addMonitorForm.time_between_check_days" placeholder="天"></el-input>
                    </el-col>
                    <el-col :span="4">
                        <!-- <el-input v-model="addMonitorForm.update_time" disabled></el-input> -->
                        <el-input v-model="addMonitorForm.time_between_check_hours" placeholder="时"></el-input>
                    </el-col>
                    <el-col :span="4">
                        <!-- <el-input v-model="addMonitorForm.update_time" disabled></el-input> -->
                        <el-input v-model="addMonitorForm.time_between_check_minutes" placeholder="分"></el-input>
                    </el-col>
                    <el-col :span="4">
                        <!-- <el-input v-model="addMonitorForm.update_time" disabled></el-input> -->
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
                    id:'1',name:'1',create_time:'1',update_time:'1'
                },
                {
                    id:'2',name:'1',create_time:'1',update_time:'1'
                },
                {
                    id:'3',name:'1',create_time:'1',update_time:'1'
                },
                {
                    id:'4',name:'1',create_time:'1',update_time:'1'
                },
                {
                    id:'5',name:'1',create_time:'1',update_time:'1'
                }
            ],
            MonitorList:[
                {
                    id:'1',name:'1',url:'https://www.baidu.com/',create_time:'1',update_time:'1',last_check_time:'1'
                },
                {
                    id:'2',name:'1',url:'https://www.baidu.com/',create_time:'1',update_time:'1',last_check_time:'1'
                },
                {
                    id:'3',name:'1',url:'https://www.baidu.com/',create_time:'1',update_time:'1',last_check_time:'1'
                },
                {
                    id:'4',name:'1',url:'https://www.baidu.com/',create_time:'1',update_time:'1',last_check_time:'1'
                },
                {
                    id:'5',name:'1',url:'https://www.baidu.com/',create_time:'1',update_time:'1',last_check_time:'1'
                }
            ],
            queryInfo:{
                name:'',
                pnum:1,
                psize:2
            },
            total:5,
            addSpace:false,
            addSpaceForm:{
                name:''
            },
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
                notification_email:''
            },
            options_weeks:[
                {value: 7,label: 'Guide'},
                {value: 'guide',label: 'Guide'},
            ]
        }
    },
    created(){
        // this.getMonitorSpaceList()
    },
    methods:{
        async getMonitorSpaceList(){
            // const {data: res} = await this.$axios.get('/spaces', {params: this.queryInfo})
            const {data: res} = await this.$axios.get('/spaces')
            console.log(res)
            if(res.status !== 200) return  this.$message.error(res.msg)
            window.sessionStorage.setItem('token',res.data.token)
            this.$message.success(res.message)
            // this.total=res.data
            this.MonitorSpaceList = res.data
        },
        handleSizeChange(val){
            this.queryInfo.psize = val
            this.getMonitorSpaceList()
            console.log(val);
        },
        handleCurrentChange(val){
            this.queryInfo.pnum = val
            console.log(val);
            this.getMonitorSpaceList()
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
            // this.$router.push('/monitor')
            console.log(val.id)
            this.okMonitor=false
            const {data: res} = await this.$axios.get('/space/${val.id}/watches')
            if(res.status !== 200) return  this.$message.error(res.msg)
            // this.total=res.data
            this.MonitorList = res.data
        },
        async addMonitorList(){
            this.addMonitor=false
            const {data: res} = await this.$axios.post('/space/${val.id}/watch',this.$qs.stringify(this.addMonitorForm))
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
        async DeleteWatch(row){
            console.log(row.id)
            const {data: res} = await this.$axios.del('/watch/${row.id}',{data: {id: row.id}})
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.JumpMonitorManage()
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