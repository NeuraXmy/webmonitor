<template>
    <div class="row mb-3 mb-md-0">
        <el-card style="width: 100%;margin-bottom: 10px;">
            <h3>当前套餐</h3>
            <div v-if="using !== null">
                <div class="slider-demo-block">
                    <span class="demonstration">使用情况</span>
                    <el-slider v-model="using" disabled />
                </div>
                <span style="font-size: 14px;">已用次数{{using}} / 总次数{{Package.period_check_count}}</span>
            </div>
            <div v-if="using === null">
                <div class="slider-demo-block">
                    <span class="demonstration">当前无套餐</span>
                    <el-slider v-model="using" disabled />
                </div>
                <span style="font-size: 14px;">已用次数0 / 总次数0</span>
            </div>
        </el-card>
        <div class="col-xl-12">
            <div class="block block-rounded js-appear-enabled">
                <div class="block-header block-header-default">
                    <h3 class="block-title"><el-icon><Link /></el-icon>快捷操作</h3>
                </div>
                <div class="block-content p-0">
                    <div class="justify-content-md-between align-items-md-center">
                        <div class="mb-3">
                            <router-link to="/spaces" class="class_href">
                                <div class="v2board-shortcuts-item">
                                    <el-container>
                                        <el-aside width="200px">
                                            <div>添加监控</div>
                                            <div class="description">快速添加监控进行体验</div>
                                        </el-aside>
                                        <el-main>
                                            <i class="nav-main-link-icon " style="float: right;"><el-icon size="30px"><Monitor /></el-icon></i>
                                        </el-main>
                                    </el-container>
                                </div>
                            </router-link>
                            <router-link to="/tools" class="class_href">
                                <div class="v2board-shortcuts-item">
                                    <el-container>
                                        <el-aside width="200px">
                                            <div>查看教程</div>
                                            <div class="description">学习如何使用 changenotify</div>
                                        </el-aside>
                                        <el-main>
                                            <i class="nav-main-link-icon " style="float: right;"><el-icon size="30px"><Reading /></el-icon></i>
                                        </el-main>
                                    </el-container>
                                </div>
                            </router-link>
                            <router-link to="/SubscribePackage" class="class_href">
                                <div class="v2board-shortcuts-item">
                                    <el-container>
                                        <el-aside width="200px">
                                            <div>购买订阅</div>
                                            <div class="description">对您当前的订阅进行购买</div>
                                        </el-aside>
                                        <el-main>
                                            <i class="nav-main-link-icon " style="float: right;"><el-icon size="30px"><ShoppingBag /></el-icon></i>
                                        </el-main>
                                    </el-container>
                                </div>
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { Reading,Monitor,ShoppingBag,Link } from '@element-plus/icons-vue'

export default{
    components: { Reading,Monitor,ShoppingBag,Link },
    data(){
        return {
            using:null,
            Package:{
                period_check_count:null
            }
        }
    },
    created(){
        this.getPackage()
    },
    methods:{
        //获得正在使用的套餐
        async getPackage(){
            // this.loading = true
            const {data: res} = await this.$axios.get('/package/using',
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            if(res.status !== 200) return  this.$message.error(res.msg)
            this.$message.success(res.msg)
            console.log(res)
            this.Package = res.data
            this.using = this.Package.period_check_count - this.Package.check_count_left
            // this.loading = false
            // this.Package = res.data.items
        },
    }
}
</script>

<style scoped>
.row {
    display: flex;
    flex-wrap: wrap;
    margin-right: -14px;
    margin-left: -14px
}
.col-xl-12 {
    flex: 0 0 100%;
    max-width: 100%
}
.mb-md-0,.my-md-0 {
    margin-bottom: 0!important
}
.block.block-rounded {
    border-radius: .25rem
}
.block-header-default {
    background-color: #f8f9fc
}
.block-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: .75rem 1.25rem;
    transition: opacity .25s ease-out
}
.block-title {
    flex: 1 1 auto;
    min-height: 1.75rem;
    margin: 0;
    font-size: 1.125rem;
    font-weight: 400;
    line-height: 1.75
}
.block-content {
    transition: opacity .25s ease-out;
    width: 100%;
    margin: 0 auto;
    padding: 1.25rem 1.25rem 1px;
    overflow-x: visible
}
.class_href {
    text-decoration: none;
    color: inherit; 
}
.align-items-md-center {
    align-items: center!important
}
.justify-content-md-between {
    justify-content: space-between!important
}
.mb-3,.my-3 {
    margin-bottom: 1rem!important
}
.v2board-shortcuts-item {
    cursor: pointer;
    padding: 20px;
    border-bottom: 1px solid #eee;
    position: relative;
    background-color: #f8f9fc
}
.p-0 {
    padding: 0!important
}
.description {
    font-size: 12px;
    opacity: .5
}
.v2board-shortcuts-item:hover {
    background: #f6f6f6
}
.nav-main-link-icon {
    flex: 0 0 auto;
    display: inline-block;
    margin-right: .625rem;
    min-width: 1.25rem;
    font-size: 1rem;
    text-align: center;
    color: rgba(6,101,208,.7)
}
.si-book-open:before {
    content: "\E04C"
}
.slider-demo-block {
  display: flex;
  align-items: center;
}
.slider-demo-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
}
.slider-demo-block .demonstration {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  line-height: 44px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 0;
}
.slider-demo-block .demonstration + .el-slider {
  flex: 0 0 70%;
}
</style>