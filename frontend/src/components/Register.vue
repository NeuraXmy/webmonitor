<template>
  <div class="login-body">
    <div class="login-container">
      <div class="head">
        <img class="logo" src="../../public/changenotify.png" />
        <div class="name">
          <div class="title">{{ $t('name') }}</div>
        </div>
      </div>
        <el-form ref="userRegisterRef" :rules="userRules" :model="userForm" label-width="0px" class="form_style">
          <el-menu
              mode="horizontal"
              :ellipsis="false"
              @select="handleSelect"
              active-text-color="#000000"
              text-color="#545c64"
            >
            <div class="flex-grow" />
              <el-sub-menu index="2" style="margin-right='0px'">
                  <template #title><font-awesome-icon icon="fas fa-language" /></template>
                  <el-menu-item index="2-1">English</el-menu-item>
                  <el-menu-item index="2-2">简体中文</el-menu-item>
              </el-sub-menu>
            </el-menu>
            <el-form-item prop="email">
                <el-input v-model="userForm.email" :placeholder="$t('table.email')"></el-input>
            </el-form-item>
            <el-form-item prop="password">
                <el-input show-password v-model="userForm.password" :placeholder="$t('table.password')"></el-input>
            </el-form-item>
            <el-form-item prop="nickname">
                <el-input v-model="userForm.nickname" :placeholder="$t('label.nickname')"></el-input>
            </el-form-item>
            <el-form-item>
                <el-input v-model="userForm.invitation_code" :placeholder="$t('label.invite')"></el-input>
            </el-form-item>
            <vue-hcaptcha :sitekey="sitekey" @verify="verify" @challengeExpired="challengeExpired"></vue-hcaptcha>
            <!-- <cfturnstile
              :sitekey="sitekey"
              @verify="verify"
            /> -->
            <el-form-item>
                <el-button type="primary" @click="register">{{ $t('register') }}</el-button>
                <el-button @click="restForm">{{ $t('restForm') }}</el-button>
            </el-form-item>
            <a class="form__link" @click="login">{{ $t('login') }}</a>
        </el-form>
    </div>
  </div>
</template>

<script>
import vueRecaptcha from 'vue3-recaptcha2';
import cfturnstile from 'cfturnstile-vue3'
import VueHcaptcha from '@hcaptcha/vue3-hcaptcha';

export default {
  components: { vueRecaptcha,cfturnstile,VueHcaptcha },
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
          password:'',
          nickname:'',
          invitation_code: ''
      },
      userRules:{
          email:[
              {required:true, validator: validEmail, trigger:'blur'}
          ],
          password:[
              {required:true, message: '请输入密码', trigger:'blur'}
          ],
          nickname:[
              {required:true, min:2,  message: '昵称长度不能小于2位', trigger:'blur'}
          ]
      },
      okVerified: false,
      sitekey:'50c11cc1-e8f1-4076-aac4-80099d040f90'
    };
  },
  created(){
      let params = new URLSearchParams(window.location.search);
      this.userForm.invitation_code = params.get('invitation_code');
  },
  methods:{
    restForm(){
      this.$refs.userRegisterRef.resetFields()
    },
    async register(){
      if(this.okVerified === true){
        this.$refs.userRegisterRef.validate(async valid => {
          console.log(valid)
          if(!valid) return 
          const {data: res} = await this.$axios.post('/auth/register',this.$qs.stringify(this.userForm))
          if(res.status ===200){
            console.log(res)
            window.sessionStorage.setItem('email',this.userForm.email)
            console.log(sessionStorage.getItem('email'))
            this.$message.success(res.msg)
            this.$router.push('/activate')
          }else{
            console.log(res)
            this.$message.error(res.msg);
          }
        })
      }else{
        alert("人机验证未成功！")
      }
      
    },
    verify(token) {
        // console.log(token)
        // console.log("-----")
        this.okVerified = true;
    },
    challengeExpired(){
      // this.okVerified = false;
      // console.log("-----");
    },
    login(){
      this.$router.push('/login')
    },
    handleSelect(val){
        // console.log(val)
        if(val === "2-1") this.$i18n.locale = 'en'
        else this.$i18n.locale = 'zh'
    },
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
    height: 600px;
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
.flex-grow {
  flex-grow: 1;
}
</style>