<template>
    <div>
        <a :href="iframe_url" title="将我拖动到书签栏">小书签</a>
    </div>
    <el-card style="margin-top: 20px;">
        <body>
            <h2>元素选择器</h2>
            <p>元素选择器类型可以选择 Xpath 或 Css selector。</p>
            <p>一行一个元素选择器，每一行的格式为：选择器类型{选择器内容}，例如：</p>
            <code>xpath://body/div/span[contains(@class,’example-class’]</code>
            <p>可以借助浏览器 F12 直接 copy 这两种选择器，或者系统提供的小书签工具。</p>
            <h3>实例</h3>
            <p>例如监控百度热点，打开网址<a href="https://top.baidu.com/board?platform=pc&sa=pcindex_entry">https://top.baidu.com/board?platform=pc&sa=pcindex_entry</a></p>
            <p>方法一：借助浏览器 F12 直接 copy 这两种选择器，按 F12 或者点击鼠标右键 -&gt; 检查，进而调出开发者工具</p>
            <ol>
                <li>按左上角的小箭头（Ctrl+Shift+C）开启选择模式</li>
                <li>选定区域后右键高亮的代码</li>
                <li>Copy –&gt; Copy XPath</li>
            </ol>
            <img style="width: 60%; height: 60%" src="../../images/Baidu_F12.png" />
            <p>方法二：小书签工具</p>
            <ol>
                <li>拖动上方小书签至浏览器导航栏</li>
                <li>打开监控网址后，点击浏览器导航栏上的小书签按钮</li>
                <li>选定区域后点击高亮的部分，页面下方自动获取XPath</li>
            </ol>
            <img style="width: 60%; height: 60%" src="../../images/Baidu_bookmarklet.png" />
            <p>在空间中添加监控任务</p>
            <ul>
                <li>监控名：随便</li>
                <li>监控说明：随便</li>
                <li>监控网址：填写监控网址</li>
                <li>关键词：填写监控关键词，监控内容为该关键词，出现即可触发</li>
                <li>监控元素：可监控整个网页，或者选择元素选择器（XPath 和 CssSelector），粘贴上一步复制的 XPath 或者 CssSelector 内容，可添加多个选择器，例如：<br>
                xpath:复制的 XPath 内容<br>
                css:复制的 CssSelector 内容
                </li>
                <li>刷新频率：默认抓取频率为一小时，自行根据需要调整</li>
                <li>通知邮箱：随便</li>
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
