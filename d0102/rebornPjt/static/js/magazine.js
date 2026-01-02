
function selectBtn(str){
    if (str == ''){
        location.href='/magazine/mlist/';
    }else{
        location.href='/magazine/mlist/?category='+str;
    }
}

function searchBtn(){
    searchFrm.submit();
}

//$(document).ready(function(){});
$(function(){
    
    $('#mz-like').click(function(){

        $.ajax({
            url:'/magazine/mlike/',
            type:'post',
            headers:{'X-CSRFToken':'{{csrf_token}}'},
            data:{'mno':'{{mz.mno}}'},
            dataType:'json',
            success:function(data){
                console.log('result : ',data.result);

                if(data.like_chk == '1'){
                    dataHtml = `<i class="fa-solid fa-heart"></i> (${data.like_count})`;
                }else{
                    dataHtml = `<i class="fa-regular fa-heart"></i> (${data.like_count})`;
                }

                $('#mz-like').html(dataHtml);

            },
            error:function(){
                alert('실패');
            }
        });//ajax

    });//mz-like

}); //jquery