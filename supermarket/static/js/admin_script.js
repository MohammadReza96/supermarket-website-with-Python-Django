$(document).ready(function(){
    var listofelement= $('select[id^="id_product_features-"][id$="-product_feature_feature"]')
    $(listofelement).on('change',function(){
        f_id=$(this).val();
        dd1=$(this).attr('id');
        dd2=dd1.replace("-product_feature_feature","-filter_value");

        $.ajax({
            type:"GET",
            url:"/products/ajax_admin/?feature_id="+f_id,
            success:function(res){
                cols=document.getElementById(dd2);
                cols.options.length=0;
                for (var k in res){
                    cols.options.add(new Option(k,res[k]))
                }
            }
        });

    });
});