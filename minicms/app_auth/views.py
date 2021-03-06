import datetime
import json,re
# import redis
# from statics.scripts import encryption
# from mtrops_v2.settings import SECRET_KEY,DATABASES,REDIS_INFO
from django.views import View
from django.shortcuts import render,HttpResponse,redirect
from app_auth import models as auth_db
from app_log import models as log_db
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from app_auth.perms_control import menus_list,perms_list
from django.contrib.sessions.models import Session

# Create your views here.


class CustomBackend(ModelBackend):
    """自定义登录认证"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = auth_db.User.objects.get(Q(user_name=username) | Q(email=username)| Q(phone=username))
            if user:
                # 加密密码
                # key = SECRET_KEY[2:18]
                # pc = encryption.prpcrypt(key)  # 初始化密钥
                # aes_passwd = pc.encrypt(password)
                aes_passwd = password
                user_passwd = user.passwd.strip("b").strip("'")
                if aes_passwd == user_passwd:
                    return user
        except Exception as e:
            print (e)
            return None


def login_check(func):
    """登录认证装饰器"""
    def wrapper(request,*args,**kwargs):
        next_url = request.get_full_path()
        if request.session.get("username"):
            return func(request, *args, **kwargs)
        else:
            return redirect("/auth/login/?next={}".format(next_url))
    return wrapper



def perms_check(func):
    """权限装饰器"""
    def wrapper(request,*args,**kwargs):
        req_url = request.get_full_path()

        req_url = "/".join(req_url.split("/")[:3]) + "/"

        req_method= request.method

        if request.session['role_id']  == 1:
            return func(request, *args, **kwargs)
        
        try:
            try:
                perms_obj = auth_db.Perms.objects.get(perms_url=req_url)
                url_title = perms_obj.perms_title
            except:
                menu_obj = auth_db.Menus.objects.get(menu_url=req_url)

                req_type = req_method.lower()

                perms_obj = auth_db.Perms.objects.filter(Q(menus_id=menu_obj.id) & Q(perms_req=req_type)).first()

                url_title = perms_obj.perms_title

            perms_all_list = request.session['perms_all_list']


            if req_url in perms_all_list.keys():

                if req_method in perms_all_list[req_url]:
                    log_obj = log_db.UserLog(user_name=request.session['user_name'], ready_name=request.session['username'],
                                             url_title=url_title, status="成功")
                    log_obj.save()
                    return func(request, *args, **kwargs)
                else:
                    log_obj = log_db.UserLog(user_name=request.session['user_name'], ready_name=request.session['username'],
                                             url_title=url_title, status="失败")
                    log_obj.save()
                    return HttpResponse("perms_false")
            else:
                log_obj = log_db.UserLog(user_name=request.session['user_name'], ready_name=request.session['username'], url_title=url_title, status="失败")
                log_obj.save()
                return HttpResponse("perms_false")
        except Exception as e:
            s = str(e)
            s = s.split()[0]

            if s == "Menus":
                print(s)
                e = 'Error: 请求URL权限未添加！'
            return HttpResponse(e)
    return wrapper


class Login(View):
    """登录认证视图"""
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Login, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        处理GET请求
        """
        return render(request, 'login.html')

    def post(self, request):
        """
        处理POST请求
        """
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')

        user = authenticate(username=username, password=passwd)

        if user:
            login(request, user)
            request.session['username'] = user.ready_name
            request.session['user_name'] = user.user_name

            role_id = user.role.all()[0].id

            request.session['role_id'] = role_id
            request.session['menu_all_list'] = menus_list(username)
            request.session['perms_all_list'] = perms_list(role_id)


            user.status = "在线"
            user.save()

            next_url = request.GET.get("next")

            log_obj = log_db.UserLog(user_name=user.user_name, ready_name=user.ready_name,url_title="登录", status="成功")
            log_obj.save()
            if next_url:
                return redirect(next_url)
            else:
                return redirect('/')

        return render(request, 'login.html')


