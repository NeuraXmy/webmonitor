module.exports= {
    devServer:{
        proxy:{
            '/':{
                target: 'http://192.227.148.27:23456/',
                changeOrigin:true,
                pathRewrite:{
                    '^/': '/'
                }
            }
        }
    }
}