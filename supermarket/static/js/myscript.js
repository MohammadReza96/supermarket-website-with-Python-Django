// ok  ------------------------------------ for checking user_name is valid or not 
$(document).ready(function(){
    $('#user_name_check').blur(function(event){
        let user_name = $('#user_name_check').val()
        $.ajax({
            type:"GET",
            url:"/accounts/username_form_validation/",
            data:{
                user_name:user_name
            },
            success:function(res){
                if (user_name == "") {
                    $("#register_form_message").text('').css({"border":"0px solid white"})
                }else if(res == 'ok'){
                    $("#register_form_message").text('نام کاربری معتبر است').css({"color":"green","border":"1px solid green"})
                }
                else {
                    $("#register_form_message").text('این نام کاربری قبلا استفاده شده است').css({"color":"red","border":"1px solid red"})
                }
            }
        })
    })
})
// ok  ------------------------------------ for showing cheapest products base on special group_name
function change_group_cheap(group_id){
    let gp_id = group_id;
    if (Number(gp_id)=== 0 ){
        gp_id=''
    }
    $.ajax({
        type:"GET",
        url:"/products/cheapest_product/",
        data:{
            group_id:gp_id,
        },
        success : function(res){
            $('#cheap_pro').html(res)
        }
    })
    $('.block-header__group').removeClass('block-header__group--active')
    $('#bn_'+group_id).addClass('block-header__group--active')
}
// ok  ------------------------------------ for showing newest products base on special group_name
function change_group_new(group_id){
    let gp_id = group_id;
    if (Number(gp_id)=== 0 ){
        gp_id=''
    }
    $.ajax({
        type:"GET",
        url:"/products/newest_product/",
        data:{
            group_id:gp_id,
        },
        success : function(res){
            $('#new_pro').html(res)
        }
    })
    $('.block-header__group').removeClass('block-header__group--active')
    $('#bn_'+group_id).addClass('block-header__group--active')
}
// ok  ------------------------------------ for showing topsell products base on special group_name
function change_group_topsell(group_id){
    let gp_id = group_id;
    if (Number(gp_id)=== 0 ){
        gp_id=''
    }
    $.ajax({
        type:"GET",
        url:"/products/topsell_product/",
        data:{
            group_id:gp_id,
        },
        success : function(res){
            $('#top_pro').html(res)
        }
    })
    $('.block-header__group').removeClass('block-header__group--active')
    $('#bn_'+group_id).addClass('block-header__group--active')
}
// ok  ------------------------------------ update favorite list count
function favorite_list_status(){
    $.ajax({
        type:'GET',
        url: "/favorite/favorite_list_status/",
        success: function(res){
            $('#indicator__value').text(res);
        }

    })
}
//----------------------------------------- for running the function above all time
favorite_list_status()
// ok  ------------------------------------ add product to favorite list
function add_to_favorite(product_id){
    $.ajax({
        type:"GET",
        url:"/favorite/add_to_favorite/",
        data:{
            product_id:product_id,
        },
        success : function(res){
            $("#unlike_"+ product_id).css("color","red")
            favorite_list_status()
            alert(res)
        }
    })
}
// ok  ------------------------------------ delete product from favorite list
function delete_from_favorite_list(product_id){
    $.ajax({
        type:"GET",
        url:"/favorite/delete_from_favorite_list/",
        data:{
            product_id:product_id
        },
        success:function(res){
            $('#favorite_product_list').html(res)
            favorite_list_status()
            // alert('این محصول از لیست مورد علاقه شما حذف شد')
        }
    })
}
// ok  ------------------------------------ changing warehouse_status color
$(document).ready(function(){
    function change_color_warehouse_status_red(){
        $(".warehouse_status").css("color","red")
    }
    function change_color_warehouse_status_white(){
        $(".warehouse_status").css("color","#BBBBBB")
    }
    setInterval(change_color_warehouse_status_red,700)
    setInterval(change_color_warehouse_status_white,2200)
});
// ok ------------------------------------- for showing the reply box for 1 comment
function showCreateCommentForm(comment_id,product_slug){
    $.ajax({
        type:"GET",
        url:"/comments/create_comment/" + product_slug,
        data:{
            comment_id:comment_id
        },
        success:function(res){
            $('#btn_'+ comment_id).hide();  // for hide a tag in html
            $('#comment_form_'+ comment_id).show();
            $('#btn_unshow_'+ comment_id).show()
            $('#btn_unshow_'+ comment_id).text('انصراف').css({'background-color':'red','color':'white'});
            $("#comment_form_"+comment_id).html(res)
        }
    });
}
// ok ------------------------------------- for hiding the reply box for 1 comment
function UnshowCreateCommentForm(comment_id){
    $('#btn_'+ comment_id).show();
    $('#btn_unshow_'+ comment_id).hide();
    $('#comment_form_'+ comment_id).hide();
}
// ok ------------------------------------- for setting a score for a product
function addScore(score,product_id){
    var pid =product_id
    var starRating=document.querySelectorAll('.fa-star')
    starRating.forEach(element =>{
        element.classList.remove('checked')
    })
    for (let i =1 ; i <= score ; i++){
        const element = document.getElementById('star_' + i);
        element.classList.add('checked')
    }
    //---------- this function update the average score immediately
    function average_Score_status(product_id){
        $.ajax({
            type:'GET',
            url: "/scoring/average_score_update/",
            data:{
                product_id:product_id
            },
            success: function(res){
                $('#average_score').text(res);
            }
        })
    }   

    $.ajax({
        type: "GET",
        url: "/scoring/user_score/",
        data:{
            product_id:product_id,
            score:score
        },
        success : function(res){
            average_Score_status(product_id)
        }
    });

    starRating.forEach(element=>{
        element.classList.add('disable')
    })
}
// ok ------------------------------------- for updating compare product list status
function status_of_compare_product(){
    $.ajax({
        type:'GET',
        url: "/compare/status_compare_product/",
        success: function(res){
            $('#indicator__value_2').text(res);
        }
    })
}
status_of_compare_product();
// ok ------------------------------------- for adding to compare product list
function addToCompareList(product_id){
    var product_id=product_id;
    $.ajax({
        type:"GET",
        url:"/compare/add_to_product_compare/",
        data:{
            product_id:product_id
        },
        success: function(res){
            alert(res)
            status_of_compare_product()
        }
    });
}
// ok ------------------------------------- for deleting from compare product list
function deleteFromCompareList(product_id){
    var product_id=product_id;
    $.ajax({
        type:"GET",
        url:"/compare/delete_from_product_compare/",
        data:{
            product_id:product_id
        },
        success: function(res){
            $("#compare_list").html(res);
            status_of_compare_product()
        }
    });
}
// ok ------------------------------------- for updating shopcard list status
function update_status_of_shopcard(){
    $.ajax({
        type:'GET',
        url:"/orders/status_shop_card/",
        success:function(res){
            $('#indicator__value_3').text(res)
        }
    })
}
update_status_of_shopcard()
// ok ------------------------------------- for adding a product in shopcard list
function add_to_shopcard(product_id,number){
    if (number===0){
        number=$('#product-quantity').val()
    }
    $.ajax({
        type:'GET',
        url: "/orders/add_to_shop_card/",
        data:{
            product_id:product_id,
            number:number
        },
        success: function(res){
            alert('کالای شما با موفقیت در سبد شما اضافه شد')
            $('#indicator__value_3').text(res);
            status_of_shopcard();
        }
    })
}
// ok ------------------------------------- for deleting  a product from shopcard list
function delete_from_shopcard(product_id){
    $.ajax({
        type:'GET',
        url: "/orders/delete_form_shop_card/",
        data:{
            product_id:product_id,
        },
        success: function(res){
            $('#shop_card_list').html(res);
            status_of_shopcard();
        }

    })
}
// ok ------------------------------------- for adding extra number of a  product in shopcard list
function add_more_product(product_id,number){
    if (number===0){
        number=$('#product-quantity-'+product_id).val()
    }
    $.ajax({
        type:'GET',
        url: "/orders/add_more_product/",
        data:{
            product_id:product_id,
            number:number
        },
        success: function(res){
            $('#shop_card_list').html(res);
            status_of_shopcard();
        }

    });
}
// ok ------------------------------------- for adding filter to price 
function showVal(x){
    x=x.toString().replace(/\B(?=(\d{3})+(?!\d))/g,',');
    document.getElementById('cur_price').innerText=x;
}
// ok ------------------------------------ for removing the querystring from url   ** I pick this code from web :) **
function removeURLParameter(url, parameter) {
    var urlparts = url.split('?');   
    if (urlparts.length >= 2) {

        var prefix = encodeURIComponent(parameter) + '=';
        var pars = urlparts[1].split(/[&;]/g);

        for (var i = pars.length; i-- > 0;) {    
            if (pars[i].lastIndexOf(prefix, 0) !== -1) {  
                pars.splice(i, 1);
            }
        }

        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
    }
    return url;
}
// ok ------------------------------------- for setting the sort type of products
function select_sort(){
    var select_sort_value=$("#select_sort").val();

    var data="?"
    var url = removeURLParameter(window.location.href,"sort_type");

    if ( url.includes(data)) {
        window.location = url + "&sort_type=" + select_sort_value;
    } else {
        window.location = url + "?sort_type=" + select_sort_value;
    }

}
// ok ------------------------------------- for setiing how many product to show in a page
function select_number_show_1(){
    var select_number_show=$("#select_number_show").val();
    
    var data="?"
    var url = removeURLParameter(window.location.href,"select_number_show");

    if ( url.includes(data)) {
        window.location = url + "&select_number_show=" + select_number_show;

    } else {
        window.location = url + "?select_number_show=" + select_number_show;
    }

}