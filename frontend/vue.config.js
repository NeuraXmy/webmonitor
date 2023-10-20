module.exports= {
    devServer:{
        proxy:{
            '/':{
                target: 'http://localhost:23456',
                changeOrigin:true,
                pathRewrite:{
                    '^/': '/'
                }
            }
        }
    }
}