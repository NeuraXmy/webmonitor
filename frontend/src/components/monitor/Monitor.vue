<template>
    <div v-if="okMonitor">
      <el-breadcrumb>
          <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>任务管理</el-breadcrumb-item>
          <el-breadcrumb-item>监控空间列表</el-breadcrumb-item>
      </el-breadcrumb>
      <el-card>
          <el-row>
              <!-- <el-col :span="12">
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
              </el-col> -->
              <el-col :span="4">
                  <div>
                      <el-button type="primary" @click="addSpace=true"><el-icon><Plus /></el-icon>新增空间</el-button>
                      
                  </div>
              </el-col>
              <el-col :span="2">
                  <div>
                      <a href="javascript:(function() {var iframe = document.createElement('iframe');iframe.src = 'http://127.0.0.1:5173/select_monitor';iframe.style.position = 'fixed';iframe.style.top = '70%';iframe.style.right = '0';iframe.style.width = '100%';iframe.style.height = '30%';iframe.style.zIndex = 2147483647;iframe.id = 'iframe';var container = document.body;container.appendChild(iframe);var getcssSelector = function(path) {  console.log(path.length);  return path[path.length-1];};var cssPath = function(el) {    var path = [];    while (      (el.nodeName.toLowerCase() != 'body') &&        (el = el.parentNode) &&        path.unshift(el.nodeName.toLowerCase() +          (el.id ? %27#' + el.id : '') +            (el.className ? '.' + el.className.replace(/\s+/g, '.') : ''))    );    return path;};window.addEventListener('click', function(evt) {    console.log(evt);    console.log(evt.target.baseURI);    console.log(evt.target.innerText);    var x = evt.clientX;    var y = evt.clientY;    var el = document.elementFromPoint(x, y);    var selector = cssPath(el);    var element = evt.target;    var xpath = getXPath(element);    selector = getcssSelector(selector);        console.log(xpath);    console.log(selector);    var targetWindow = document.getElementById('iframe').contentWindow;    targetWindow.postMessage({xpath:xpath, selector:selector,  selectText:evt.target.innerText}, 'http://127.0.0.1:5173/select_monitor');});function mouse_over(event) {  var element = event.target;  element.style.border = '1px solid red';}function mouse_out(event) {  var element = event.target;  element.style.border = '';}function getXPath(element) {  if (element.id !== '') {    return '//*[@id=' + '%22' + element.id + '%22' + ']';  }  if (element === document.body) {    return '/html/body';  }  var index = 1;  const childNodes = element.parentNode ? element.parentNode.childNodes : [];  var siblings = childNodes;  for (var i = 0; i < siblings.length; i++) {    var sibling = siblings[i];    if (sibling === element) {      return (        getXPath(element.parentNode) +        '/' +        element.tagName.toLowerCase() +        '[' +        index +        ']'      );    }    if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {      index++;    }  }}document.addEventListener('mouseover', mouse_over);document.addEventListener('mouseout', mouse_out);var links = document.getElementsByTagName('a');for (var i = 0; i < links.length; i++) {    links[i].addEventListener('click', function(event) {    event.preventDefault();    event.stopPropagation();  });}})();" title="将我拖动到书签栏">小书签</a>
                      
                  </div>
              </el-col>
          </el-row>
          <el-row>
              <el-table :data="MonitorSpaceList" style="width: 100%">
                  <el-table-column prop="id" label="ID" width="100" />
                  <el-table-column prop="name" label="昵称" width="200" />
                  <el-table-column prop="create_time" label="创建时间" width="400" />
                  <el-table-column prop="update_time" label="更新时间" width="400" />
                  <el-table-column prop="edit" label="Edit" width="120">
                      <template #default="scope">
                          <!-- <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
                          >Edit</el-button
                          >
                          <el-button
                          size="small"
                          type="danger"
                          @click="handleDelete(scope.$index, scope.row)"
                          >Delete</el-button
                          > -->
                          <el-button size="small" @click="JumpMonitorManage(scope.row)"
                          >查看空间</el-button
                          >
                      </template>
                  </el-table-column>
              </el-table>
          </el-row>
      </el-card>
      <el-dialog
      v-model="addSpace"
      title="新增空间"
      width="40%"
    >
      <el-form ref="addSpaceRef" :rules="addSpaceRules" :model="addSpaceForm" label-width="80px" class="form_style">
          <el-form-item label="昵称">
              <el-col :span="20">
                  <el-input v-model="addSpaceForm.name" placeholder="请输入昵称"></el-input>
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
    </div>
    <div v-if="!okMonitor">
        <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>任务管理</el-breadcrumb-item>
            <el-breadcrumb-item @click="this.okMonitor=true">监控空间列表</el-breadcrumb-item>
            <el-breadcrumb-item>空间监控管理</el-breadcrumb-item>
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
                      <a :href='generateUrl' title="将我拖动到书签栏">拖到书签栏</a>
                      
                  </div>
              </el-col> -->
          </el-row>
          <el-row>
              <el-table :data="MonitorList" style="width: 100%">
                  <el-table-column prop="id" label="ID" width="50" />
                  <el-table-column prop="name" label="昵称" width="80" />
                  <el-table-column prop="url" label="网址" width="270" />
                  <el-table-column prop="create_time" label="创建时间" width="200" />
                  <el-table-column prop="update_time" label="更新时间" width="200" />
                  <el-table-column prop="last_check_time" label="检查时间" width="200" />
                  <el-table-column prop="edit" label="Edit" width="240">
                      <template #default="scope">
                          <el-button size="small" @click="WatchEdit(scope.row)"
                          >编辑</el-button
                          >
                          <el-button
                          size="small"
                          type="danger"
                          @click="DeleteWatch(scope.row)"
                          >删除</el-button
                          >
                          <el-button
                          size="small"
                          type="info"
                          @click="RefreshWatch(scope.row)"
                          >刷新</el-button
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
          >
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
                          <el-select v-model="this.addMonitorForm.include_filters" placeholder="Select" size="large">
                              <el-option
                              v-for="item in options"
                              :key="item.value"
                              :label="item.label"
                              :value="item.value"
                              />
                          </el-select>
                          <el-input type="textarea" v-model="addMonitorForm.include_filters" placeholder="请输入监控元素说明"></el-input>
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
          >
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
                          <el-select v-model="value" placeholder="Select" size="large">
                              <el-option
                              v-for="item in options"
                              :key="item.value"
                              :label="item.label"
                              :value="item.value"
                              />
                          </el-select>
                          <el-input type="textarea" v-model="addMonitorForm.include_filters" placeholder="请输入监控元素说明"></el-input>
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
              <template #footer>
              <span class="dialog-footer">
                  <el-button @click="EditMonitor = false">Cancel</el-button>
                  <el-button type="primary" @click="WatchEditConfirm">
                  Confirm
                  </el-button>
              </span>
              </template>
          </el-dialog>
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
      </div>
  </template>
  <script>
  import { Search,Plus,Delete } from '@element-plus/icons-vue'
  import { ref, computed } from 'vue';
