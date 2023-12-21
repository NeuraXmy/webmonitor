<template>
    <div>
        <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>购买订阅</el-breadcrumb-item>
        </el-breadcrumb>
        <h2>选择最合适您的套餐</h2>
        <div>
            <el-check-tag :checked="checkedCycle" style="margin-right: 8px" @change="onChangeCycle">按周期</el-check-tag>
            <el-check-tag :checked="checkedFrequency" @change="onChangeFrequency">按次数</el-check-tag>
        </div>
    </div>
    <div v-loading="loading">
        <el-row :gutter="30" style="margin-top: 20px;">
            <el-col
                style="margin-top: 20px;"
                v-for="item in Packages"
                :key=item.index
                :span="7"
            >
                <div class="col-md-12 col-xl-4">
                    <el-card class="block block-link-pop block-rounded m-3 mx-xl-0" shadow="hover">
                        <div class="block-header plan">
                            <h3 class="block-title">{{ item.name }}</h3>
                        </div>
                        <div class="block-content bg-gray-light">
                            <div class="py-2">
                                <p class="h1 mb-2">¥ {{ item.price }}</p>
                                <p class="h6 text-muted">{{ item.period_type }}</p>
                            </div>
                        </div>
                        <div class="block-content py-3">
                            <div class="mb-3">
                                监控次数 {{ item.period_check_count }}<br>
                            </div>
                            <el-button style="margin-top: 20px;" type="primary" size="small" @click="SubscribePackage(item.id)">立即订阅</el-button>
                        </div>
                    </el-card>
                </div>
            </el-col>
        </el-row>
    </div>
    <el-dialog
        v-model="okSubscribePackage"
        width="30%"
        align-center
        >
        <span>是否订阅该套餐？</span>
        <template #footer>
            <span class="dialog-footer">
            <el-button @click="okSubscribePackage = false">取消</el-button>
            <el-button type="primary" @click="ConfirmSubscribePackage">
                确定
            </el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script>
export default {
    data(){
        return {
            Packages:[
                // {
                //     name: "标准",
                //     price: 10.00
                // }
            ],
            PackageList:[],
            PackagesCycle:[],
            PackagesFrequency:[],
            checkedCycle:true,
            checkedFrequency:false,
            okSubscribePackage:false,
            Package_id:1,
            loading:false
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
            this.loading = false
            this.PackageList = res.data.items
            this.PackagesCycle = []
            this.PackagesFrequency = []
            // console.log(res.data.items)
            for(let i = 0; i < this.PackageList.length; i++){
                this.PackageList[i].price/=100.0;
                if(this.PackageList[i].period_type === 0) this.PackageList[i].period_type = "一次性";
                else if(this.PackageList[i].period_type === 1) this.PackageList[i].period_type = "日付";
                else if(this.PackageList[i].period_type === 2) this.PackageList[i].period_type = "月付";
                else if(this.PackageList[i].period_type === 3) this.PackageList[i].period_type = "年付";
                if(this.PackageList[i].period_type === "一次性") this.PackagesFrequency.push(this.PackageList[i]);
                else this.PackagesCycle.push(this.PackageList[i]);
            }
            this.Packages = this.PackagesCycle;
        },
        //订阅套餐
        SubscribePackage(id){
            this.okSubscribePackage = true;
            this.Package_id = id
        },
        //确定订阅套餐
        async ConfirmSubscribePackage(){
            this.okSubscribePackage = false
            // this.loading = true
            let data = sessionStorage.getItem('token')
            const {data: res} = await this.$axios.post('/package/purchase/' + this.Package_id,data,
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
            // this.loading = false
        },
        onChangeCycle(){
            this.checkedCycle = true;
            this.checkedFrequency = false;
            this.Packages = this.PackagesCycle;
        },
        onChangeFrequency(){
            this.checkedCycle = false;
            this.checkedFrequency = true;
            this.Packages = this.PackagesFrequency;
        }

    }
};
</script>
<style>
.col-xl-4 {
    flex: 0 0 33.333333%;
    max-width: 33.333333%
}
.col-md-12 {
    flex: 0 0 100%;
    max-width: 100%
}
.block.block-rounded {
    border-radius: .25rem
}
.block.block-bordered {
    border: 1px solid #e4e9f3;
    box-shadow: none
}
.block-content {
    transition: opacity .25s ease-out;
    /* width: 100%; */
    margin: 0 auto;
    padding: 1.25rem 1.25rem 1px;
    overflow-x: visible
}
.mb-2 {
    margin-bottom: .5rem!important
}
.h1,h1 {
    font-size: 2.25rem
}
.pt-2,.py-2 {
    padding-top: .5rem!important
}
.bg-gray-light {
    background-color: #e9ecef!important
}
.block-header.plan {
    background-color: #fff!important
}
.h6,h6 {
    font-size: 1rem
}
.text-muted {
    color: #6c757d!important
}
.block-header.plan {
    background-color: #fff!important
}
.block-title {
    flex: 1 1 auto;
    min-height: 1.75rem;
    margin: 5px;
    font-size: 1.125rem;
    font-weight: 400;
    line-height: 1.75
}
</style>