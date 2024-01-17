<template>
    <div>
        <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>套餐管理</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-row>
                <el-button type="primary" @click="AddPackage"><el-icon><Plus /></el-icon>新增套餐</el-button>
            </el-row>
            <el-row>
                <el-table v-loading="loading" :data="PackageList" style="width: 100%">
                    <el-table-column prop="id" label="ID" width="150" />
                    <el-table-column prop="name" label="套餐名称" width="150" />
                    <el-table-column prop="period_type" label="周期" width="100" >
                        <template #default="scope">
                            <span v-if="scope.row.period_type === 0">一次性</span>
                            <span v-if="scope.row.period_type === 1">日付</span>
                            <span v-if="scope.row.period_type === 2">月付</span>
                            <span v-if="scope.row.period_type === 3">年付</span>
                        </template>
                    </el-table-column>
                    <!-- <el-table-column prop="period_count" label="周期数" width="150" /> -->
                    <el-table-column prop="period_check_count" label="监控次数" width="200" />
                    <el-table-column prop="price" label="价格(分)" width="100" />
                    <el-table-column prop="hide" label="隐藏" width="80" >
                        <template #default="scope">
                            <el-switch
                                v-model="scope.row.hide"
                                :active-value = 1
                                :inactive-value = 0
                                active-color="#02538C"
                                inactive-color="#B9B9B9"
                                inline-prompt
                                active-text="ON"
                                inactive-text="OFF"
                                @click="RevisePackage(scope.row)"/>
                        </template>
                    </el-table-column>
                    <el-table-column prop="initial" label="初始套餐" width="80" >
                        <template #default="scope">
                            <el-switch
                                v-model="scope.row.initial"
                                :active-value = 1
                                :inactive-value = 0
                                active-color="#02538C"
                                inactive-color="#B9B9B9"
                                inline-prompt
                                active-text="ON"
                                inactive-text="OFF"
                                @click="RevisePackage(scope.row)"/>
                        </template>
                    </el-table-column>
                    <el-table-column prop="inviter_package:" label="赠送邀请者" width="80" >
                        <template #default="scope">
                            <el-switch
                                v-model="scope.row.inviter_package"
                                :active-value = 1
                                :inactive-value = 0
                                active-color="#02538C"
                                inactive-color="#B9B9B9"
                                inline-prompt
                                active-text="ON"
                                inactive-text="OFF"
                                @click="RevisePackage(scope.row)"/>
                        </template>
                    </el-table-column>
                    <el-table-column prop="invitee_package:" label="赠送被邀请者" width="80" >
                        <template #default="scope">
                            <el-switch
                                v-model="scope.row.invitee_package"
                                :active-value = 1
                                :inactive-value = 0
                                active-color="#02538C"
                                inactive-color="#B9B9B9"
                                inline-prompt
                                active-text="ON"
                                inactive-text="OFF"
                                @click="RevisePackage(scope.row)"/>
                        </template>
                    </el-table-column>
                    <el-table-column prop="edit" label="操作" width="230">
                        <template #default="scope">
                            <el-button size="small" @click="PackageEdit(scope.row)"
                                >编辑</el-button
                            >
                            <el-button
                                size="small"
                                type="danger"
                                @click="DeletePackage(scope.row)"
                                >删除</el-button
                            >
                            <!-- <el-button class="operatBtn" size="small"
                                :disabled="scope.$index===0"
                                @click="moveUp(scope.$index,scope.row)">
                                <el-icon><Top /></el-icon>
                            </el-button>
                            <el-button class="operatBtn" size="small"
                                :disabled="scope.$index===(PackageList.length-1)"
                                @click="moveDown(scope.$index,scope.row)">
                                <el-icon><Bottom /></el-icon>
                            </el-button> -->
                        </template>
                    </el-table-column>
                </el-table>
                <el-pagination
                    v-model:current-page="queryPage.page"
                    v-model:page-size="queryPage.size"
                    :page-sizes="[5, 10, 20, 50]"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="TotalPages"
                    @size-change="handleSizePackageChange"
                    @current-change="handleCurrentPackageChange"
                />
            </el-row>
        </el-card>
    </div>
    <el-dialog
      v-model="okAddPackage"
      title="新增套餐"
      width="40%"
    >
        <el-form ref="PackageRef" :rules="PackageRules" :model="PackageForm" label-width="80px" class="form_style">
            <el-form-item label="套餐名称" prop="name">
                <el-col :span="20">
                    <el-input v-model="PackageForm.name" placeholder="请输入套餐名称"></el-input>
                </el-col>
            </el-form-item>
            <!-- <el-form-item label="周期数" prop="period_count">
                <el-col :span="20">
                    <el-input v-model="PackageForm.period_count" placeholder="请输入周期数"></el-input>
                </el-col>
            </el-form-item> -->
            <el-form-item label="周期">
                <el-col :span="20">
                    <el-select v-model="PackageForm.period_type" placeholder="Select" @change="ChangePackage_type">
                        <el-option
                            v-for="item in Package_types"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </el-col>
            </el-form-item>
            <el-form-item label="监控次数" prop="period_check_count">
                <el-col :span="20">
                    <el-input v-model="PackageForm.period_check_count" placeholder="请输入监控次数"></el-input>
                </el-col>
            </el-form-item>
            <!-- <el-form-item label="周期" prop="name">
                <el-col :span="20">
                    <el-input v-model="PackageForm.period_type" placeholder="请输入周期"></el-input>
                </el-col>
            </el-form-item> -->
            <el-form-item label="价格(分)" prop="price">
                <el-col :span="20">
                    <el-input v-model="PackageForm.price" placeholder="请输入价格"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="隐藏" prop="hide">
                <el-col :span="20">
                    <el-switch
                        v-model="PackageForm.hide"
                        :active-value = 1
                        :inactive-value = 0
                        active-color="#02538C"
                        inactive-color="#B9B9B9"
                        inline-prompt
                        active-text="ON"
                        inactive-text="OFF"
                    />
                </el-col>
            </el-form-item>
            <el-form-item label="初始套餐" prop="initial">
                <el-col :span="20">
                    <el-switch
                        v-model="PackageForm.initial"
                        :active-value = 1
                        :inactive-value = 0
                        active-color="#02538C"
                        inactive-color="#B9B9B9"
                        inline-prompt
                        active-text="ON"
                        inactive-text="OFF"
                    />
                </el-col>
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
            <el-button @click="okAddPackage = false">取消</el-button>
            <el-button type="primary" @click="AddPackageConfirm">
                确定
            </el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog
      v-model="okEditPackage"
      title="编辑套餐"
      width="40%"
    >
        <el-form ref="PackageRef" :rules="PackageRules" :model="PackageForm" label-width="80px" class="form_style">
            <el-form-item label="套餐名称" prop="name">
                <el-col :span="20">
                    <el-input v-model="PackageForm.name" placeholder="请输入套餐名称"></el-input>
                </el-col>
            </el-form-item>
            <!-- <el-form-item label="周期数" prop="period_count">
                <el-col :span="20">
                    <el-input v-model="PackageForm.period_count" placeholder="请输入周期数"></el-input>
                </el-col>
            </el-form-item> -->
            <el-form-item label="周期">
                <el-col :span="20">
                    <el-select v-model="PackageForm.period_type" placeholder="Select" @change="ChangePackage_type">
                        <el-option
                            v-for="item in Package_types"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </el-col>
            </el-form-item>
            <el-form-item label="监控次数" prop="period_check_count">
                <el-col :span="20">
                    <el-input v-model="PackageForm.period_check_count" placeholder="请输入监控次数"></el-input>
                </el-col>
            </el-form-item>
            <!-- <el-form-item label="周期" prop="name">
                <el-col :span="20">
                    <el-input v-model="PackageForm.period_type" placeholder="请输入周期"></el-input>
                </el-col>
            </el-form-item> -->
            <el-form-item label="价格(分)" prop="price">
                <el-col :span="20">
                    <el-input v-model="PackageForm.price" placeholder="请输入价格"></el-input>
                </el-col>
            </el-form-item>
            
        </el-form>
        <template #footer>
            <span class="dialog-footer">
            <el-button @click="okEditPackage = false">取消</el-button>
            <el-button type="primary" @click="EditPackageConfirm">
                确定
            </el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog
        v-model="okDeletePackage"
        width="30%"
        align-center
        >
        <span>是否删除该套餐？</span>
        <template #footer>
            <span class="dialog-footer">
            <el-button @click="okDeletePackage = false">取消</el-button>
            <el-button type="primary" @click="ConfirmDeletePackage">
                确定
            </el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script>
