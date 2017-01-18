var msecs = 400; //改变时间得到不同的闪烁间隔；
var counter = 0;
var onload = function() {
    setTimeout("blink()", msecs);
};

function blink(){
    var bg = document.getElementsByClassName('high-bg');
    for(var id=0;id<bg.length ;id++){
        if(counter%2==1){
            bg[id].style.backgroundColor="#e6c5c6";
        }else {
            bg[id].style.backgroundColor="#c9ca77";
        }
    }
    counter +=1;
    setTimeout("blink()",msecs);
}



$(function(){

    $('.js_switcher').on('change', function(){
        var isChecked = $(this).is(':checked');
        //$.weui.alert(isChecked + '');
        if(isChecked){
            document.getElementById('zabbix_img').style.display = "";
        }else{
            document.getElementById('zabbix_img').style.display = "none";
        }
        //console.log(isChecked);
    });
});


$(function () {
    $('.weui_btn_area').on('click', '#ackevent', function (e) {
        var confirm_msg = $('#textarea').val()||'微信确认';
        $.weui.dialog({
            title: '确认报警内容',
            content: confirm_msg ,
            buttons: [{
                label: '过会儿确认',
                type: 'default',
                onClick: function (){
                    console.log('知道了......');
                }
            }, {
                label: '现在确认',
                type: 'primary',
                onClick: function (){
                    var urls = window.location.href;
                    eventid = urls.split('/')[5];
                    var zurl = "/wx_api/acknowlege.html?eventid="+eventid+"&msg="+confirm_msg;
                    var xmlhttp = new XMLHttpRequest();
                    xmlhttp.open('GET',zurl,true);
                    xmlhttp.send();
                    setTimeout('myrefresh()',1000);
                }
            }]
        });

    });


});





function myrefresh()
{
window.location.reload();
}

$(function(){
var imglist =document.getElementsByTagName("img");
//安卓4.0+等高版本不支持window.screen.width，安卓2.3.3系统支持
var _width;
doDraw();

window.onresize = function(){
    //捕捉屏幕窗口变化，始终保证图片根据屏幕宽度合理显示
    doDraw();
}

function doDraw(){
    _width = window.innerWidth;
    for( var i = 0, len = imglist.length; i < len; i++){
        DrawImage(imglist[i],_width);
    }
}

function DrawImage(ImgD,_width){
    var image=new Image();
    image.src=ImgD.src;
    image.onload = function(){
        //限制，只对宽高都大于30的图片做显示处理
        if(image.width>30 && image.height>30){
            if(image.width>_width){
                ImgD.width=_width;
                ImgD.height=(image.height*_width)/image.width;
            }else{
                ImgD.width=image.width;
                ImgD.height=image.height;
            }

        }
    }

}

})