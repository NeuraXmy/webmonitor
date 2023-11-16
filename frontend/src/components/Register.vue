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
        console.log(valid)
        if(!valid) return 
        const {data: res} = await this.$axios.post('/auth/register',this.$qs.stringify(this.userForm))
        if(res.status ===200){
          console.log(res)
          this.$message.success(res.msg)
          this.$router.push('/login')
        }else{
          console.log(res)
          this.$message.error(res.msg);
        }
        
      })
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
@import '@/assets/css/login.css';
 
.login-info {
    margin-top: 10px;
}

</style>
