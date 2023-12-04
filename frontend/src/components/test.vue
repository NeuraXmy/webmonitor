<template>
    <div style="margin-bottom: 20px">
        <el-button size="small" @click="addTab(editableTabsValue)">
        新增空间
        </el-button>
    </div>
    <el-tabs
        v-model="editableTabsValue"
        type="border-card"
        class="demo-tabs"
        closable
        @tab-remove="removeTab"
    >
        <el-tab-pane
            v-for="item in editableTabs"
            :key="item.name"
            :label="item.title"
            :name="item.name"
        >
        
        </el-tab-pane>
    </el-tabs>
</template>

<script>
import { ref } from 'vue';

export default{
    data(){
        return {
            editableTabs:[
                {
                    title: '默认空间',
                    name: '1',
                    content: 'Tab 1 content',
                },
                {
                    title: 'Tab 2',
                    name: '2',
                    content: 'Tab 2 content',
                },
            ],
            editableTabsValue:''
        }
    },
    created(){
        this.editableTabsValue = '1'
    },
    methods:{
        removeTab(tab){
            console.log(tab)
            console.log(this.editableTabsValue)
        }
    }
}
</script>

<style>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
</style>