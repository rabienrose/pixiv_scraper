cur_img=null
oss_display_root="https://pixivchamo.oss-cn-beijing.aliyuncs.com/display_imgs/"
moe_count=-1
dislike_count=-1
unrate_count=-1
total_check_count=0
right_count=0
cur_score=0
temp_moe_count=0
temp_moe_ok_count=0
temp_choose_moe_count=0
cur_type=0
moe_uncheck_count=0
dislike_uncheck_count=0
function update_ok_rate(predict_score, choose){
    total_check_count=total_check_count+1
    if (predict_score>0){
        temp_moe_count=temp_moe_count+1
    }
    if (predict_score>0 && choose==1){
        temp_moe_ok_count=temp_moe_ok_count+1
    }
    if (choose==1){
        temp_choose_moe_count=temp_choose_moe_count+1
    }
    if (predict_score>0 && choose==1 || predict_score<=0 && choose==0){
        right_count=right_count+1
    }
    rate=(right_count/total_check_count).toFixed(2)
    recall=(temp_moe_ok_count/temp_moe_count).toFixed(2)
    precision=(temp_moe_ok_count/temp_choose_moe_count).toFixed(2)
    document.getElementById('ok_rate').innerHTML="Percent: "+rate
//    document.getElementById('precision').innerHTML="Prec: "+precision
}

function get_unrate(){
    sel_dom = document.getElementById('type_select')
    str=sel_dom.innerHTML
    val=0
    if (str=="Unrate"){
        val=0
    }
    if (str=="Moe"){
        val=1
    }
    if (str=="Dislike"){
        val=-1
    }
    
    $.ajax({
        type: 'GET',
        url: '../../show_unrate',
        dataType: 'json',
        data: {"type": val},
        success: function(data) {
            img_dom = document.getElementById('main_pic')
            if ("img_file" in data){
                cur_img=data["img_file"]
                img_dom.src=oss_display_root+cur_img
                document.getElementById('score').innerHTML="Score: "+data["score"]
                cur_score=data["score"]
                cur_type=data["type"]
                update_count()
            }
        },
        async: false
    });
}

function change_type(){
    sel_dom = document.getElementById('type_select')
    str=sel_dom.innerHTML
    if (str=="Unrate"){
        sel_dom.innerHTML="Moe"
    }
    if (str=="Moe"){
        sel_dom.innerHTML="Dislike"
    }
    if (str=="Dislike"){
        sel_dom.innerHTML="Unrate"
    }
}
function set_moe_val(val){
    if (cur_img==null){
        return
    }
    $.ajax({
        type: 'GET',
        url: '../../set_moe',
        dataType: 'json',
        data: {
            "img_name": cur_img,
            "val":val
        },
        success: function(data) {
        },
        async: false
    });
}
function set_check_val(val){
    if (cur_img==null){
        return
    }
    $.ajax({
        type: 'GET',
        url: '../../set_check',
        dataType: 'json',
        data: {
           "img_name": cur_img,
           "val":val
        },
        success: function(data) {
        },
        async: false
    });
}
function like(){
    update_ok_rate(cur_score, 1)
    if (cur_type==-1){
        dislike_count=dislike_count-1
        moe_count=moe_count+1
        dislike_uncheck_count=dislike_uncheck_count-1
        set_moe_val(1)
        set_check_val(1)
    }else if(cur_type==0){
        unrate_count=unrate_count-1
        moe_count=moe_count+1
        moe_uncheck_count=moe_uncheck_count+1
        set_moe_val(1)
        set_check_val(0)
    }else if(cur_type==1){
        moe_uncheck_count=moe_uncheck_count-1
        set_check_val(1)
    }
    get_unrate()
}
function next(){
    get_unrate()
}
function reset(){
    if (cur_type==-1){
        dislike_count=dislike_count-1
        unrate_count=unrate_count+1
        dislike_uncheck_count=dislike_uncheck_count-1
        set_moe_val(0)
        set_check_val(0)
    }else if(cur_type==0){
        
    }else if(cur_type==1){
        moe_count=moe_count-1
        unrate_count=unrate_count+1
        moe_uncheck_count=moe_uncheck_count-1
        set_moe_val(0)
        set_check_val(0)
    }
    get_unrate()
}
function dislike(){
    update_ok_rate(cur_score, 0)
    if (cur_type==1){
        dislike_count=dislike_count+1
        moe_count=moe_count-1
        moe_uncheck_count=moe_uncheck_count-1
        set_moe_val(-1)
        set_check_val(1)
    }else if(cur_type==0){
        dislike_count=dislike_count+1
        unrate_count=unrate_count-1
        dislike_uncheck_count=dislike_uncheck_count+1
        set_moe_val(-1)
        set_check_val(0)
    }else if(cur_type==-1){
        dislike_uncheck_count=dislike_uncheck_count-1
        set_check_val(1)
    }
    get_unrate()
}

function update_count(){
    document.getElementById('moe_count').innerHTML="Moe: "+moe_count
    document.getElementById('dislike_count').innerHTML="Dislike: "+dislike_count
    if (cur_type==1){
        document.getElementById('unrate_count').innerHTML="Uncheck: "+moe_uncheck_count
    }else if (cur_type==-1){
        document.getElementById('unrate_count').innerHTML="Uncheck: "+dislike_uncheck_count
    }else if (cur_type==0){
        document.getElementById('unrate_count').innerHTML="Unrate: "+unrate_count
    }
}

function show_count(){
    $.ajax({
        type: 'GET',
        url: '../../get_count',
        dataType: 'json',
        success: function(data) {
            console.log(data)
            moe_count=data["moe"]
            dislike_count=data["dislike"]
            unrate_count=data["unrate"]
            moe_uncheck_count=data["moe_uncheck"]
            dislike_uncheck_count=data["dislike_uncheck"]
            update_count()
        },
        async: false
    });
    
}

$(document).ready(function(){
    show_count()
    get_unrate()
    sel_dom.innerHTML="Unrate"
})

