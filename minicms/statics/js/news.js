
////////////////////////作者管理////////////////////////////
//添加保存作者
$("#add-author").click(function(){
    var name = $("#add-name").val();
    var mobile = $("#add-mobile").val();
    var email = $("#add-email").val();

    $.post("/news/author/",{'name':name,'mobile':mobile,'email':email},function(data){
        if(data=="perms_false1"){
            $("#msg-alert").empty();
            $("#msg-alert").append("权限不足，请联系管理员");
            $("#alert").show();
        }else {
            $("#msg-alert").empty();
            $("#msg-alert").append(data.msg);
            $("#authorModal").modal("hide");
            $("#alert").show();
//            window.location.href = data.url;
        }
    })

});
//修改--查询获取作者修改信息,并赋值给对应的对象（文本框等）
$('td a[name="edit-author"]').click(function(){
    var author_id = $(this).attr("author_id");
        $.ajax({
            url: "/news/author/",
            type: "PUT",
            data: JSON.stringify({'author_id':author_id}),
            success: function(data) {
                        $("#edit-name").val(data.name);
                        $("#edit-mobile").val(data.mobile);
                        $("#edit-email").val(data.email);
                        $("#sub-edit-author").attr('author_id', data.author_id);
                        $("#edit-authorModal").modal('show');
                    }


    });
});

//修改-保存作者信息
$("#sub-edit-author").click(function(){
    var author_id = $(this).attr('author_id');
    var name = $("#edit-name").val();
    var mobile = $("#edit-mobile").val();
    var email = $("#edit-email").val();

     $.ajax({
            url: "/news/author/",
            type: "PUT",
            data: JSON.stringify({'action':'edit','name':name, 'mobile':mobile,'email':email,'author_id':author_id}),
            success: function(data) {
                    $("#msg-alert").empty();
                    $("#msg-alert").append(data.msg);
                    $("#edit-authorModal").modal("hide");
                    $("#alert").show();
//                    window.location.href = data.url;

        }
    });
});
//删除作者
$("td a[name='del-author']").click(function(){
   var author_id = $(this).attr('author_id');
   var statu = confirm("是否确认删除！");
   if (statu==true)
    {
         $.ajax({
            url: "/news/author/",
            type: "DELETE",
            data: JSON.stringify({'author_id':author_id}),
            success: function(data) {
                console.log(data);
                if(data.code != 0){
                    $("#msg-alert").empty();
                    $("#msg-alert").append("权限不足，请联系管理员");
                    $("#alert").show();
            }else {
                    $("#msg-alert").empty();
                    $("#msg-alert").append(data.msg);
                    $("#alert").show();
                }
             }
        });
    }
});


////////////////////////书籍管理////////////////////////////
//添加保存书籍
$("#add-book").click(function(){

    var name = $("#add-name").val();
    var title = $("#add-title").val();
    var pub_id = $("#add-pub").val();
    $.post("/news/book/",{'name':name,'title':title,'pub_id':pub_id},function(data){
        console.log(data);
        if(data.code != 0){
            $("#msg-alert").empty();
            $("#msg-alert").append("处理错误，请联系管理员! "+data.code );
            $("#alert").show();
        }else {
            $("#msg-alert").empty();
            $("#msg-alert").append(data.msg);
            $("#bookModal").modal("hide");
            $("#alert").show();
//            window.location.href = data.url;
        }
    })

});


//修改--查询获取书籍修改信息,并赋值给对应的对象（文本框等）
$('td a[name="edit-book"]').click(function(){
    var book_id = $(this).attr("book_id");
        $.ajax({
            url: "/news/book/",
            type: "PUT",
            data: JSON.stringify({'book_id':book_id}),
            success: function(data) {
                        $("#edit-name").val(data.name);
                        $("#edit-title").val(data.title);
                        var pub_info = data.pub_info;
                        for (i = 0; i < pub_info.length; i++) {
                            $("#edit-pub").val(pub_info[0].pub_id);
                        }
                        $("#sub-edit-book").attr('book_id', data.book_id);
                        $("#edit-bookModal").modal('show');
                    }


    });
});

//修改-保存书籍信息
$("#sub-edit-book").click(function(){
    var book_id = $(this).attr('book_id');
    var name = $("#edit-name").val();
    var title = $("#edit-title").val();
    var pub_id = $("#edit-pub").val();

     $.ajax({
            url: "/news/book/",
            type: "PUT",
            data: JSON.stringify({'action':'edit','name':name, 'title':title,'pub_id':pub_id,'book_id':book_id}),
            success: function(data) {
                    $("#msg-alert").empty();
                    $("#msg-alert").append(data.msg);
                    $("#edit-bookModal").modal("hide");
                    $("#alert").show();
//                    window.location.href = data.url;

        }
    });
});
//删除书籍
$("td a[name='del-book']").click(function(){
   var book_id = $(this).attr('book_id');
   var statu = confirm("是否确认删除！");
   if (statu==true)
    {
         $.ajax({
            url: "/news/book/",
            type: "DELETE",
            data: JSON.stringify({'book_id':book_id}),
            success: function(data) {
                console.log(data);
                if(data.code !=0){
                    $("#msg-alert").empty();
                    $("#msg-alert").append("权限不足，请联系管理员");
                    $("#alert").show();
                 }else {
                    $("#msg-alert").empty();
                    $("#msg-alert").append(data.msg);
                    $("#alert").show();
                }
             }
        });
    }
});