import { Search,Plus,Delete,Edit,Top,Bottom } from '@element-plus/icons-vue'
export default{
    
    components: { Search,Plus,Delete,Edit,Top,Bottom },
    data(){
        const validPrice = (rule, value, callback) => {
            if(value >= 500){
                return callback()
            }
            return callback(new Error('价格至少500分'))
        }
        return {
            PackageList:[
                {
                    id:1,
                    period_type:"一次性",
                    price:10,
                    period_check_count:"200"
                }
            ],
            loading:false,
            okDeletePackage:false,
            Package_id:'',
            okEditPackage:false,
            PackageRules:{
                name:[
                    {required:true, message: '请输入套餐名称', trigger:'blur'},
                ],
                period_type:[
                    {required:true, message: '请输入周期', trigger:'blur'}
                ],
                price:[
                    {required:true, message: '请输入价格', trigger:'blur'},
                    {required:true, validator: validPrice, trigger:'blur'}
                ],
                period_check_count:[
                    {required:true, message: '请输入监控次数', trigger:'blur'}
                ],
                period_count:[
                    {required:true, message: '请输入周期次数', trigger:'blur'}
                ]
            },
            PackageForm:{
                name:'test',
                period_type:0,
                period_count:1,
                price:0,
                period_check_count:1,
                hide:0,
                initial:0
            },
            Package_types:[
                {
                    value: 0,
                    label: '一次性',
                },
                {
                    value: 3,
                    label: '年付',
                },
                {
                    value: 2,
                    label: '月付',
                },
                {
                    value: 1,
                    label: '日付',
                }
            ],
            Package_type:'',
            okAddPackage:false,
            TotalPages: 10,
            queryPage: {
                page:1,
                size:10
            },
        }
    },
    created(){
        this.getPackagesList()
    },
    methods: {
        //获得所有套餐
        async getPackagesList(){
            this.loading = true
            const {data: res} = await this.$axios.get('/package/template',
            {
                params: this.queryPage,
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            console.log(res)
            this.loading = false
            this.TotalPages = res.data.total
            this.PackageList = res.data.items
            // console.log(this.PackageList)
        },
        //获得单个套餐信息
        // async getPackageList(){
        //     this.loading = true
        //     const {data: res} = await this.$axios.get('/package/template/' + this.Package_id,
        //     {
        //         // params: this.queryPage,
        //         headers : {
        //             'token': sessionStorage.getItem('token')
        //         }
        //     })
        //     if(res.status !== 200) return  this.$message.error(res.msg)
        //     this.$message.success(res.msg)
        //     this.loading = false
        //     console.log(res.data)
        //     this.PackageForm = res.data
        // },
        //删除套餐
        DeletePackage(row){
            this.Package_id = row.id;
            this.okDeletePackage = true;
        },
        //确定删除套餐
        async ConfirmDeletePackage(){
            this.okDeletePackage = false;
            this.loading = true
            const {data: res} = await this.$axios.delete('/package/template/'+this.Package_id,
            {
                // params:{id: this.okDeleteSubscribe},
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.getPackagesList()
            this.loading = false
        },
        //编辑套餐
        PackageEdit(row){
            this.okEditPackage = true;
            this.Package_id = row.id;
            for(let i = 0; i < this.PackageList.length; i++){
                if(this.PackageList[i].id === row.id){
                    this.PackageForm = this.PackageList[i];
                    break;
                }
            }
        },
        //确定编辑套餐
        EditPackageConfirm(){
            this.$refs.PackageRef.validate(async valid => {
                console.log(valid)
                if(!valid) return 
                this.okEditPackage = false
                this.loading = true
                let data = this.$qs.stringify(this.PackageForm)
                // let data = this.PackageForm
                console.log(data)
                const {data: res} = await this.$axios.put('/package/template/'+this.Package_id,data,
                {
                    headers : {
                        'token': sessionStorage.getItem('token')
                    }
                })
                if(res.status ===200){
                    this.getPackagesList()
                }else{
                    this.$message.error(res.msg);
                }
                this.loading = false
            })
        },
        ChangePackage_type(){

        },
        //添加套餐
        AddPackage(){
            this.okAddPackage = true;
            this.PackageForm.name = '';
            this.PackageForm.period_type = 0;
            this.PackageForm.period_count = 1;
            this.PackageForm.price = 500;
            this.PackageForm.period_check_count = 0;
            this.PackageForm.hide = 0
            this.PackageForm.initial = 0
        },
        //确定添加套餐
        AddPackageConfirm(){
            this.$refs.PackageRef.validate(async valid => {
                console.log(valid)
                if(!valid) return ;
                this.okAddPackage = false
                this.loading = true
                let data = this.$qs.stringify(this.PackageForm)
                const {data: res} = await this.$axios.post('/package/template',data,
                {
                    headers : {
                        'token': sessionStorage.getItem('token')
                    }
                })
                if(res.status ===200){
                    this.getPackagesList()
                }else{
                    this.$message.error(res.msg);
                }
                this.loading = false
            })
        },
        //获得套餐页号
        handleCurrentPackageChange(val){
            this.queryPage.page = val
            this.getPackagesList()
        },
        //获得套餐页数
        handleSizePackageChange(val){
            this.queryPage.size = val
            this.getPackagesList()
        },
        //修改包状态
        async RevisePackage(row){
            this.Package_id = row.id;
            for(let i = 0; i < this.PackageList.length; i++){
                if(this.PackageList[i].id === row.id){
                    this.PackageForm = this.PackageList[i];
                    break;
                }
            }
            this.loading = true
            // console.log(this.PackageForm.hide)
            let data = this.$qs.stringify(this.PackageForm)
            const {data: res} = await this.$axios.put('/package/template/'+row.id,data,
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status ===200){
                this.getPackagesList()
            }else{
                this.$message.error(res.message);
            }
            this.loading = false
        },
        //向上移动
        moveUp(index,row) {
            var that = this;
            console.log('上移',index,row);
            console.log(that.PackageList[index]);
            if (index > 0) {
                let upDate = that.PackageList[index - 1];
                that.PackageList.splice(index - 1, 1);
                that.PackageList.splice(index,0, upDate);
            } else {
                alert('已经是第一条，不可上移');
            }
        },
        //向下移动
        moveDown(index,row){
            var that = this;
            console.log('下移',index,row);
            if ((index + 1) === that.PackageList.length){
                alert('已经是最后一条，不可下移');
            } else {
                console.log(index);
                let downDate = that.PackageList[index + 1];
                that.PackageList.splice(index + 1, 1);
                that.PackageList.splice(index,0, downDate);
            }
        },
    }
};
</script>
<style>

</style>