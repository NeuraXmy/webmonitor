// 2、创建英文语言包对象
export default {
    name: "changenotify",
    home: {
        space: "Spaces",
        monitor: "Monitors",
        subscribe: "Purchase Subscription",
        order: "My Orders",
        tool: "Tools"
    },
    table: {
        username: 'Username',
        email: 'Email',
        mobile: 'Mobile'
    },
    breadcrumbs: {
        home: "Home",
        spaces: "Spaces"
    },
    tabs: {
        editSpace: "Edit Space",
        deleteSpace: "Delete Space",
        addMonitor: "Add Monitor",
        editMonitor: "Edit Monitor",
        deleteWatch: "Delete Watch",
        refreshWatch: "Refresh Watch",
        historyWatch: "History Watch"
    },
    buttons: {
        addSpace: "Add Space",
        editSpace: "Edit Space",
        deleteSpace: "Delete Space",
        addMonitor: "Add Monitor",
        editMonitor: "Edit Monitor",
        deleteWatch: "Delete Watch",
        refreshWatch: "Refresh Watch",
        historyWatch: "History Watch",
        cancel: "Cancel",
        confirm: "Confirm"
    },
    tableColumns: {
        id: "ID",
        name: "Name",
        url: "URL",
        lastCheckTime: "Last Check Time",
        lastCheckState: "Last Check State",
        last24hCheckCount: "Last 24h Check Count",
        last24hNotificationCount: "Last 24h Notification Count",
        paused: "Paused",
        edit: "Edit"
    },
    switch: {
        on: "ON",
        off: "OFF"
    },
    messages: {
        deleteSpaceConfirm: "Are you sure you want to delete this space?",
        refreshWatchSuccess: "Watch refreshed successfully",
        quotaExceeded: "Watch quota exceeded. All watches paused!"
    },
    placeholders: {
        nickname: "Enter nickname",
        spaceDescription: "Enter space description",
        monitorName: "Enter monitor name",
        monitorDescription: "Enter monitor description",
        monitorUrl: "Enter URL (starting with http:// or https://)",
        monitorKeywords: "Enter monitor keywords",
        monitorElement: "Enter monitor element (XPath/CssSelector)",
        refreshFrequency: "Refresh Frequency",
        notificationEmail: "Enter notification email"
    },
    monitor: {
        home: 'Home',
        monitoring: 'Monitoring',
        consumption: {
            thisMonth: 'Consumption This Month',
            today: 'Consumption Today',
            yesterday: 'Consumption Yesterday',
            todayAlerts: 'Today\'s Alerts',
            chatLineIcon: 'Chat Line Icon',
        },
        actions: {
            deleteMonitors: 'Batch Delete',
            closeMonitors: 'Batch Close',
        },
        table: {
            id: 'ID',
            monitorName: 'Monitor Name',
            url: 'URL',
            checkTime: 'Check Time',
            checkStatus: 'Check Status',
            last24hCheckCount: 'Last 24h Check Count',
            last24hAlerts: 'Last 24h Alerts',
            enable: 'Enable',
            edit: 'Edit',
            delete: 'Delete',
            refresh: 'Refresh',
            history: 'Check History',
        },
        dialogs: {
            addMonitor: {
                title: 'Add Monitor URL',
                monitorName: 'Monitor Name',
                monitorDesc: 'Monitor Description',
                url: 'URL',
                keyword: 'Keyword',
                element: 'Monitor Element',
                refreshTime: 'Refresh Time',
                notificationEmail: 'Notification Email',
                cancel: 'Cancel',
                confirm: 'Confirm',
            },
            editMonitor: {
                title: 'Edit Monitor Information',
                monitorName: 'Monitor Name',
                monitorDesc: 'Monitor Description',
                url: 'URL',
                keyword: 'Keyword',
                element: 'Monitor Element',
                refreshTime: 'Refresh Time',
                notificationEmail: 'Notification Email',
                cancel: 'Cancel',
                confirm: 'Confirm',
            },
            confirmDeleteWatch: {
                message: 'Do you want to delete the monitor?',
                cancel: 'Cancel',
                confirm: 'Confirm',
            },
            refreshWatchSuccess: 'Monitor refreshed successfully',
            confirmDeleteMonitors: {
                message: 'Are you sure you want to delete the selected items?',
                cancel: 'Cancel',
                confirm: 'Confirm',
            },
            confirmCloseMonitors: {
                message: 'Are you sure you want to close the selected items?',
                cancel: 'Cancel',
                confirm: 'Confirm',
            },
            quotaExceeded: 'Monitor package limit exceeded, all monitors paused!',
        },
    }
}