@login_check
def Logout(request):
    user_name = request.session['user_name']
    user_obj = auth_db.User.objects.get(user_name=user_name)
    user_obj.status = "离线"
    user_obj.save()
    logout(request)
    request.session.delete()
    return render(request, "login.html")


class Index(View):
    """首页"""
    @method_decorator(csrf_exempt)
    @method_decorator(login_check)
    def dispatch(self, request, *args, **kwargs):
        return super(Index, self).dispatch(request, *args, **kwargs)

    def get(self,request,*args,**kwargs):
        title = "运维管理-首页"

        # 时间
        now = datetime.datetime.now()
        A = now.strftime('%A')
        Y = now.strftime('%Y')
        m = now.strftime('%m')
        d = now.strftime('%d')
        H_M = now.strftime('%H:%M')

        # 主机数量

        role_id = request.session['role_id']

        role_obj = auth_db.Role.objects.get(id=role_id)


        user_num = auth_db.User.objects.all().count()
        return  render(request,'base.html',locals())



class RoleMG(View):
    """角色管理"""
    @method_decorator(csrf_exempt)
    @method_decorator(login_check)
    @method_decorator(perms_check)
    def dispatch(self, request, *args, **kwargs):
        return super(RoleMG,self).dispatch(request, *args, **kwargs)

    def get(self,request):
        title = "角色管理"

        role_obj = auth_db.Role.objects.all()

        return render(request,'rbac_role.html',locals())


    def post(self,request):
        '''添加角色'''
        role_title = request.POST.get("role_title")
        role_msg = request.POST.get("role_msg")
        try:
            role_obj = auth_db.Role(role_title=role_title,role_msg=role_msg)
            role_obj.save()
            data = "角色 %s 添加成功，请刷新查看" % role_title
        except Exception as e:
            data = "添加失败：\n%s" % e

        return HttpResponse(data)

    def put(self,request):
        """修改角色"""
        role_info = eval(request.body.decode())
        role_id = role_info.get("role_id")
        role_title = role_info.get("role_title")
        role_msg = role_info.get("role_msg")
        action = role_info.get("action",None)
        if action:
            """修改角色信息"""
            role_obj = auth_db.Role.objects.get(id=role_id)
            role_obj.role_title = role_title
            role_obj.role_msg = role_msg
            role_obj.save()
            data = "角色已修改，请刷新查看！"
            return HttpResponse(data)
        else:
            """获取修改信息"""
            role_info = auth_db.Role.objects.get(id=role_id)
            info_json = {'role_id': role_info.id, 'role_title': role_info.role_title, 'role_msg': role_info.role_msg}
            data = json.dumps(info_json)

        return HttpResponse(data)

    def delete(self,request):
        role_info = eval(request.body.decode())
        role_id = role_info.get("role_id")
        auth_db.Role.objects.get(id=role_id).delete()
        data = "角色已删除，请刷新查看"
        return HttpResponse(data)


@csrf_exempt
@login_check
@perms_check
def get_role_menu(request):
    """获取角色菜单"""
    role_id = request.POST.get("role_id")
    role_obj = auth_db.Role.objects.get(id=role_id)

    # 根据角色获取菜单列表
    menu_list = role_obj.menu.all()
    menu_num_list = []

    for i in menu_list:
        menu_num_list.append(i.menu_num)

    #获取全部菜单列表
    menu_obj = auth_db.Menus.objects.all()

    nodes = []

    for menu in menu_obj:
        if menu.menu_num in menu_num_list:
            nodes.append({"id": menu.menu_num, "pId": menu.pmenu_id, "name": menu.menu_title, 'open': True,
                          'checked': True})
        else:
            nodes.append({"id": menu.menu_num, "pId": menu.pmenu_id, "name": menu.menu_title, 'open': True})

    menu_data = json.dumps(nodes)

    return HttpResponse(menu_data)


