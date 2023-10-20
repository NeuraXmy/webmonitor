import AdminService from './../services/admin'
import {ElMessage} from 'element-plus'
import {useRouter} from 'vue-router'
function Admin_Manage(){

    
    const router = useRouter();
    function Admin_Login(user,psw){
        AdminService.admin_login(user,psw).then((data)=>{
            if(data.data.code==200){
                //成功
                ElMessage.success("登录成功");
                router.push("home");
            }else{
                ElMessage.warning(data.data.msg);
            }
        }).catch(err=>{
            console(err);
            ElMessage.error("请求出错");
        });
    }
    function Add_Admin(){

    }
    function AdminListBYPage(){

    }
    function AdminCountBySearchName(){

    }
    return{
        Admin_Login,
        Add_Admin,
        AdminListBYPage,
        AdminCountBySearchName
    }
}

export default Admin_Manage