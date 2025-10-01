module.exports = {
  root: true,
  env: {
    node: true,
    'vue/setup-compiler-macros': true, 
  },
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended',
  ],
  parserOptions: {
    // ✅ 수정된 부분: 최신 파서로 변경
    parser: '@babel/eslint-parser',
    // Babel 설정 파일이 없어도 파서가 동작하도록 설정
    requireConfigFile: false, 
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    // 'no-unused-vars' 규칙을 경고 수준으로 낮추어 빌드 실패를 방지
    'no-unused-vars': 'warn', 
  },
};

