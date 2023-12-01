<template>
    <div>
        <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>监控管理</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
          <el-row>
            <el-col :span="2">
                  <div>
                      <el-button type="success" @click="RestoreMonitors"><el-icon><RefreshLeft /></el-icon>批量恢复</el-button>
                  </div>
              </el-col>
              <el-col :span="4">
                  <div>
                      <el-button type="danger" @click="DeleteMonitors"><el-icon><Delete /></el-icon>批量删除</el-button>
                  </div>
              </el-col>
          </el-row>
          <el-row>
              <el-table v-loading="loading" :data="MonitorList" style="width: 100%" @selection-change="handleSelectionMonitorsChange">
                  <el-table-column type="selection" width="50" />
                  <el-table-column prop="id" label="ID" width="50" />
                  <el-table-column prop="notification_email" label="邮箱" width="180" />
                  <el-table-column prop="name" label="监控名" width="150" />
                  <el-table-column prop="url" label="网址" width="220" />
                  <el-table-column prop="last_check_time" label="检查时间" width="170" />
                  <el-table-column prop="last_check_state" label="检查状态" width="200" />
                  <el-table-column prop="edit" label="Edit" width="200">
                      <template #default="scope">
                         <el-button size="small" @click="RestoreMonitor(scope.row)"
                          >恢复</el-button
                          >
                          <el-button
                          size="small"
                          type="danger"
                          @click="DeleteWatch(scope.row)"
                          >删除</el-button
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
            v-model="okDeleteMonitors"
            width="30%"
            align-center
            title="温馨提示"
            >
            <span>你确定要删除选中项吗？</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okDeleteMonitors = false">取消</el-button>
                <el-button type="primary" @click="ConfirmDeleteMonitors">
                    确定
                </el-button>
                </span>
            </template>
        </el-dialog>
        <el-dialog
            v-model="okRestoreMonitor"
            width="30%"
            align-center
            title="温馨提示"
            >
            <span>是否恢复监控？</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okRestoreMonitor = false">取消</el-button>
                <el-button type="primary" @click="ConfirmRestoreMonitor">
                    确定
                </el-button>
                </span>
            </template>
        </el-dialog>
        <el-dialog
            v-model="okRestoreMonitors"
            width="30%"
            align-center
            title="温馨提示"
            >
            <span>你确定要恢复选中项吗？</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okRestoreMonitors = false">取消</el-button>
                <el-button type="primary" @click="ConfirmRestoreMonitors">
                    确定
                </el-button>
                </span>
            </template>
        </el-dialog>
      </div>
  </template>
  <script>
  import { Search,Plus,Delete,RefreshLeft } from '@element-plus/icons-vue'
  export default{
      
      components: { Search,Plus,Delete,RefreshLeft },
      data(){
          return {
              MonitorList:[
                //   {id:'',name:'',url:'',create_time:'',update_time:'',last_check_time:''}
              ],
              space_id: 1,
              watch_id: 1,
              EditMonitor: false,
              generateUrl: '',
              okDeleteWatch: false,
              DeleteWatchID: '',
              okDisabled: false,
              loading: false,
              TotalPages: 10,
              queryPage: {
                page:1,
                size:5
              },
              selectMonitorsRows:'',
              okDeleteMonitors:false,
              queryMonitor:{
                url:'',
                name:''
              },
              okRestoreMonitors:false,
              RestoreMonitorID:'',
              okRestoreMonitor:false
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
              console.log("11111")
              const {data: res} = await this.$axios.get('/watches/softdelete',
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
            //   this.RefreshMonitorManage(this.space_id)
              this.JumpMonitorManage()
              this.loading = false
          },
          DeleteWatch(row){
            this.okDeleteWatch = true;
            this.DeleteWatchID = row.id;
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
            this.JumpMonitorManage()
            this.okDeleteMonitors = false;
        },
        //获得监控页号
        handleCurrentMonitorChange(val){
            this.queryPage.page = val
            this.JumpMonitorManage()
        },
        //获得监控页数
        handleSizeMonitorChange(val){
            this.queryPage.size = val
            this.JumpMonitorManage()
        },
        async searchMonitor(){
            this.loading = true
            const {data: res} = await this.$axios.get('/watches/search',this.queryMonitor,
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
        //触发恢复监控按钮
        RestoreMonitor(value){
            this.okRestoreMonitor = true;
            this.RestoreMonitorID = value.id
        },
        //确定恢复单个监控
        async ConfirmRestoreMonitor(){
            this.okRestoreMonitor = false;
            this.loading = true
            let data = sessionStorage.getItem('token')
            const {data: res} = await this.$axios.put('/watch/' + this.RestoreMonitorID + '/restore',data,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.JumpMonitorManage();
            this.loading = false
        },
        //触发恢复多个监控
        RestoreMonitors(){
            if(this.selectMonitorsRows.length > 0){
                this.okRestoreMonitors = true;
            }
        },
        //确定批量恢复多个监控
        ConfirmRestoreMonitors(){
            for(let i = 0; i < this.selectMonitorsRows.length; i++){
                this.RestoreMonitor(this.selectMonitorsRows[i])
                this.ConfirmRestoreMonitor()
            }
            this.JumpMonitorManage()
            this.okRestoreMonitors = false;
        },
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