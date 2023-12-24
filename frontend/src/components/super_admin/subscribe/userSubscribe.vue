<template>
    <div>
        <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item :to="{ path: '/userlist' }">用户管理</el-breadcrumb-item>
            <el-breadcrumb-item>用户套餐</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-row>
                <el-button type="primary" @click="AddPackage"><el-icon><Plus /></el-icon>新增套餐</el-button>
            </el-row>
            <el-row>
                <el-table v-loading="loading" :data="OrderList" style="width: 100%">
                    <el-table-column prop="id" label="ID" width="50" />
                    <el-table-column prop="create_time" label="创建时间" width="200" />
                    <el-table-column prop="name" label="套餐名称" width="150" />
                    <el-table-column prop="period_type" label="周期" width="150" />
                    <el-table-column prop="period_check_count" label="监控总次数" width="150" />
                    <el-table-column prop="price" label="订单金额(元)" width="150" />
                    <!-- <el-table-column prop="check_count_left" label="监控剩余次数" width="150" /> -->
                    <el-table-column prop="edit" label="操作" width="200">
                        <template #default="scope">
                            <!-- <el-button size="small" @click="PackageEdit(scope.row)"
                            >更换</el-button
                            > -->
                            <el-button
                                size="small"
                                type="danger"
                                @click="DeletePackage(scope.row)"
                                >删除</el-button
                            >
                        </template> 
                    </el-table-column>
                </el-table>
                <el-pagination
                    v-model:current-page="queryPage.page"
                    v-model:page-size="queryPage.size"
                    :page-sizes="[5, 10, 20, 50]"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="TotalPages"
                    @size-change="handleSizeOrderChange"
                    @current-change="handleCurrentOrderChange"
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
            <el-form-item label="选择套餐" prop="name">
                <el-col :span="20">
                    <el-select v-model="SelectPackageID" placeholder="Select" @change="ChangePackage">
                        <el-option
                            v-for="item in PackageList"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                        />
                    </el-select>
                </el-col>
            </el-form-item>
            <!-- <el-form-item label="周期数" prop="period_count">
                <el-col :span="20">
                    <el-input v-model="PackageForm.period_count" placeholder="请输入周期数"></el-input>
                </el-col>
            </el-form-item> -->
            <el-form-item label="周期">
                <el-col :span="20">
                    <el-select disabled v-model="PackageForm.period_type" placeholder="Select" @change="ChangePackage_type">
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
                    <el-input disabled v-model="PackageForm.period_check_count" placeholder="请输入监控次数"></el-input>
                </el-col>
            </el-form-item>
            <!-- <el-form-item label="周期" prop="name">
                <el-col :span="20">
                    <el-input v-model="PackageForm.period_type" placeholder="请输入周期"></el-input>
                </el-col>
            </el-form-item> -->
            <el-form-item label="价格(分)" prop="price">
                <el-col :span="20">
                    <el-input disabled v-model="PackageForm.price" placeholder="请输入价格"></el-input>
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
    <!-- <el-dialog
      v-model="okEditPackage"
      title="编辑套餐"
      width="40%"
    >
        <el-form ref="PackageRef" :rules="PackageRules" :model="PackageForm" label-width="80px" class="form_style">
            <el-form-item label="套餐名称" prop="name">
                <el-col :span="20">
                    <el-input disabled v-model="PackageForm.name" placeholder="请输入套餐名称"></el-input>
                </el-col>
            </el-form-item>
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
            <el-form-item label="价格(分)" prop="price">
                <el-col :span="20">
                    <el-input v-model="PackageForm.price" placeholder="请输入价格"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="剩余次数" prop="check_count_left">
                <el-col :span="20">
                    <el-input v-model="PackageForm.check_count_left" placeholder="请输入套餐剩余次数"></el-input>
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
    </el-dialog> -->
</template>

