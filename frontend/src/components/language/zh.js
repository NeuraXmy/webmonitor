// 1、创建中文语言包对象
export default{
    name: "多模态信息舆论监控",
    home: {
        space: "空间",
        monitor: "监控",
        subscribe: "购买订阅",
        order: "我的订单",
        tool: "工具"
    },
    table: {
        username: '用户名',
        email: '邮箱',
        mobile: '手机'
    },
    breadcrumbs: {
        home: "首页",
        spaces: "空间"
    },
    tabs: {
        editSpace: "编辑空间",
        deleteSpace: "删除空间",
        addMonitor: "新增监控网址",
        editMonitor: "编辑监控信息",
        deleteWatch: "删除监控",
        refreshWatch: "刷新监控",
        historyWatch: "检查记录"
    },
    buttons: {
        addSpace: "新增空间",
        editSpace: "编辑空间",
        deleteSpace: "删除空间",
        addMonitor: "新增监控",
        editMonitor: "编辑监控",
        deleteWatch: "删除监控",
        refreshWatch: "刷新监控",
        historyWatch: "检查记录",
        cancel: "取消",
        confirm: "确定"
    },
    tableColumns: {
        id: "ID",
        name: "监控名",
        url: "网址",
        lastCheckTime: "检查时间",
        lastCheckState: "检查状态",
        last24hCheckCount: "24小时检查次数",
        last24hNotificationCount: "24小时触发警报次数",
        paused: "是否启用",
        edit: "Edit"
    },
    switch: {
        on: "ON",
        off: "OFF"
    },
    messages: {
        deleteSpaceConfirm: "是否删除监控？",
        refreshWatchSuccess: "刷新监控成功.",
        quotaExceeded: "监控套餐次数已超限，所有监控暂停！"
    },
    placeholders: {
        nickname: "请输入昵称",
        spaceDescription: "请输入空间说明",
        monitorName: "请输入监控名",
        monitorDescription: "请输入监控说明",
        monitorUrl: "请输入网址（http://或https://开头）",
        monitorKeywords: "请输入监控关键词",
        monitorElement: "请输入监控元素（XPath/CssSelector）",
        refreshFrequency: "刷新频率",
        notificationEmail: "请输入通知邮箱"
    },
    monitor: {
        home: '首页',
        monitoring: '监控',
        consumption: {
            thisMonth: '本月消耗次数',
            today: '今日消耗次数',
            yesterday: '昨日消耗次数',
            todayAlerts: '今日触发警报次数',
            chatLineIcon: '聊天图标',
        },
        actions: {
            deleteMonitors: '批量删除',
            closeMonitors: '批量关闭',
        },
        table: {
            id: 'ID',
            monitorName: '监控名',
            url: '网址',
            checkTime: '检查时间',
            checkStatus: '检查状态',
            last24hCheckCount: '24小时检查次数',
            last24hAlerts: '24小时触发警报次数',
            enable: '是否启用',
            edit: '编辑',
            delete: '删除',
            refresh: '刷新',
            history: '检查记录',
        },
        dialogs: {
            addMonitor: {
                title: '新增监控网址',
                monitorName: '监控名',
                monitorDesc: '监控说明',
                url: '网址',
                keyword: '关键词',
                element: '监控元素',
                refreshTime: '刷新时间',
                notificationEmail: '通知邮箱',
                cancel: '取消',
                confirm: '确定',
            },
            editMonitor: {
                title: '编辑监控信息',
                monitorName: '监控名',
                monitorDesc: '监控说明',
                url: '网址',
                keyword: '关键词',
                element: '监控元素',
                refreshTime: '刷新时间',
                notificationEmail: '通知邮箱',
                cancel: '取消',
                confirm: '确定',
            },
            confirmDeleteWatch: {
                message: '是否删除监控？',
                cancel: '取消',
                confirm: '确定',
            },
            refreshWatchSuccess: '刷新监控成功',
            confirmDeleteMonitors: {
                message: '你确定要删除选中项吗？',
                cancel: '取消',
                confirm: '确定',
            },
            confirmCloseMonitors: {
                message: '你确定要关闭选中项吗？',
                cancel: '取消',
                confirm: '确定',
            },
            quotaExceeded: '监控套餐次数已超限，所有监控暂停！',
        },
    }
}
//昵称,空间说明