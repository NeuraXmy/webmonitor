<template>
    <div>
      <el-breadcrumb>
        <el-breadcrumb-item :to="{ path: '/home' }">{{ $t('tools.home') }}</el-breadcrumb-item>
        <el-breadcrumb-item>{{ $t('tools.tools') }}</el-breadcrumb-item>
      </el-breadcrumb>
      <a :href="iframe_url" :title="$t('tools.bookmark')">{{ $t('tools.bookmark') }}</a>
    </div>
    <el-card style="margin-top: 20px;">
      <body>
        <h2>{{ $t('tools.elementSelector') }}</h2>
        <p>{{ $t('tools.xpathOrCssSelector') }}</p>
        <p>{{ $t('tools.exampleSelector') }}</p>
        <code>xpath://body/div/span[contains(@class, "example-class")]</code>
        <p>{{ $t('tools.copySelectors') }}</p>
        <h3>{{ $t('tools.instance') }}</h3>
        <p>{{ $t('tools.openUrl') }}<a href="https://top.baidu.com/board?platform=pc&sa=pcindex_entry">https://top.baidu.com/board?platform=pc&sa=pcindex_entry</a></p>
        <p>{{ $t('tools.methodOne') }}</p>
        <ol>
          <li>{{ $t('tools.selectMode') }}</li>
          <li>{{ $t('tools.rightClick') }}</li>
          <li>{{ $t('tools.copyXPath') }}</li>
        </ol>
        <img style="width: 60%; height: 60%" src="../../images/Baidu_F12.png" />
        <p>{{ $t('tools.methodTwo') }}</p>
        <ol>
          <li>{{ $t('tools.dragBookmark') }}</li>
          <li>{{ $t('tools.clickBookmark') }}</li>
          <li>{{ $t('tools.highlightArea') }}</li>
        </ol>
        <img style="width: 60%; height: 60%" src="../../images/Baidu_bookmarklet.png" />
        <p>{{ $t('tools.addMonitoringTask') }}</p>
        <ul>
          <li>{{ $t('tools.monitoringName') }}</li>
          <li>{{ $t('tools.monitoringDescription') }}</li>
          <li>{{ $t('tools.monitoringUrl') }}</li>
          <li>{{ $t('tools.keywords') }}</li>
          <li>{{ $t('tools.monitoringElement') }}
            <br>{{ $t('tools.xpath') }}<br>{{ $t('tools.css') }}
          </li>
          <li>{{ $t('tools.refreshRate') }}</li>
          <li>{{ $t('tools.notificationEmail') }}</li>
        </ul>
        <img style="width: 60%; height: 60%" src="../../images/Add_monitor.png" />
      </body>
    </el-card>
</template>
  

<script>
export default {
    data(){
        return {
            iframe_url:''
        }
    },
    created(){
        this.getBookmark()
    },
    methods: {
        async getBookmark(){
            const {data: res} = await this.$axios.get('/bookmark/inject.js',
            {
                headers : {
                    'token': sessionStorage.getItem('token')
                }
            })
            this.iframe_url = res.data
        }
    }
};
</script>