//   import filePath from '../../embed/inject.js';
  export default{
      
      components: { Search,Plus,Delete },
      data(){
          return {
              okMonitor:true,
              MonitorSpaceList:[
                //   {
                //       id:'',name:'',create_time:'',update_time:''
                //   }
              ],
              MonitorList:[
                //   {
                //       id:'',name:'',url:'',create_time:'',update_time:'',last_check_time:''
                //   }
              ],
              value:'',
              options:[
                  {
                      value: 'XPath',
                      label: 'XPath',
                  },
                  {
                      value: 'CssSelector',
                      label: 'CssSelector',
                  }
                //   ,
                //   {
                //       value: 'JSONPath',
                //       label: 'JSONPath',
                //   }
              ],
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
              generateUrl:'',
              okDeleteWatch:false,
              DeleteWatchID:''
          }
      },
      created(){
          this.getMonitorSpaceList()
          //书签的url
        //   const filePath = '../embed/inject.js';
        //   console.log(filePath)
        //   try {
        //       const response = fetch(filePath);
        //       const data = response.text();
        //       this.generateUrl = data;
        //   } catch (error) {
        //       console.error(error);
        //   }
        //   console.log(this.generateUrl)
      },
      methods:{
          async getMonitorSpaceList(){
            console.log("---")
              const {data: res} = await this.$axios.get('/spaces',
              {
                  headers : {
                      'token': sessionStorage.getItem('token')
                  }
              })
              if(res.status !== 200) return  this.$message.error(res.msg)
              this.$message.success(res.message)
              
              console.log(res.data)
              this.MonitorSpaceList = res.data

              console.log(this.MonitorSpaceList)
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
          //刷新监控列表
          async RefreshMonitorManage(val){
              this.space_id = val
              // this.okMonitor=false
              const {data: res} = await this.$axios.get('/space/'+this.space_id+'/watches',
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
              let data = this.$qs.stringify(this.addMonitorForm)
              const {data: res} = await this.$axios.post('/space/'+this.space_id+'/watch',data,
              {
                  headers : {
                      'token': sessionStorage.getItem('token')
                  }
              })
              if(res.status !== 200) return  this.$message.error(res.msg)
              
              this.RefreshMonitorManage(this.space_id)
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
          //用户确定删除监控
          async ConfirmDeleteWatch(){
              const {data: res} = await this.$axios.delete('/watch/'+this.DeleteWatchID,
              {
                  params:{id: this.DeleteWatchID},
                  headers : {
                      'token': sessionStorage.getItem('token')
                  }
              })
              if(res.status !== 200) return  this.$message.error(res.msg)
              this.RefreshMonitorManage(this.space_id)
              this.okDeleteWatch = false;
          },
          DeleteWatch(row){
            this.okDeleteWatch = true;
            this.DeleteWatchID = row.id;
          },
          //触发用户修改监控,保存watch_id并且获取监控信息
          async WatchEdit(row){
              this.EditMonitor=true;
              this.watch_id=row.id;
              const {data: res} = await this.$axios.get('/watch/'+this.watch_id,
              {
                  headers : {
                      'token': sessionStorage.getItem('token')
                  }
              })
              if(res.status !== 200) return  this.$message.error(res.msg)
              
              this.addMonitorForm = res.data
          },
          //用户修改监控
          async WatchEditConfirm(){
              this.EditMonitor=false
              let data = this.$qs.stringify(this.addMonitorForm)
              const {data: res} = await this.$axios.put('/watch/'+this.watch_id,data,
              {
                  headers : {
                      'token': sessionStorage.getItem('token')
                  }
              })
              if(res.status !== 200) return  this.$message.error(res.msg)
              
              this.RefreshMonitorManage(this.space_id)
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
              
              this.RefreshMonitorManage(this.space_id)
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