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
                    <el-button type="primary"><el-icon><Plus /></el-icon>增加</el-button>
                </div>
            </el-col>
            <el-col :span="2">
                <div>
                    <el-button type="success"><el-icon><Delete /></el-icon>删除</el-button>
                </div>
            </el-col>
        </el-row>
        <el-row>
            <el-table :data="MonitorList" style="width: 100%">
                <el-table-column prop="id" label="ID" width="180" />
                <el-table-column prop="name" label="昵称" width="180" />
                <el-table-column prop="url" label="网址" width="200" />
                <el-table-column prop="create_time" label="创建时间" width="180" />
                <el-table-column prop="update_time" label="更新时间" width="180" />
                <el-table-column prop="last_check_time" label="检查时间" width="180" />
            </el-table>
        </el-row>
      </el-card>
    </div>
</template>
<script>
import { Search,Plus,Delete } from '@element-plus/icons-vue'
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
                name
            }
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
        async JumpMonitorManage(val){
            // this.$router.push('/monitor')
            console.log(val.id)
            this.okMonitor=false
            const {data: res} = await this.$axios.get('/space/${val.id}/watchs')
            if(res.status !== 200) return  this.$message.error(res.msg)
            // this.total=res.data
            this.MonitorList = res.data
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