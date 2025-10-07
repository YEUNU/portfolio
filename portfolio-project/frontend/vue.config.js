const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  
  // SEO 최적화를 위한 설정
  chainWebpack: config => {
    // HTML 플러그인 설정
    config.plugin('html').tap(args => {
      args[0].title = '성연우의 포트폴리오 | 개발자 포트폴리오'
      args[0].meta = {
        viewport: 'width=device-width,initial-scale=1.0',
        'theme-color': '#121212'
      }
      return args
    })
    
    // preload 플러그인이 존재하는지 확인 후 설정
    if (config.plugins.has('preload')) {
      config.plugin('preload').tap(options => {
        options[0] = {
          rel: 'preload',
          include: 'initial',
          fileBlacklist: [/\.map$/, /hot-update\.js$/]
        }
        return options
      })
    }
    
    // prefetch 플러그인이 존재하는지 확인 후 설정
    if (config.plugins.has('prefetch')) {
      config.plugin('prefetch').tap(options => {
        options[0].fileBlacklist = options[0].fileBlacklist || []
        options[0].fileBlacklist.push(/\.map$/, /hot-update\.js$/)
        return options
      })
    }
  },
  
  // 개발 서버 설정
  devServer: {
    port: 3000,
    open: true
  },
  
  // 빌드 최적화
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all',
          }
        }
      }
    }
  }
})