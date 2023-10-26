<template>
  <div class="login_container">
      <div class="login_box">
          <div class="title">
            欢迎
          </div>
          <el-form ref="userRef" :rules="userRules" :model="userForm" label-width="0px" class="form_style">
              <el-form-item prop="email">
                  <el-input v-model="userForm.email" placeholder="用户名"></el-input>
              </el-form-item>
              <el-form-item prop="password">
                  <el-input show-password v-model="userForm.password" placeholder="密码"></el-input>
              </el-form-item>
              <a class="form__link" @click="register">注册新账户</a>
              <el-form-item>
                  <el-button type="primary" @click="login">登录</el-button>
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
          email:'sxt',
          password:'123'
      },
      userRules:{
          email:[
              {required:true, message: '请输入邮箱', trigger:'blur'},
              // {min:2, max:6,  message: '长度在2到6个字符', trigger:'blur'}
          ],
          password:[
              {required:true, message: '请输入密码', trigger:'blur'}
          ]
      }
    };
  },
  methods:{
    restForm(){
      // console.log(this)
      this.$refs.userRef.resetFields()
    },
    login(){
      this.$refs.userRef.validate(async valid => {
        // console.log(valid)
        if(!valid) return 
        const {data: res} = await this.$axios.post('/auth/login',this.$qs.stringify(this.userForm))
        if(res.status ===200){
          window.sessionStorage.setItem('token',res.data.token)
          this.$message.success(res.message)
          this.$router.push('/home')
        }else{
          this.$message.error(res.message);
        }
        
      })
    },
    register(){
      // console.log("----")
      this.$router.push('/register')
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
.form__link {
  /* color: #181818; */
  font-size: 15px;
  margin-top: 25px;
  border-bottom: 1px solid #a0a5a8;
  line-height: 2;
  cursor: pointer;
  text-decoration: none;
}




</style>