<script>
import { Search,Plus,Delete,Edit } from '@element-plus/icons-vue'
export default{
    
    components: { Search,Plus,Delete,Edit },
    data(){
        return {
            OrderList:[
                
            ],
            loading:false,
            TotalPages: 10,
            queryPage: {
                page:1,
                size:10
            },
            UserID:'',
            okEditPackage:false,
            PackageRules:{
                name:[
                    {required:true, message: '请输入套餐名称', trigger:'blur'},
                ],
                period_type:[
                    {required:true, message: '请输入周期', trigger:'blur'}
                ],
                price:[
                    {required:true, message: '请输入价格', trigger:'blur'}
                ],
                period_check_count:[
                    {required:true, message: '请输入监控次数', trigger:'blur'}
                ],
                period_count:[
                    {required:true, message: '请输入周期次数', trigger:'blur'}
                ],
                check_count_left:[
                    {required:true, message: '请输入剩余监控次数', trigger:'blur'}
                ]
            },
            PackageForm:{
                name:'test',
                period_type:0,
                period_count:1,
                price:0,
                period_check_count:1,
                check_count_left:1,
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
            okAddPackage:false,
            PackageList:[],
            SelectPackageID:1,
            okDeletePackage:false
        }
    },
    created(){
        this.getPackagesList()
        this.getOrderList()
    },
    methods: {
        async getOrderList(){
            this.loading = true
            this.UserID = sessionStorage.getItem('UserID')
            const {data: res} = await this.$axios.get('/user/' +  this.UserID + '/package',
            {
                params: this.queryPage,
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            // console.log(res)
            this.TotalPages = res.data.total
            this.OrderList = res.data.items
            for(let i = 0; i < this.OrderList.length; i++){
                this.OrderList[i].price /= 100.0
                if(this.OrderList[i].period_type === 0) this.OrderList[i].period_type = "一次性";
                else if(this.OrderList[i].period_type === 1) this.OrderList[i].period_type = "日付";
                else if(this.OrderList[i].period_type === 2) this.OrderList[i].period_type = "月付";
                else if(this.OrderList[i].period_type === 3) this.OrderList[i].period_type = "年付";
            }
            this.loading = false
            // console.log(this.OrderList)
        },
        //获得所有套餐
        async getPackagesList(){
            this.loading = true
            const {data: res} = await this.$axios.get('/package/template',
            {
                // params: this.queryPage,
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            // console.log(res)
            this.loading = false
            // this.TotalPages = res.data.total
            this.PackageList = res.data.items
            console.log(this.PackageList)
            this.SelectPackageID = this.PackageList[0].id
            this.PackageForm.period_type = this.PackageList[0].period_type
            this.PackageForm.period_check_count = this.PackageList[0].period_check_count
            this.PackageForm.price = this.PackageList[0].price
            this.PackageForm.hide = this.PackageList[0].hide
            this.PackageForm.initial = this.PackageList[0].initial;
        },
        //编辑套餐
        PackageEdit(row){
            this.okEditPackage = true;
            this.Package_id = row.id;
            for(let i = 0; i < this.OrderList.length; i++){
                if(this.OrderList[i].id === row.id){
                    this.PackageForm.name = this.OrderList[i].name;
                    this.PackageForm.period_type = this.OrderList[i].period_type;
                    this.PackageForm.period_count = this.OrderList[i].period_count;
                    this.PackageForm.price = this.OrderList[i].price;
                    this.PackageForm.period_check_count = this.OrderList[i].period_check_count;
                    this.PackageForm.check_count_left = this.OrderList[i].check_count_left;
                    
                    if(this.PackageForm.period_type === "一次性") this.PackageForm.period_type = 0;
                    else if(this.PackageForm.period_type === "日付") this.PackageForm.period_type = 1;
                    else if(this.PackageForm.period_type === "月付") this.PackageForm.period_type = 2;
                    else if(this.PackageForm.period_type === "年付") this.PackageForm.period_type = 3;
                    break;
                }
            }
            console.log(this.OrderList)
            console.log(this.PackageForm)
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
                const {data: res} = await this.$axios.put('/package/'+this.Package_id,data,
                {
                    headers : {
                        'token': sessionStorage.getItem('token')
                    }
                })
                if(res.status ===200){
                    this.getOrderList()
                }else{
                    this.$message.error(res.msg);
                }
                this.loading = false
            })
        },
        //添加套餐
        AddPackage(){
            this.okAddPackage = true;
        },
        //确定添加套餐
        AddPackageConfirm(){
            this.$refs.PackageRef.validate(async valid => {
                console.log(valid)
                if(!valid) return ;
                this.okAddPackage = false
                this.loading = true
                // console.log(this.SelectPackageID)
                let data = this.$qs.stringify(this.PackageForm)
                console.log(this.PackageForm)
                const {data: res} = await this.$axios.post('/package/purchase/'+this.SelectPackageID+'/user/'+this.UserID ,data,
                {
                    headers : {
                        'token': sessionStorage.getItem('token')
                    }
                })
                if(res.status ===200){
                    this.getOrderList()
                }else{
                    this.$message.error(res.msg);
                }
                this.loading = false
            })
        },
        //获得套餐页号
        handleCurrentOrderChange(val){
            this.queryPage.page = val
            this.getOrderList()
        },
        //获得套餐页数
        handleSizeOrderChange(val){
            this.queryPage.size = val
            this.getOrderList()
        },
        //选择指定用户套餐
        ChangePackage(){
            for(let i = 0; i < this.PackageList.length; i++){
                if(this.SelectPackageID === this.PackageList[i].id){
                    this.PackageForm.name = this.PackageList[i].name
                    this.PackageForm.period_type = this.PackageList[i].period_type
                    this.PackageForm.period_check_count = this.PackageList[i].period_check_count
                    this.PackageForm.price = this.PackageList[i].price
                    this.PackageForm.hide = this.PackageList[i].hide
                    this.PackageForm.initial = this.PackageList[i].initial;
                }
            }
        },
        //删除套餐
        DeletePackage(row){
            this.Package_id = row.id;
            this.okDeletePackage = true;
        },
        //确定删除套餐
        async ConfirmDeletePackage(){
            this.okDeletePackage = false;
            this.loading = true
            const {data: res} = await this.$axios.delete('/package/'+this.Package_id,
            {
                // params:{id: this.okDeleteSubscribe},
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.getOrderList()
            this.loading = false
        },
    }
};
</script>
<style>

</style>