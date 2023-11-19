<template>
  <div class="login_container">
      <div class="login_box">
          <div class="title">
            多模态信息舆情监控
          </div>
          <el-form ref="userRef" :rules="userRules" :model="userForm" label-width="0px" class="form_style">
              <el-form-item prop="email" >
                  <el-input prefix-icon="User" v-model="userForm.email" placeholder="邮箱"></el-input>
              </el-form-item>
              <el-form-item  prop="password">
                  <el-input show-password prefix-icon="Lock" v-model="userForm.password" placeholder="密码"></el-input>
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
import { User,Lock } from '@element-plus/icons-vue'

export default{
  components: { User,Lock },
  data() {
    const validEmail = (rule, value, callback) => {
      const EmailReg = /^^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$/
      if(EmailReg.test(value)){
        return callback()
      }
      return callback(new Error('请输入正确的邮箱'))
    }
    return {
      userForm:{
          email:'',
          password:''
      },
      userRules:{
          email:[
              // {required:true, message: '请输入邮箱', trigger:'blur'},
              {required:true, validator: validEmail, trigger:'blur'}
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
        console.log(valid)
        if(!valid) return 
        const {data: res} = await this.$axios.post('/auth/login',this.$qs.stringify(this.userForm))
        if(res.status ===200){
          window.sessionStorage.setItem('token',res.data.token)
          this.$message.success(res.msg)
          this.$router.push('/home')
        }else{
          this.$message.error(res.msg);
        }
        
      })
    },
    register(){
      this.$router.push('/register')
    },
    forgetPassword(){

    }
  }
}
</script>
<style lang='less' scoped>
.login_container {
  background-color:#f8fbfd;
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
  width: 350px;
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


@import '@/assets/css/login.css';
 
.login-info {
    margin-top: 10px;
}
</style>
