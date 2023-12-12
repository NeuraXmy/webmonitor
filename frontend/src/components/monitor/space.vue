<template>
    <div>
      <el-breadcrumb>
          <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>任务管理</el-breadcrumb-item>
          <el-breadcrumb-item>监控空间列表</el-breadcrumb-item>
      </el-breadcrumb>
      <el-card>
          <el-row>
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
              loading: false,
              iframe_url: '',
              TotalPages: 10,
              queryPage: {
                page:1,
                size:5
              }
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
                //   params: this.queryPage,
                  headers : {
                      'token': sessionStorage.getItem('token')
                  }
              })
              if(res.status !== 200) return  this.$message.error(res.msg)
              this.$message.success(res.msg)
              this.TotalPages = res.data.total
              console.log(res.data)
              this.MonitorSpaceList = res.data.items
              this.loading = false
              console.log(this.MonitorSpaceList)
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