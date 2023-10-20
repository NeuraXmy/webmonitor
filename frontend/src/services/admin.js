import axios from './../utils/axios'
import api from './../api'
// 获取管理员数据 根据页面与管理员姓名
function getAdminListBySearchAndPage({currentPage,pageSize,searchName}){
    return axios({
        url:api.admin.GetAdminListBySearchAndPage,
        method:"post",
        data:{
            currentPage,
            pageSize,
            searchName
        }
    })
}

// 获取管理员的总条数 根据页面与管理员姓名
function getAdminListBySearchCount({searchName}){
    return axios({
        url:api.admin.GetAdminListBySearchCount,
        method:"post",
        data:{
            searchName
        }
    })
}

//删除管理员
function delAdminById(id){
    return axios({
        url:api.admin.DelAdminById,
        method:"get",
        params:{
            id
        }
    })
}

//获取管理员数据，根据管理员id
function getAdminInfoById(id){
    return axios({
        url:api.admin.GetAdminInfoById,
        method:"get",
        params:{
            id
        }
    })
}
//更新管理员数据 ，根据管理员id
function updateAdminInfoById(userInfo){
    return axios({
        url:api.admin.UpdateAdminInfoById,
        method:"post",
        data:userInfo
    })
}


//添加管理员
function add_admin({user,pwd,rePwd,name,type}){
    return axios({
        url:api.admin.Add_admin,
        method:"post",
        data:{
          user,pwd,rePwd,name,type
        }
    })
}
//管理员登录
function admin_login(user,pwd){
    return axios({
        url:api.admin.Admin_login,
        method:"post",
        data:{
           user,pwd
        }
    })
}
export default {
    getAdminListBySearchAndPage,
    getAdminListBySearchCount,
    delAdminById,
    updateAdminInfoById,
    getAdminInfoById,
    admin_login,
    add_admin
}