@csrf_exempt
@login_check
@perms_check
def add_role_menu(request):
    """菜单授权"""
    menu_nums = request.POST.get("node_id_json")
    role_id = request.POST.get("role_id")

    role_obj = auth_db.Role.objects.get(id=role_id)

    menu_nums = json.loads(menu_nums)

    role_obj.menu.clear()

    for i in menu_nums:
        menu_obj = auth_db.Menus.objects.get(menu_num=i)
        role_obj.menu.add(menu_obj)

    data = "授权已更新，重新登录即生效！"
    return HttpResponse(data)



@csrf_exempt
@login_check
@perms_check
def get_role_perms(request):
    """获取角色权限"""
    role_id = request.POST.get("role_id")

    role_obj = auth_db.Role.objects.get(id=role_id)

    #获取用户拥有的权限
    perms_list = role_obj.perms.all()

    perms_num_list = []

    for i in perms_list:
        perms_num = "perms"+str(role_id)+"#"+str(i.id)
        perms_num_list.append(perms_num)
        perms_num_list.append(i.menus.id)
        perms_num_list.append(i.menus.pmenu_id)


    menu_obj = role_obj.menu.all()
    perms_info=[]
    for i in menu_obj:
        menu_id = i.id
        perms_obj = auth_db.Perms.objects.filter(menus_id=menu_id)
        for j in perms_obj:
            perms_info.append({"menu_id":j.menus.id,"menu_title":j.menus.menu_title,"pmenu_id":j.menus.pmenu_id})


    nodes = []
    menu_list = []
    pmenu_id_list = []
    for i in  perms_info:
        menu_info = {"menu_id":i['menu_id'],"menu_title":i['menu_title'],"pmenu_id":i['pmenu_id']}
        pmenu_id=i['pmenu_id']
        if menu_info not in menu_list:
            menu_list.append(menu_info)
        if pmenu_id not in pmenu_id_list:
            pmenu_id_list.append(pmenu_id)

    pmenu_list = []

    for i in pmenu_id_list:
        if i != '0':
            pmenu_obj = auth_db.Menus.objects.get(id=i)
            pmenu_list.append({"pmenu_id":i,"pmenu_title":pmenu_obj.menu_title})

    for i in pmenu_list:

        if i['pmenu_id'] in perms_num_list:
            nodes.append({"id": i['pmenu_id'], "pId": 0, "name": i['pmenu_title'], 'open': True,'checked': True})
        else:
            nodes.append({"id": i['pmenu_id'], "pId": 0, "name": i['pmenu_title'], 'open': True})

        for j in menu_list:

            if j["pmenu_id"] == i['pmenu_id']:

                perms_obj = auth_db.Perms.objects.filter(menus_id=j['menu_id'])

                menu_num = "menu"+str(j['menu_id'])

                if j['menu_id'] in perms_num_list:
                    nodes.append({"id": menu_num, "pId": i['pmenu_id'], "name": j['menu_title'], 'open': True,'checked': True})
                else:
                    nodes.append({"id": menu_num, "pId": i['pmenu_id'], "name": j['menu_title'], 'open': True})

                for perms in perms_obj:

                    perms_num = "perms"+str(role_id)+"#"+str(perms.id)

                    if perms_num in perms_num_list:
                        nodes.append({"id": perms_num, "pId": menu_num, "name": perms.perms_title, 'open': True,'checked': True})
                    else:
                        nodes.append({"id": perms_num, "pId": menu_num, "name": perms.perms_title, 'open': True})

    perms_data = json.dumps(nodes)

    return HttpResponse(perms_data)


