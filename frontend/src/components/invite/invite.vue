<template>
    <el-card>
        <el-form ref="MonitorRef" :rules="verifyRules" :model="verifyForm" label-width="130px" class="form_style">
            <el-form-item :label="$t('invite.fill_out_invitation_code')" prop="code">
                <el-col :span="10">
                    <el-input v-model="verifyForm.invitation_code" :placeholder="$t('invite.please_fill_out_code')" :disabled="invited"></el-input>
                </el-col>
                <el-col :span="10" style="margin-left: 20px;">
                    <el-button type="primary" round @click="verifyInvition" :loading="verify_Code_loading">{{$t('invite.verify')}}</el-button>
                </el-col>
            </el-form-item>
        </el-form>
        <el-text class="mx-1" size="small">{{$t('invite.detail')}}</el-text>
    </el-card>
    <el-card style="margin-top: 20px;">
        <div style="display: flex; justify-content: space-between;">
            <div>
                <span>{{$t('invite.invitation_code')}}     
                    <el-text class="mx-1" size="small">{{ InvitionCode }}</el-text>
                    <el-button type="primary" link @click="copyInvitationCode">{{$t('invite.copy')}}</el-button>
                </span>
            </div>
            <div style="display: flex; justify-content: flex-end;">
                <el-button type="primary" round @click="CreateInvition" :loading="Create_Code_loading">{{$t('invite.create_invitation_code')}}</el-button>
            </div>
        </div>
        <div>
            <span>{{$t('invite.invitation_link')}}  
                <el-text class="mx-1" size="small">{{ InvitionLink }}</el-text>
                <el-button type="primary" link @click="copyInvitationLink">{{$t('invite.copy')}}</el-button>
            </span>
        </div>
    </el-card>
    <el-card style="margin-top: 20px;">
        <span>{{$t('invite.my_invition')}}</span>
        <el-row>
            <el-table v-loading="loading" :data="InviteList" style="width: 100%">
                <el-table-column prop="email" :label="$t('invite.email')" width="1000" />
                <el-table-column prop="create_time" :label="$t('invite.create_time')" width="200" />
            </el-table>
            <el-pagination
                v-model:current-page="queryPage.page"
                v-model:page-size="queryPage.size"
                :page-sizes="[5, 10, 20, 50]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="TotalPages"
                @size-change="handleSizeInviteChange"
                @current-change="handleCurrentInviteChange"
            />
        </el-row>
    </el-card>

</template>

<script>
export default{
    data(){
        return {
            InviteList:[
                // {id: "www.baidu.com", name: "2024/1/15"}
            ],
            loading:false,
            TotalPages: 10,
            queryPage: {
                page:1,
                size:10
            },
            InvitionCode:null,
            Create_Code_loading:false,
            verifyForm: {
                invitation_code: null
            },
            verifyRules:{
                code:[
                    {required:true, message: '请输入对方邀请码', trigger:'blur'},
                ]
            },
            verify_Code_loading: false,
            invited: false,
            InvitionLink: null
        }
    },
    created(){
        this.getInviteList()
        this.getInviteCode()
    },
    methods:{
        //获取邀请详情
        async getInviteList(){
            this.loading = true
            const {data: res} = await this.$axios.get('/user/invitations',
            {
                params: this.queryPage,
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            this.loading = false
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            // console.log(res)
            this.InviteList = res.data.items
        },
        //获取邀请码
        async getInviteCode(){
            this.loading = true
            const {data: res} = await this.$axios.get('/user',
            {
                // params: this.queryPage,
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            this.loading = false
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            // console.log(res)
            this.InvitionCode = res.data.invitation_code
            this.invited = res.data.invited
            this.InvitionLink = 'https://app.changenotify.net/register?invitation_code=' + this.InvitionCode
        },
        //生成邀请链接
        async CreateInvition(){
            this.Create_Code_loading = true
            let data = sessionStorage.getItem('token')
            const {data: res} = await this.$axios.put('/user/invitation_code',data,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            this.Create_Code_loading = false
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            // console.log(res)
            this.InvitionCode = res.data.invitation_code
            this.InvitionLink = 'https://app.changenotify.net/register?invitation_code=' + this.InvitionCode
        },
        //验证邀请码
        async verifyInvition(){
            this.verify_Code_loading = true
            let data = sessionStorage.getItem('token')
            console.log(this.verifyForm)
            const {data: res} = await this.$axios.post('/user/invitation_code',this.$qs.stringify(this.verifyForm),
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            this.verify_Code_loading = false
            if(res.status !== 200) return this.$message.error(res.msg)
            this.$message.success(res.msg)
            this.getInviteCode();
        },
        copyInvitationCode() {
            /* 创建一个临时输入框元素 */
            const tempInput = document.createElement('input');
            tempInput.value = this.InvitionCode;
            document.body.appendChild(tempInput);

            /* 选择文本内容 */
            tempInput.select();
            tempInput.setSelectionRange(0, 99999); /* 兼容移动设备 */

            /* 复制文本内容到剪贴板 */
            document.execCommand('copy');

            /* 移除临时输入框 */
            document.body.removeChild(tempInput);

            /* 提示复制成功 */
            this.$message.success('邀请码已复制！');
        },
        copyInvitationLink(){
            /* 创建一个临时输入框元素 */
            const tempInput = document.createElement('input');
            tempInput.value = this.InvitionLink;
            document.body.appendChild(tempInput);

            /* 选择文本内容 */
            tempInput.select();
            tempInput.setSelectionRange(0, 99999); /* 兼容移动设备 */

            /* 复制文本内容到剪贴板 */
            document.execCommand('copy');

            /* 移除临时输入框 */
            document.body.removeChild(tempInput);

            /* 提示复制成功 */
            this.$message.success('邀请链接已复制！');
        },
        handleSizeInviteChange(val){
            this.queryPage.size = val
            this.getInviteList()
        },
        handleCurrentInviteChange(val){
            this.queryPage.page = val
            this.getInviteList()
        }
    }
}
</script>