////////////////////////部门管理////////////////////////////
//添加保存部门
$("#add-department").click(function(){

    var name = $("#add-name").val();
    var code = $("#add-code").val();
    $.post("/news/department/",{'name':name,'code':code},function(data){
        console.log(data);
        if(data.code != 0){
            $("#msg-alert").empty();
            $("#msg-alert").append("处理错误，请联系管理员! "+data.code );
            $("#alert").show();
        }else {
            $("#msg-alert").empty();
            $("#msg-alert").append(data.msg);
            $("#departmentModal").modal("hide");
            $("#alert").show();
//            window.location.href = data.url;
        }
    })

});


//修改--查询获取部门修改信息,并赋值给对应的对象（文本框等）
$('td a[name="edit-department"]').click(function(){
    var department_id = $(this).attr("department_id");
        $.ajax({
            url: "/news/department/",
            type: "PUT",
            data: JSON.stringify({'department_id':department_id}),
            success: function(data) {
                        $("#edit-name").val(data.name);
                        $("#edit-code").val(data.code);

                        $("#sub-edit-department").attr('department_id', data.department_id);
                        $("#edit-departmentModal").modal('show');
                    }


    });
});

//修改-保存部门信息
$("#sub-edit-department").click(function(){
    var department_id = $(this).attr('department_id');
    var name = $("#edit-name").val();
    var code = $("#edit-code").val();

     $.ajax({
            url: "/news/department/",
            type: "PUT",
            data: JSON.stringify({'action':'edit','name':name, 'code':code,'department_id':department_id}),
            success: function(data) {
                    $("#msg-alert").empty();
                    $("#msg-alert").append(data.msg);
                    $("#edit-departmentModal").modal("hide");
                    $("#alert").show();
//                    window.location.href = data.url;

        }
    });
});
//删除部门
$("td a[name='del-department']").click(function(){
   var department_id = $(this).attr('department_id');
   var statu = confirm("是否确认删除！");
   if (statu==true)
    {
         $.ajax({
            url: "/news/department/",
            type: "DELETE",
            data: JSON.stringify({'department_id':department_id}),
            success: function(data) {
                console.log(data);
                if(data.code !=0){
                    $("#msg-alert").empty();
                    $("#msg-alert").append("权限不足，请联系管理员");
                    $("#alert").show();
                 }else {
                    $("#msg-alert").empty();
                    $("#msg-alert").append(data.msg);
                    $("#alert").show();
                }
             }
        });
    }
});


////////////////////////人员管理////////////////////////////
//添加保存人员
$("#add-person").click(function(){

    var name = $("#add-name").val();
    var hometown_id = $("#add-hometown").val();
    var living_id = $("#add-living").val();
    var visitation_id = $("#add-visitation").val();
    var department_id = $("#add-department").val();

    $.post("/news/person/",{
        'name':name,
        'hometown_id':hometown_id,
        'living_id':living_id,
        'visitation_id':visitation_id,
        'department_id':department_id
    },function(data){
        console.log(data);
        if(data.code != 0){
            $("#msg-alert").empty();
            $("#msg-alert").append("处理错误，请联系管理员! "+data.code );
            $("#alert").show();
        }else {
            $("#msg-alert").empty();
            $("#msg-alert").append(data.msg);
            $("#personModal").modal("hide");
            $("#alert").show();
//            window.location.href = data.url;
        }
    })

});


//修改--查询获取人员修改信息,并赋值给对应的对象（文本框等）
$('td a[name="edit-person"]').click(function(){
    var person_id = $(this).attr("person_id");
        $.ajax({
            url: "/news/person/",
            type: "PUT",
            data: JSON.stringify({'person_id':person_id}),
            success: function(data) {
                        $("#edit-name").val(data.name);
//                         for (i = 0; i < pub_info.length; i++) {
//                            $("#edit-pub").val(pub_info[0].pub_id);
//                        }
                        selected_info = data.selected_info;
                        $("#edit-hometown").val(selected_info[0].id);
                        $("#edit-visitation").val(selected_info[1].id);
                        $("#edit-living").val(selected_info[2].id);
                        $("#edit-department").val(selected_info[3].id);

                        $("#sub-edit-person").attr('person_id', data.person_id);
                        $("#edit-personModal").modal('show');
                    }


    });
});

//修改-保存人员信息
$("#sub-edit-person").click(function(){
    var person_id = $(this).attr('person_id');
    var name = $("#edit-name").val();
    var code = $("#edit-code").val();

     $.ajax({
            url: "/news/person/",
            type: "PUT",
            data: JSON.stringify({'action':'edit','name':name, 'code':code,'person_id':person_id}),
            success: function(data) {
                    $("#msg-alert").empty();
                    $("#msg-alert").append(data.msg);
                    $("#edit-personModal").modal("hide");
                    $("#alert").show();
//                    window.location.href = data.url;

        }
    });
});
//删除人员
$("td a[name='del-person']").click(function(){
   var person_id = $(this).attr('person_id');
   var statu = confirm("是否确认删除！");
   if (statu==true)
    {
         $.ajax({
            url: "/news/person/",
            type: "DELETE",
            data: JSON.stringify({'person_id':person_id}),
            success: function(data) {
                console.log(data);
                if(data.code !=0){
                    $("#msg-alert").empty();
                    $("#msg-alert").append("权限不足，请联系管理员");
                    $("#alert").show();
                 }else {
                    $("#msg-alert").empty();
                    $("#msg-alert").append(data.msg);
                    $("#alert").show();
                }
             }
        });
    }
});



