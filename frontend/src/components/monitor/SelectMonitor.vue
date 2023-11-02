<template>
    <div>
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
                    <!-- <el-input v-model="addMonitorForm.element" placeholder="请输入网址"></el-input> -->
                    <el-select v-model="value" placeholder="Select" size="large">
                        <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                        />
                    </el-select>
                </el-col>
            </el-form-item>
            <el-form-item label="刷新时间">
                <el-col :span="4">
                    <!-- <el-input v-model="addMonitorForm.update_time" disabled></el-input> -->
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
        <el-button @click="test">123</el-button>
    </div>
</template>
  
<script>
export default{
    data(){
        return {
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
                notification_email:''
            }
        }
    },
    mounted(){
        window.addEventListener("message", (e) => {
            console.log(e);
            // this.addMonitorForm.=e.data;
        });
    },
    methods:{
        test(val){
            this.addMonitorForm.name="val";
        }
    }
}
</script>
  