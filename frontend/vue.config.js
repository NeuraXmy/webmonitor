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
    },
    chainWebpack: config => {
        config.plugin('html')
          .tap(args => {
            args[0].contentSecurityPolicy = {
              useDefaults: true,
              directives: {
                defaultSrc: ["'self'"]
                // 其他指令...
              }
            };
            return args;
        });
    }
}