@csrf_exempt
@login_check
@perms_check
def add_role_perms(request):
    """权限授权"""
    perms_nums = request.POST.get("node_id_json")

    role_id = request.POST.get("role_id")

    role_obj = auth_db.Role.objects.get(id=role_id)

    perms_nums = json.loads(perms_nums)

    role_obj.perms.clear()

    for i in perms_nums:
        if re.search(r"#",str(i)):
            perms_id = i.split("#")[-1]
            perms_obj = auth_db.Perms.objects.get(id=perms_id)
            role_obj.perms.add(perms_obj)

    data = "授权已更新，重新登录即生效！"
    return HttpResponse(data)


class UserMG(View):
    """用户管理"""
    @method_decorator(csrf_exempt)
    @method_decorator(login_check)
    @method_decorator(perms_check)
    def dispatch(self, request, *args, **kwargs):
        return super(UserMG,self).dispatch(request, *args, **kwargs)

    def get(self,request):
        title = '用户管理'
        roles = auth_db.Role.objects.all()
        role_list = []
        print('get method,用户管理查询界面')
        for role in roles:
            role_list.append({"role_title": role.role_title, "role_id": role.id})

        #当前所有在线会话
        session_obj = Session.objects.all()
        online_user = []
        for i in session_obj:
            online_user.append(i.get_decoded()['user_name'])


        role_id = request.session['role_id']
        role_obj = auth_db.Role.objects.get(id=role_id)

        if role_obj.role_title == "administrator":
            user_info = auth_db.User.objects.all()
        else:
            user_name = request.session['user_name']
            user_info = auth_db.User.objects.filter(user_name=user_name)

        user_list = []
        for user in user_info:
            role_obj = user.role.all()
            role_title = []
            for i in  role_obj:
                    role_title.append(i.role_title)

            if user.user_name in online_user:
                status = "在线"
            else:
                status = "离线"

            user_list.append({"ready_name": user.ready_name, "user_id": user.id, "user_name": user.user_name,
                              'phone': user.phone, 'email': user.email, 'role_title': ",".join(role_title),
                              'status': status})

            user.status = status
            user.save()

        return render(request, 'rbac_user.html', locals())


    def post(self,request):
        print('pos method,用户管理添加保存入库处理')
        """添加用户"""
        user_name = request.POST.get("user_name")
        ready_name = request.POST.get("ready_name")
        passwd = request.POST.get("passwd")
        role_id = request.POST.get("role")
        phone = request.POST.get("phone")
        email = request.POST.get("email")


        try:
            # django自带用户信息表
            role_obj = auth_db.Role.objects.get(id=role_id)
            user_obj = auth_db.User(user_name=user_name, email=email, passwd=passwd, ready_name=ready_name,
                                    phone=phone)
            user_obj.save()

            #添加用户角色（多对多关系）
            user_obj = auth_db.User.objects.get(user_name=user_name)
            user_obj.role.add(role_obj)
            user_obj.save()
            data = "用户 %s 添加成功,请刷新查看！" % user_name

        except Exception as e :
            data = "用户添加失败：\n %s " % e

        return HttpResponse(data)

    def put(self,request):
        """修改用户"""
        req_info = eval(request.body.decode())
        user_id = req_info.get("user_id")
        ready_name = req_info.get("ready_name")
        user_name = req_info.get("user_name")
        role_id = req_info.get("role_id")
        phone = req_info.get("phone")
        email = req_info.get("email")
        action = req_info.get("action")

        if action:
            print('put method,用户管理修改保存入库处理')
            user_obj = auth_db.User.objects.get(id=user_id)
            user_obj.ready_name = ready_name
            user_obj.user_name = user_name
            user_obj.email = email
            user_obj.phone = phone
            role_obj = auth_db.Role.objects.get(id=role_id)
            user_obj.role.clear()
            user_obj.role.add(role_obj)
            user_obj.save()
            data = "用户 %s 修改成功,请刷新查看！" % user_name
        else:
            print('put method,用户管理修改查询界面')
            """获取修改的用户信息"""
            user_obj = auth_db.User.objects.get(id=user_id)
            role_obj = user_obj.role.all()
            role_info = []
            for i in role_obj:
                role_info.append({"role_title":i.role_title,"role_id":i.id})

            role_info = json.dumps(role_info)
            data = json.dumps({"user_name":user_obj.user_name, "email":user_obj.email, "passwd":user_obj.passwd, "ready_name":user_obj.ready_name,
                                        "phone":user_obj.phone,"role_info":role_info,"user_id":user_obj.id})

        return HttpResponse(data)

    def delete(self,request):
        print('del method,用户管理删除逻辑')
        """删除用户"""
        req_info = eval(request.body.decode())
        user_id = req_info.get("user_id")
        auth_db.User.objects.get(id=user_id).delete()
        data = "用户已删除,请刷新查看！"
        return HttpResponse(data)




