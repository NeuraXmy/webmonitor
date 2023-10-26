<template>
    <div>
      <el-breadcrumb :separator-class="el-icon-arrow-right">
          <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>任务管理</el-breadcrumb-item>
          <el-breadcrumb-item>网页监控管理</el-breadcrumb-item>
          <!-- <el-breadcrumb-item>promotion detail</el-breadcrumb-item> -->
      </el-breadcrumb>
      <el-card>
        <el-row>
            <el-col :span="2">
                <div>
                    <el-button type="primary" :icon="Plus">增加</el-button>
                </div>
            </el-col>
            <el-col :span="2">
                <div>
                    <el-button type="success" :icon="Delete">删除</el-button>
                </div>
            </el-col>
        </el-row>
        <el-row>
            <el-table :data="tableData" style="width: 100%">
                <el-table-column prop="date" label="创建时间" width="180" />
                <el-table-column prop="name" label="监控网址" width="180" />
                <el-table-column prop="name" label="ID" width="180" />
                <el-table-column prop="name" label="昵称" width="180" />
                <el-table-column prop="name" label="更新时间" width="180" />
            </el-table>
        </el-row>
      </el-card>
    </div>
  </template>
  <script setup>
  import { Search,Plus,Delete } from '@element-plus/icons-vue'
  </script>
  
  <style>
  .input-with-select .el-input-group__prepend {
    background-color: var(--el-fill-color-blank);
  }
  </style>