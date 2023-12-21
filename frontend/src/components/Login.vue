<template>
  <div class="login-body">
    <div class="login-container">
      <div class="head">
        <img class="logo" src="../../public/changenotify.png" />
        <div class="name">
          <div class="title">多模态信息舆情监控</div>
        </div>
      </div>
      <el-form ref="userRef" :rules="userRules" :model="userForm" label-width="0px" class="form_style">
            <el-form-item prop="email" >
                <el-input prefix-icon="User" v-model="userForm.email" placeholder="邮箱"></el-input>
            </el-form-item>
            <el-form-item  prop="password">
                <el-input show-password prefix-icon="Lock" v-model="userForm.password" placeholder="密码"></el-input>
            </el-form-item>
            <el-form-item>
              <!-- <div class="cf-turnstile" data-sitekey="0x4AAAAAAAOhZLLzYs90Djqz" data-callback="javascriptCallback"></div> -->
                <el-button type="primary" @click="login">登录</el-button>
                <el-button @click="restForm">重置</el-button>
            </el-form-item>
            <a class="form__link" @click="register">注册</a>
            <!-- <router-link to="/register">
              <div style="margin-top: 5px">注册</div>
          </router-link> -->
        </el-form>
    </div>
  </div>
</template>

<script>
import { User,Lock } from '@element-plus/icons-vue'
import Cookies from 'universal-cookie';

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
          // console.log(res.data)
          window.sessionStorage.setItem('token',res.data.token)
          window.sessionStorage.setItem('role',res.data.role)
          window.sessionStorage.setItem('email',this.userForm.email)
          // window.localStorage.setItem('token',res.data.token)
          this.$message.success(res.msg)
          // console.log(res)
          if(res.data.role === 0) this.$router.push('/home')
          else this.$router.push('/admin')
          this.setCookie('verify_authenticity_token' , res.data.token);
          // console.log(this.getCookie('verify_authenticity_token'))
        }else{
          this.$message.error(res.msg);
        }
        
      })
    },
    register(){
      // console.log("-----")
      this.$router.push('/register')
      // this.$router.push({ path: '/register' }).then(() => {
      //   console.log("----")
      //   location.reload()
      // })
    },
    forgetPassword(){

    },
    //添加cookie
    setCookie(name , value){
      const cookies = new Cookies();
        const options = {
          secure: true,
          sameSite: 'none',
        };
      cookies.set(name, value, options);
    },
    //获得cookie
    getCookie(name){
      console.log(document.cookie)
      var arr = document.cookie.split(";")
      for(var i = 0 ; i < arr.length ; i++){
        var arr2 = arr[i].split("=")
        if(arr2[0].trim() === name){
          return arr2[1]
        }
      }
    },
    //删除cookie
    removeCookie(name){
      setCookie(name,"")
    },
    test(){
        const cookies = new Cookies();
        const options = {
          secure: true,
          sameSite: 'none',
        };
        cookies.set('access_token', 'c212e015-d66e-460f-97ab-55fab8e19bed', options);
        console.log(this.getCookie('access_token'))
    }

  }
}
</script>
<style scoped>
.login-body {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    background-color: #fff;
}
.login-container {
    width: 420px;
    height: 500px;
    background-color: #fff;
    border-radius: 4px;
    box-shadow: 0px 21px 41px 0px rgba(0, 0, 0, 0.2);
}
.head {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px 0 20px 0;
}
.head img {
    width: 100px;
    height: 100px;
    margin-right: 20px;
}
.head .title {
    font-size: 28px;
    color: #409EFF;
    font-weight: bold;
}
.head .tips {
    font-size: 12px;
    color: #999;
}
.login-form {
    width: 70%;
    margin: 0 auto;
}
.login-form >>> .el-form--label-top .el-form-item__label {
    padding: 0;
}
.login-form >>> .el-form-item {
    margin-bottom: 0;
}
.form_style{
  bottom: 0;
  width: 100%;
  padding: 0 10%;
  box-sizing: border-box;

}
.form__link {
  /* color: #181818; */
  font-size: 14px;
  margin-top: 25px;
  color: #409EFF;
  border-bottom: 1px solid #a0a5a8;
  line-height: 2;
  cursor: pointer;
  text-decoration: none;
}
</style>