@csrf_exempt
@login_check
@perms_check
def change_passwd(request):
    """修改用户密码"""
    new_passwd = request.POST.get("new_passwd")

    user_id = request.POST.get("user_id")

    action = request.POST.get("action")

    if action:
        user_name = request.session['user_name']
        user_obj = auth_db.User.objects.get(user_name=user_name)
    else:
        user_obj = auth_db.User.objects.get(id=user_id)



    user_obj.passwd = new_passwd

    user_obj.save()

    data = "密码已修改,请重新登录！"

    return HttpResponse(data)

class MenuMG(View):
    """菜单管理"""
    @method_decorator(csrf_exempt)
    @method_decorator(login_check)
    @method_decorator(perms_check)
    def dispatch(self, request, *args, **kwargs):
        return super(MenuMG,self).dispatch(request, *args, **kwargs)


    def get(self,request):
        """查看菜单"""
        title = "菜单管理"

        menu_obj = auth_db.Menus.objects.all().order_by('menu_num')
        menu_list = []
        for menu in menu_obj:
            menu_dict = {}
            menu_dict['menu_title'] = menu.menu_title

            menu_dict['menu_id'] = menu.menu_num
            menu_dict['pmenu_id'] = menu.pmenu_id

            menu_list.append(menu_dict)

        nodes = []
        node_dict = {}

        for i in menu_obj:
            node_id = i.menu_num

            node_dict[node_id] = {"menu_id": i.id, "menu_title": i.menu_title, "menu_url": i.menu_url,
                                  "menu_type": i.menu_type, "menu_icon": i.menu_icon,
                                  "menu_num": i.menu_num, "pmenu_id": i.pmenu_id}

            nodes.append(node_id)
        menu_info = []
        nodes = sorted(nodes)
        for node_id in nodes:
            menu_info.append(node_dict[node_id])

        return render(request,'rbac_menu.html',locals())

    def post(self,request):
        """添加菜单"""
        menu_title = request.POST.get("menu_title")
        menu_url = request.POST.get("menu_url")
        menu_type = request.POST.get("menu_type")
        pmenu_id = request.POST.get("pmenu_id")
        menu_icon = request.POST.get("menu_icon")

        if menu_type=="一级菜单":
            pmenu_id = 0
        else:
            menu_icon=None

        menu_obj = auth_db.Menus(menu_title=menu_title,menu_url=menu_url,menu_type=menu_type,pmenu_id=pmenu_id,menu_icon=menu_icon)
        menu_obj.save()

        if menu_obj.menu_type == "一级菜单":
            menu_num = menu_obj.id
            print(menu_num)
        else:
            menu_num = int(str(pmenu_id) + '0' + str(menu_obj.id))

        menu_obj.menu_num = menu_num
        menu_obj.save()

        data = "菜单添加成功,请刷新查看！"
        return HttpResponse(data)

    def put(self,request):
        """修改菜单"""
        req_info = eval(request.body.decode())
        menu_id = req_info.get("menu_id")
        menu_title = req_info.get("menu_title")
        menu_url = req_info.get("menu_url")
        menu_type = req_info.get("menu_type")
        pmenu_id = req_info.get("pmenu_id")
        menu_icon = req_info.get("menu_icon")
        action = req_info.get("action")

        if action:
            if menu_type == u"一级菜单":
                pmenu_id = 0
            else:
                menu_icon = None
            menu_obj = auth_db.Menus.objects.get(id=menu_id)
            menu_obj.menu_title = menu_title
            menu_obj.menu_url = menu_url
            menu_obj.menu_type = menu_type
            menu_obj.pmenu_id = pmenu_id

            menu_obj.menu_icon = menu_icon

            menu_obj.save()

            if menu_type == u"一级菜单":
                menu_num = menu_id
            else:
                menu_num = int(str(pmenu_id) + '0' + str(menu_id))

            menu_obj.menu_num = menu_num
            menu_obj.save()

            data = "菜单已修改，请刷新查看！"

        else:
            menu_info = auth_db.Menus.objects.get(id=menu_id)

            info_json = {'menu_id': menu_info.id, 'menu_title': menu_info.menu_title,
                         'menu_url': menu_info.menu_url, 'menu_type': menu_info.menu_type,
                         'pmenu_id': menu_info.pmenu_id, 'menu_icon': menu_info.menu_icon}

            data = json.dumps(info_json)

        return HttpResponse(data)


    def delete(self,request):
        """删除菜单"""
        req_info = eval(request.body.decode())
        menu_id = req_info.get("menu_id")
        auth_db.Menus.objects.get(id=menu_id).delete()
        data = "菜单已删除,请刷新查看！"
        return HttpResponse(data)


