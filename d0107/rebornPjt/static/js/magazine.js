
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



