<template>
  <div class="login_container">
      <div class="login_box">
          <div class="title">
            多模态信息舆情监控
          </div>
          <el-form ref="userRegisterRef" :rules="userRules" :model="userForm" label-width="0px" class="form_style">
              <el-form-item prop="email">
                  <el-input v-model="userForm.email" placeholder="邮箱"></el-input>
              </el-form-item>
              <el-form-item prop="password">
                  <el-input show-password v-model="userForm.password" placeholder="密码"></el-input>
              </el-form-item>
              <el-form-item prop="nickname">
                  <el-input v-model="userForm.nickname" placeholder="昵称"></el-input>
              </el-form-item>
              <vue-recaptcha
                :sitekey="v2Sitekey"
                size="normal"
                theme="light"
                hl="zh"
                @verify="recaptchaVerified"
                @expire="recaptchaExpired"
                @fail="recaptchaFailed"
                ref="vueRecaptcha">
              </vue-recaptcha>
              <el-form-item>
                  <el-button type="primary" @click="register">注册</el-button>
                  <el-button @click="restForm">重置</el-button>
              </el-form-item>
          </el-form>
      </div>
  </div>
</template>

<script>
import vueRecaptcha from 'vue3-recaptcha2';
export default {
  components: { vueRecaptcha },
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
          nickname:''
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
      okVerified: false
    };
  },
  setup() {
    const v2Sitekey = '6LcqoRMpAAAAAIYDSZpLccz_w7axiDZ9EvUaFaqt';
    return {
      v2Sitekey
    }
  },
  methods:{
    restForm(){
      // console.log(this)
      this.$refs.userRegisterRef.resetFields()
    },
    register(){
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
    // 回传一组 token，并把 token 传给后端验证
    recaptchaVerified(res){
      console.log(res)
      this.okVerified = true
	  },
 
    recaptchaExpired(){
      // 过期后执行动作
      this.okVerified = false
    },
 
    recaptchaFailed(){
      // 失败执行动作
      this.okVerified = false
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
  height: 400px;
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
.login-info {
    margin-top: 10px;
}

</style>
