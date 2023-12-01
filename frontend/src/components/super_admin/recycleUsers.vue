<template>
    <div>
      <el-breadcrumb>
          <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>用户回收</el-breadcrumb-item>
      </el-breadcrumb>
      <el-card>
          <el-row>
              <el-col :span="2">
                  <div>
                      <el-button type="success" @click="RestoreUsers"><el-icon><RefreshLeft /></el-icon>批量恢复</el-button>
                  </div>
              </el-col>
              <el-col :span="4">
                  <div>
                      <el-button type="danger" @click="DeleteUsers"><el-icon><Delete /></el-icon>批量删除</el-button>
                  </div>
              </el-col>
          </el-row>
          <el-row>
              <el-table v-loading="loading" :data="UserList" style="width: 100%" @selection-change="handleSelectionUserChange">
                  <el-table-column type="selection" width="55" />
                  <el-table-column prop="id" label="ID" width="50" />
                  <el-table-column prop="nickname" label="昵称" width="100" />
                  <el-table-column prop="email" label="邮箱" width="200" />
                  <el-table-column prop="role" label="权限" width="200" />
                  <el-table-column prop="update_time" label="更改时间" width="200" />
                  <el-table-column prop="spaces" label="空间数" width="100" />
                  <el-table-column prop="edit" label="Edit" width="300">
                      <template #default="scope">
                          <el-button size="small" @click="RestoreUser(scope.row)"
                          >恢复</el-button
                          >
                          <el-button
                          size="small"
                          type="danger"
                          @click="DeleteUser(scope.row)"
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
                    @size-change="handleSizeUserChange"
                    @current-change="handleCurrentUserChange"
                    />
          </el-row>
      </el-card>
    <el-dialog
            v-model="okDeleteUser"
            width="30%"
            align-center
            >
            <span>是否永久删除用户？</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okDeleteUser = false">取消</el-button>
                <el-button type="primary" @click="ConfirmDeleteUser">
                    确定
                </el-button>
                </span>
            </template>
        </el-dialog>
    <el-dialog
            v-model="okDeleteUsers"
            width="30%"
            align-center
            title="温馨提示"
            >
            <span>你确定要永久删除选中项吗？</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okDeleteUsers = false">取消</el-button>
                <el-button type="primary" @click="ConfirmDeleteUsers">
                    确定
                </el-button>
                </span>
            </template>
        </el-dialog>
    <el-dialog
            v-model="okRestoreUser"
            width="30%"
            align-center
            title="温馨提示"
            >
            <span>是否恢复用户？</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okRestoreUser = false">取消</el-button>
                <el-button type="primary" @click="ConfirmRestoreUser">
                    确定
                </el-button>
                </span>
            </template>
        </el-dialog>
    <el-dialog
            v-model="okRestoreUsers"
            width="30%"
            align-center
            title="温馨提示"
            >
            <span>你确定要恢复选中项吗？</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okRestoreUsers = false">取消</el-button>
                <el-button type="primary" @click="ConfirmRestoreUsers">
                    确定
                </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
  </template>
  <script>
  import { Search,Plus,Delete,RefreshLeft } from '@element-plus/icons-vue'
  import { ref, computed } from 'vue';
  export default{
      
      components: { Search,Plus,Delete,RefreshLeft },
      data(){
        const validEmail = (rule, value, callback) => {
            const EmailReg = /^^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$/
            if(EmailReg.test(value)){
                return callback()
            }
            return callback(new Error('请输入正确的邮箱'))
        }
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
              UserList:[
                {id:'123',nickname:'test',email:'2968035007@qq.com',update_time:'2023/11/27'}
              ],
              EditUserID:'',
              okDeleteUser:false,
              UserID:'',
              selectUserRows:'',
              okDeleteUsers:false,
              space_id: 1,
              loading: false,
              TotalPages: 10,
              queryPage: {
                email:'',
                nickname:'',
                page:1,
                size:5
              },
              okRestoreUsers:false,
              RestoreUserID:'',
              okRestoreUser:false
          }
      },
      created(){
          this.getUserList()
        //   this.getBookmark()
      },
      methods:{
          //获取用户列表
          async getUserList(){
              this.loading = true

              const {data: res} = await this.$axios.get('/users/softdelete',
              {
                  params: this.queryPage,
                  headers : {
                      'token': sessionStorage.getItem('token')
                  }
              })
              if(res.status !== 200) return  this.$message.error(res.msg)
              this.$message.success(res.msg)
              this.TotalPages = res.data.total
              
              this.UserList = res.data.items
              this.loading = false
              for(let i = 0; i < this.UserList.length; i++){
                if(this.UserList[i].role === 0){
                    this.UserList[i].role = "普通用户"
                }else{
                    this.UserList[i].role = "管理员"
                }
              }
              console.log(this.UserList)
          },
          //触发删除用户按钮
          DeleteUser(row){
            this.okDeleteUser = true;
            this.EditUserID = row.id;
          },
          //确定删除单个用户
          async ConfirmDeleteUser(){
            this.okDeleteUser = false;
            this.loading = true
            const {data: res} = await this.$axios.delete('/user/' + this.EditUserID + '/delete',
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.getUserList();
            this.loading = false
          },
          handleSelectionUserChange(row){
            this.selectUserRows = row
          },
          //触发批量删除用户按钮
          DeleteUsers(){
            console.log(this.selectUserRows.length)
            if(this.selectUserRows.length > 0){
                this.okDeleteUsers = true;
            }
          },
          //确定批量删除多个用户
          ConfirmDeleteUsers(){
            for(let i = 0; i < this.selectUserRows.length; i++){
                this.DeleteUser(this.selectUserRows[i])
                this.ConfirmDeleteUser()
            }
            this.getUserList()
            this.okDeleteUsers = false;
          },
          //触发恢复用户按钮
          RestoreUser(value){
            this.okRestoreUser = true;
            this.RestoreUserID = value.id
          },
          //确定恢复单个用户
          async ConfirmRestoreUser(){
            this.okRestoreUser = false;
            this.loading = true
            let data = sessionStorage.getItem('token')
            const {data: res} = await this.$axios.put('/user/' + this.RestoreUserID + '/restore',data,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.getUserList();
            this.loading = false
          },
          //触发恢复多个用户
          RestoreUsers(){
            if(this.selectUserRows.length > 0){
                this.okRestoreUsers = true;
            }
          },
          //确定批量恢复多个用户
          ConfirmRestoreUsers(){
            for(let i = 0; i < this.selectUserRows.length; i++){
                this.RestoreUser(this.selectUserRows[i])
                this.ConfirmRestoreUser()
            }
            this.getUserList()
            this.okRestoreUsers = false;
          },
        //获得用户页号
        handleCurrentUserChange(val){
            this.queryPage.page = val
            this.getUserList()
        },
        //获得用户页数
        handleSizeUserChange(val){
            this.queryPage.size = val
            this.getUserList()
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