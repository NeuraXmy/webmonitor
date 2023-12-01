<template>
    <div>
      <el-breadcrumb>
          <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>空间管理</el-breadcrumb-item>
      </el-breadcrumb>
      <el-card>
          <el-row>
              <el-col :span="2">
                  <div>
                      <el-button type="success" @click="RestoreSpaces"><el-icon><RefreshLeft /></el-icon>批量恢复</el-button>
                  </div>
              </el-col>
              <el-col :span="4">
                  <div>
                      <el-button type="danger" @click="DeleteSpaces"><el-icon><Delete /></el-icon>批量删除</el-button>
                  </div>
              </el-col>
          </el-row>
          <el-row>
              <el-table v-loading="loading" :data="MonitorSpaceList" style="width: 100%" @selection-change="handleSelectionSpacesChange">
                  <el-table-column type="selection" width="55" />
                  <el-table-column prop="id" label="ID" width="50" />
                  <el-table-column prop="owner_email" label="邮箱" width="200" />
                  <el-table-column prop="name" label="空间名" width="100" />
                  <el-table-column prop="desc" label="空间描述" width="300" />
                  <el-table-column prop="update_time" label="更新时间" width="200" />
                  <el-table-column prop="edit" label="Edit" width="200">
                      <template #default="scope">
                          <el-button size="small" @click="RestoreSpace(scope.row)"
                          >恢复</el-button
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
              <el-pagination
                    v-model:current-page="queryPage.page"
                    v-model:page-size="queryPage.size"
                    :page-sizes="[5, 10, 20, 50]"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="TotalPages"
                    @size-change="handleSizeSpaceChange"
                    @current-change="handleCurrentSpaceChange"
                    />
          </el-row>
      </el-card>
    <el-dialog
            v-model="okDeleteSpace"
            width="30%"
            align-center
            >
            <span>是否永久删除监控？</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okDeleteSpace = false">取消</el-button>
                <el-button type="primary" @click="ConfirmDeleteSpace">
                    确定
                </el-button>
                </span>
            </template>
        </el-dialog>
    <el-dialog
            v-model="okDeleteSpaces"
            width="30%"
            align-center
            title="温馨提示"
            >
            <span>你确定要永久删除选中项吗？</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okDeleteSpaces = false">取消</el-button>
                <el-button type="primary" @click="ConfirmDeleteSpaces">
                    确定
                </el-button>
                </span>
            </template>
        </el-dialog>
    <el-dialog
            v-model="okRestoreSpace"
            width="30%"
            align-center
            title="温馨提示"
            >
            <span>是否恢复空间？</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okRestoreSpace = false">取消</el-button>
                <el-button type="primary" @click="ConfirmRestoreSpace">
                    确定
                </el-button>
                </span>
            </template>
        </el-dialog>
    <el-dialog
            v-model="okRestoreSpaces"
            width="30%"
            align-center
            title="温馨提示"
            >
            <span>你确定要恢复选中项吗？</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okRestoreSpaces = false">取消</el-button>
                <el-button type="primary" @click="ConfirmRestoreSpaces">
                    确定
                </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
  </template>
  <script>
  import { Search,Plus,Delete,RefreshLeft } from '@element-plus/icons-vue'
//   import { ref, computed } from 'vue';
  export default{
      
      components: { Search,Plus,Delete,RefreshLeft },
      data(){
          return {
              okMonitor:true,
              MonitorSpaceList:[
                  {id:'12',name:'test',create_time:'test',update_time:'test'}
              ],
              okDeleteSpace:false,
              space_id: 1,
              loading: false,
              TotalPages: 10,
              queryPage: {
                page:1,
                size:5
              },
              UserID:'',
              selectSpacesRows:'',
              okDeleteSpaces:false,
              okRestoreSpaces:false,
              RestoreSpaceID:'',
              okRestoreSpace:false
          }
      },
      created(){
          this.getMonitorSpaceList()
      },
      methods:{
          async getMonitorSpaceList(){
              this.loading = true
              const {data: res} = await this.$axios.get('/spaces/softdelete',
              {
                  params: this.queryPage,
                  headers : {
                      'token': sessionStorage.getItem('token')
                  }
              })
              if(res.status !== 200) return  this.$message.error(res.msg)
              this.$message.success(res.msg)
              console.log(res);
              this.TotalPages = res.data.total
              
              this.MonitorSpaceList = res.data.items
              this.loading = false
              console.log(this.MonitorSpaceList)
          },
          //获取某个space下的监控列表
          JumpMonitorManage(val){
              this.space_id=val.id
              window.sessionStorage.setItem('space_id',val.id)
              this.$router.push('/monitorlist')
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
        handleSelectionSpacesChange(row){
            this.selectSpacesRows = row
        },
        //触发批量删除空间按钮
        DeleteSpaces(){
            console.log(this.selectSpacesRows.length)
            if(this.selectSpacesRows.length > 0){
                this.okDeleteSpaces = true;
            }
        },
        //确定批量删除多个空间
        ConfirmDeleteSpaces(){
            for(let i = 0; i < this.selectSpacesRows.length; i++){
                this.DeleteSpace(this.selectSpacesRows[i])
                this.ConfirmDeleteSpace()
            }
            this.getMonitorSpaceList()
            this.okDeleteSpaces = false;
        },
        //触发恢复空间按钮
        RestoreSpace(value){
            this.okRestoreSpace = true;
            this.RestoreSpaceID = value.id
        },
        //确定恢复单个空间
        async ConfirmRestoreSpace(){
            this.okRestoreSpace = false;
            this.loading = true
            let data = sessionStorage.getItem('token')
            const {data: res} = await this.$axios.put('/space/' + this.RestoreSpaceID + '/restore',data,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.getMonitorSpaceList();
            this.loading = false
        },
        //触发恢复多个空间
        RestoreSpaces(){
            if(this.selectSpacesRows.length > 0){
                this.okRestoreSpaces = true;
            }
        },
        //确定批量恢复多个空间
        ConfirmRestoreSpaces(){
            for(let i = 0; i < this.selectSpacesRows.length; i++){
                this.RestoreSpace(this.selectSpacesRows[i])
                this.ConfirmRestoreSpace()
            }
            this.getMonitorSpaceList()
            this.okRestoreSpaces = false;
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