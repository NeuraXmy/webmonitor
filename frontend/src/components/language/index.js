import { createI18n } from 'vue-i18n'
// 从语言包文件中导入语言包对象
import zh from './zh'
import en from './en'

const messages = {
    zh,
    en
}
const i18n = createI18n({
    messages,
    locale: 'zh'
})

export default i18n
