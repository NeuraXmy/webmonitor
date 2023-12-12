<template>
    <div>
      <el-breadcrumb>
          <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      </el-breadcrumb>
      <el-card>
          <el-row>
            <el-col :span="10">
                <!-- <el-input
                v-model="queryPage.email"
                placeholder="请输入邮箱"
                class="input-with-select"
                >
                <template #append>
                    <el-button @click="searchUser"><el-icon><Search /></el-icon></el-button>
                </template>
                </el-input> -->
                <el-input
                    v-model="searchValue"
                    placeholder="请输入"
                    class="input-with-select"
                    >
                    <template #prepend>
                        <el-select v-model="selectValue" placeholder="Select" style="width: 115px">
                        <el-option label="昵称" value="1" />
                        <el-option label="邮箱" value="2" />
                        </el-select>
                    </template>
                    <template #append>
                        <el-button @click="searchUser"><el-icon><Search /></el-icon></el-button>
                    </template>
                    </el-input>
              </el-col>
              <el-col :span="2">
                  <div>
                      <el-button type="primary" @click="addUser=true, this.addUserForm.role = '0'"><el-icon><Plus /></el-icon>新增用户</el-button>
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
                          <!-- <el-button size="small" @click="JumpMonitorManage(scope.row)"
                          >进入</el-button
                          > -->
                          <el-button size="small" @click="EditUser(scope.row)"
                          >编辑</el-button
                          >
                          <el-button
                          size="small"
                          type="danger"
                          @click="DeleteUser(scope.row)"
                          >删除</el-button
                          >
                          <el-button size="small" @click="EnterSpace(scope.row)"
                          >查看空间</el-button
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
      v-model="addUser"
      title="新增用户"
      width="40%"
    >
      <el-form ref="addUserRef" :rules="addUserRules" :model="addUserForm" label-width="80px" class="form_style">
          <el-form-item label="昵称" prop="nickname">
              <el-col :span="20">
                  <el-input v-model="addUserForm.nickname" placeholder="请输入昵称"></el-input>
              </el-col>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
              <el-col :span="20">
                  <el-input v-model="addUserForm.email" placeholder="请输入邮箱"></el-input>
              </el-col>
          </el-form-item>
          <el-form-item label="密码" prop="password">
              <el-col :span="20">
                  <el-input show-password v-model="addUserForm.password" placeholder="请输入密码"></el-input>
              </el-col>
          </el-form-item>
          <el-form-item label="权限" prop="role">
              <el-col :span="20">
                <el-select v-model="this.addUserForm.role" placeholder="Select" size="large" @change="ChangeRole">
                    <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                    />
                </el-select>
            </el-col>
          </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addUser = false">取消</el-button>
          <el-button type="primary" @click="addUserList">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
    <el-dialog
      v-model="okEditUser"
      title="编辑用户"
      width="40%"
    >
    <el-form ref="addUserRef" :rules="addUserRules" :model="addUserForm" label-width="80px" class="form_style">
          <el-form-item label="昵称" prop="nickname">
              <el-col :span="20">
                  <el-input v-model="addUserForm.nickname" placeholder="请输入昵称"></el-input>
              </el-col>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
              <el-col :span="20">
                  <el-input disabled v-model="addUserForm.email" placeholder="请输入邮箱"></el-input>
              </el-col>
          </el-form-item>
          <el-form-item label="密码" prop="password">
              <el-col :span="20">
                  <el-input show-password v-model="addUserForm.password" placeholder="请输入密码"></el-input>
              </el-col>
          </el-form-item>
          <el-form-item label="权限" prop="role">
              <el-col :span="20">
                <el-select v-model="addUserForm.role" placeholder="Select" size="large" @change="ChangeRole">
                    <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                    />
                </el-select>
            </el-col>
          </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="okEditUser = false">取消</el-button>
          <el-button type="primary" @click="EditUserConfirm">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
    <el-dialog
            v-model="okDeleteUser"
            width="30%"
            align-center
            >
            <span>是否删除用户？</span>
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
            <span>你确定要删除选中项吗？</span>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="okDeleteUsers = false">取消</el-button>
                <el-button type="primary" @click="ConfirmDeleteUsers">
                    确定
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
              addUser:false,
              addUserForm:{
                nickname:'',
                email:'',
                password:'',
                role:0
              },
              addUserRules:{
                email:[
                    {required:true, validator: validEmail, trigger:'blur'}
                ],
                password:[
                    { message: '请输入密码', trigger:'blur'}
                ],
                nickname:[
                    {required:true, min:2,  message: '昵称长度不能小于2位', trigger:'blur'}
                ],
                role:[
                    {required:true, trigger:'blur'}
                ]
              },
              EditUserID:'',
              okEditUser:false,
              okDeleteUser:false,
              UserID:'',
              options:[
                  {
                      value: '1',label: '管理员',
                  },
                  {
                      value: '0',label: '普通用户',
                  }
              ],
              selectUserRows:'',
              okDeleteUsers:false,

              space_id: 1,
              loading: false,
              iframe_url: '',
              TotalPages: 10,
              queryPage: {
                email:'',
                nickname:'',
                page:1,
                size:10
              },
              searchValue:'',
              selectValue:''
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

              const {data: res} = await this.$axios.get('/users/search',
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
              console.log(res.data)
              for(let i = 0; i < this.UserList.length; i++){
                if(this.UserList[i].role === 0){
                    this.UserList[i].role = "普通用户"
                }else{
                    this.UserList[i].role = "管理员"
                }
              }
              console.log(this.UserList)
          },
          //增加用户
          addUserList(){
            console.log(this.addUserForm)
            this.$refs.addUserRef.validate(async valid => {
                console.log(valid)
                if(!valid) return 

                this.addUser=false
                this.loading = true
                let data = this.$qs.stringify(this.addUserForm)
                console.log(this.addUserForm)
                const {data: res} = await this.$axios.post('/user',data,
                {
                    headers : {
                        'token': sessionStorage.getItem('token')
                    }
                })
                if(res.status ===200){
                    this.getUserList()
                }else{
                    this.$message.error(res.msg);
                }
                this.loading = false
            })
          },
          //触发编辑用户按钮
          async EditUser(row){
              this.EditUserID = row.id;
              this.loading = true
              console.log(row.id)
              const {data: res} = await this.$axios.get('/user/' + this.EditUserID,
              {
                  headers : {
                      'token': sessionStorage.getItem('token')
                  }
              })
              if(res.status !== 200) return  this.$message.error(res.msg)
              console.log(res.data)
              this.okEditUser = true;
              this.loading = false
              this.addUserForm = res.data
              //转成字符串
              if(this.addUserForm.role === 0) this.addUserForm.role = '0'
              else this.addUserForm.role = '1'
          },
          //确认编辑用户
          EditUserConfirm(){
            this.$refs.addUserRef.validate(async valid => {
                console.log(valid)
                if(!valid) return 
                this.okEditUser=false
                this.loading = true
                // console.log(row.id)
                let data = this.$qs.stringify(this.addUserForm)
                console.log(this.addUserForm)
                const {data: res} = await this.$axios.put('/user/'+this.EditUserID,data,
                {
                    headers : {
                        'token': sessionStorage.getItem('token')
                    }
                })
                if(res.status ===200){
                    this.getUserList()
                }else{
                    this.$message.error(res.msg);
                }
                this.loading = false
            })
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
            let data = sessionStorage.getItem('token')
            const {data: res} = await this.$axios.put('/user/'+this.EditUserID+'/softdelete',data,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.getUserList();
            this.loading = false
          },
          //进入用户空间
          EnterSpace(val){
              this.UserID=val.id
              window.sessionStorage.setItem('UserID',val.id)
              this.$router.push('/spacelist')
          },
          //搜索用户
          async searchUser(){
            if(this.searchValue !== '' && this.selectValue === ''){
                alert("请先选择搜索项！");
                return ;
            }
            this.loading = true
            console.log(this.selectValue)
            if(this.selectValue === '2'){
                this.queryPage.email = this.searchValue
                this.queryPage.nickname = ''
            }else if(this.selectValue === '1'){
                this.queryPage.email = ''
                this.queryPage.nickname = this.searchValue
            }else{
                this.queryPage.email = ''
                this.queryPage.nickname = ''
            }
            this.queryPage.page = 1
            this.queryPage.size = 5
            const {data: res} = await this.$axios.get('/users/search',
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
          handleSelectionUserChange(row){
            this.selectUserRows = row
            // console.log(row[0].id)
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
        ChangeRole(){
            console.log(this.addUserForm.role)
            // if(this.value === '1'){
            //     this.okDisabled = true
            //     this.addMonitorForm.include_filters = ""
            // }else if(this.value === '2'){
            //     this.okDisabled = false
            // }else if(this.value === 'JSONPath'){
            //     // this.addMonitorForm.include_filters=this.Element.jsonPath;
            // }
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