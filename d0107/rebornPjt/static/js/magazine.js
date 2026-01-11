

function selectBtn(str){

    if (str == ''){
        location.href='/magazine/mlist/';
    }else{
        location.href='/magazine/mlist/?category='+str;
    }
}

function msearchBtn(){
    // alert('msearchBtn');

    let category = document.getElementById('mmcategory').value;
    let sort = document.getElementById('mmsort').value;
    let search = document.getElementById('mmsearch').value;

    if (sort == ''){
        location.href='/magazine/mmnge/?category='+category+'&search='+search;
    }else{
        location.href='/magazine/mmnge/?category='+category+'&search='+search+'&sort='+sort;
    }
   
}

function searchBtn(){
    searchFrm.submit();
}

//$(document).ready(function(){});

