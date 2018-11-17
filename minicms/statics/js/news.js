
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
            window.location.href = data.url;
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
                        var info = eval('(' + data + ')');
                        $("#edit-name").val(info.name);
                        $("#edit-mobile").val(info.mobile);
                        $("#edit-email").val(info.email);
                        $("#sub-edit-author").attr('author_id', info.author_id);
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
                    window.location.href = data.url;

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
                if(data=="perms_false"){
                    $("#msg-alert").empty();
                    $("#msg-alert").append("权限不足，请联系管理员");
                    $("#alert").show();
            }else {
                    $("#msg-alert").empty();
                    $("#msg-alert").append(data);
                    $("#alert").show();
                }
             }
        });
    }
});