class PermsMG(View):

    """权限管理"""
    @method_decorator(csrf_exempt)
    @method_decorator(login_check)
    @method_decorator(perms_check)
    def dispatch(self, request, *args, **kwargs):
        return super(PermsMG,self).dispatch(request, *args, **kwargs)


    def get(self,request):
        """查看权限"""
        title = "权限管理"
        menu_list = auth_db.Menus.objects.all()

        perms_obj = auth_db.Perms.objects.all()

        return  render(request,'rbac_perms.html',locals())

    def post(self,request):
        """添加权限"""
        perms_req = request.POST.get("perms_req")
        perms_title = request.POST.get("perms_title")
        menus_id = request.POST.get("menus_id")
        perms_url = request.POST.get("perms_url")
        if perms_req != "other":
            perms_url=None
        perms_obj = auth_db.Perms(perms_title=perms_title, perms_req=perms_req, menus_id=menus_id,perms_url=perms_url)
        perms_obj.save()
        data = "权限添加成功，请刷新查看！"
        return  HttpResponse(data)

    def put(self,request):
        """修改权限"""
        req_info = eval(request.body.decode())
        perms_id = req_info.get("perms_id")
        perms_req = req_info.get("perms_req")
        perms_title = req_info.get("perms_title")
        perms_url = req_info.get("perms_url")
        menus_id = req_info.get("menus_id")
        action = req_info.get("action")
        if action:
            if perms_req != "other":
                perms_url = None
            perms_obj = auth_db.Perms.objects.get(id=perms_id)
            perms_obj.perms_req = perms_req
            perms_obj.perms_title = perms_title
            perms_obj.perms_url = perms_url
            perms_obj.menus_id = menus_id
            perms_obj.save()
            data = "权限已修改,请刷新查看！"
        else:
            edit_perms_obj = auth_db.Perms.objects.get(id=perms_id)

            data= json.dumps({"perms_id":edit_perms_obj.id,"perms_title":edit_perms_obj.perms_title,"perms_req":edit_perms_obj.perms_req,
                              "menus_id":edit_perms_obj.menus.id,"perms_url":edit_perms_obj.perms_url})

        return HttpResponse(data)

    def delete(self,request):
        """删除权限"""
        req_info = eval(request.body.decode())
        perms_id = req_info.get("perms_id")
        auth_db.Perms.objects.get(id=perms_id).delete()
        data = "权限已删除,请刷新查看！"
        return HttpResponse(data)