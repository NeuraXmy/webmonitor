<template>
  <div class="login_container">
      <div class="login_box">
          <div class="title">
            欢迎
          </div>
          <el-form ref="userRegisterRef" :rules="userRules" :model="userForm" label-width="0px" class="form_style">
              <el-form-item prop="name">
                  <el-input v-model="userForm.name" placeholder="用户名"></el-input>
              </el-form-item>
              <el-form-item prop="pwd">
                  <el-input show-password v-model="userForm.pwd" placeholder="密码"></el-input>
              </el-form-item>

              <el-form-item>
                  <el-button type="primary" @click="register">注册</el-button>
                  <el-button @click="restForm">重置</el-button>
              </el-form-item>
          </el-form>
      </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userForm:{
          name:'sxt',
          pwd:'123'
      },
      userRules:{
          name:[
              {required:true, message: '请输入用户名', trigger:'blur'},
              {min:2, max:6,  message: '长度在2到6个字符', trigger:'blur'}
          ],
          pwd:[
              {required:true, message: '请输入密码', trigger:'blur'}
          ]
      }
    };
  },
  methods:{
    restForm(){
      // console.log(this)
      this.$refs.userRegisterRef.resetFields()
    },
    register(){
      this.$refs.userRegisterRef.validate(async valid => {
        // console.log(valid)
        if(!valid) return 
        const {data: res} = await this.$axios.post('/auth/register',this.$qs.stringify(this.userForm))
        if(res.status ===200){
          window.sessionStorage.setItem('token',res.data.token)
          // this.$msg.success(res.msg)
          this.$route.push('/home')
        }else{
          // this.$msg.error(res.msg);
        }
        
      })
    }
  }
}
</script>
<style lang='less' scoped>
.login_container {
  background-color:darkcyan;
  height: 100%
}
.login_box{
  width: 450px;
  height: 300px;
  border-radius: 5px;
  background-color: #ccc;
  position: absolute;
  left: 50%;
  top:50%;
  transform: translate(-50%,-50%);
}
  .title {
  // width: 200px;
  // height: 100px;
  font-size: 34px;
  font-weight: 700;
  line-height: 3;
  position: absolute;
  left: 50%;
  transform: translate(-50%,0%);
  color: var(--text-color);
}
.form_style{
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 0 10%;
  box-sizing: border-box;

}


</style>
