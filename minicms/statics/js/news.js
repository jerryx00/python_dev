
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


////////////////////////书籍管理////////////////////////////
//添加保存书籍
$("#add-book").click(function(){

    var name = $("#add-name").val();
    var title = $("#add-title").val();
    var pub = $("#add-pub").val();
    $.post("/news/book/",{'name':name,'title':title,'pub':pub},function(data){
        if(data.code != "0"){
            $("#msg-alert").empty();
            $("#msg-alert").append("处理错误，请联系管理员");
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
                        var info = eval('(' + data + ')');
                        $("#edit-name").val(info.name);
                        $("#edit-title").val(info.title);
                        $("#edit-pub").val(info.pub);
                        $("#sub-edit-book").attr('book_id', info.book_id);
                        $("#edit-bookModal").modal('show');
                    }


    });
});

//修改-保存书籍信息
$("#sub-edit-book").click(function(){
    var book_id = $(this).attr('book_id');
    var name = $("#edit-name").val();
    var title = $("#edit-title").val();
    var pub = $("#edit-pub").val();

     $.ajax({
            url: "/news/book/",
            type: "PUT",
            data: JSON.stringify({'action':'edit','name':name, 'title':title,'pub':pub,'book_id':book_id}),
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
                if(data.code !="0"){
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



