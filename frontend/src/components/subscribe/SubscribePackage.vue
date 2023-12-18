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
    <div v-if="checkedCycle === true">
        <el-row :gutter="12" style="margin-top: 20px;">
            <el-col
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
                                <p class="h6 text-muted">月付</p>
                            </div>
                        </div>
                        <div class="block-content py-3">
                            <div class="mb-3">
                                每月x次监控次数<br>
                            </div>
                            <el-button style="margin-top: 20px;" type="primary" size="small">立即订阅</el-button>
                        </div>
                    </el-card>
                </div>
            </el-col>
        </el-row>
    </div>
    <div v-if="checkedFrequency === true">
        <el-row :gutter="12" style="margin-top: 20px;">
            <div style="width: 29%;">
                <el-card class="block block-link-pop block-rounded m-3 mx-xl-0" shadow="hover">
                    <div class="block-header plan">
                        <h3 class="block-title">次数包</h3>
                    </div>
                    <div class="block-content bg-gray-light">
                        <div class="py-2">
                            <p class="h1 mb-2">¥ 25.00</p>
                            <p class="h6 text-muted">一次性</p>
                        </div>
                    </div>
                    <div class="block-content py-3">
                        <div class="mb-3">
                            x次监控次数用完为止<br>
                        </div>
                        <el-button style="margin-top: 20px;" type="primary" size="small">立即订阅</el-button>
                    </div>
                </el-card>
            </div>
        </el-row>
    </div>
    <!-- <el-card style="margin-top: 20px;">
        
    </el-card> -->
</template>

<script>
export default {
    data(){
        return {
            Packages:[
                {
                    name: "标准",
                    price: 10.00
                },
                {
                    name: "进阶",
                    price: 20.00
                },
                {
                    name: "高阶",
                    price: 30.00
                }
            ],
            checkedCycle:true,
            checkedFrequency:false
        }
    },
    created(){
        // this.getBookmark()
    },
    methods: {
        onChangeCycle(){
            this.checkedCycle = true;
            this.checkedFrequency = false;
        },
        onChangeFrequency(){
            this.checkedCycle = false;
            this.checkedFrequency = true;
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