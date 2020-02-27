// 弹框消息
function notify(msg){
    toastr.options = {
        closeButton: false,
        progressBar: false,
        showMethod: 'slideDown',
        timeOut: 2000
    };
    toastr.success(msg);
}

// 确定提示框
function salert(msg,callback){
    swal({
        title: "系统提示",
        text: msg
    },callback);

}
// 定时器执行
function timerCount(cno){
    if(cno == "agent-status-timer" || cno == "airTime"){
        var timeId = $("#"+cno);
    }else{
        var timeId = $("."+cno);    
    }
    var theDay = timeId.eq(0).text();
    var theDayStr = theDay.split(':');
    var flage = 0;
    for(var i=0;i<3;i++){
        if(!isNaN(theDayStr[i])){
            flage++;
        }
    }
    if(flage == 3){
        var second = parseInt(theDayStr[2],10);
        var minute = parseInt(theDayStr[1],10);
        var hour = parseInt(theDayStr[0],10);
        second++;
        if(second >= 60){
            minute = minute+1;
            second = 0;
        }
        if(minute >= 60){
            hour = hour+1;
            minute = 0;
        }
        if(second.toString().length <2 )second = "0"+second;
        if(minute.toString().length <2)minute = "0"+minute;
        if(hour.toString().length <2)hour = "0"+hour;
        var timeWrite = hour+":"+minute+":"+second;
        timeId.text(timeWrite);
    }
    else{
        timeId.text("--");
    }
}


$(document).ready(function () {

		var ws = null;
        var reconn_interval = null;
        var other_login = false;

        function ws_connect(){
                if (window.WebSocket) {
                    if(ws == null) {
                        ws = new WebSocket("wss://" + window.location.host + "/ws");

                        ws.onmessage = function (event) {
                            window.console.info(event.data);
                            data = $.parseJSON(event.data);
                            if (data.mtype=='notify_answer_call'){  //外呼中
                                //$('#cancel-call').hide();
                                $("#call-control a").hide();
                                if (data['data']['direction']=='out'){
                                    $('#hangup-call-outcall').html('外呼中..').show();
                                }else{
                                    $('#hangup-call-outcall').html('座席来电..').show(); 
                                }
                            }
                            if (data.mtype=='notify_answered_call'){ //通话中
                                //$('#hangup-call-outcall').hide();
                                $("#call-control a").hide();
                                $('#hangup-call-calling').show();
                            }
                            if (data.mtype=='notify_hangup_call'){  //挂断电话
                                //$('#hangup-call-calling').hide();
                                $("#call-control a").hide();
                                $('#dial-btn').show();
                            }
                            if (data.mtype=='notify_other_login'){  //重复登录
                                other_login = true;
                                salert('其他地方重复登录了，您将退出系统',function(){
                                    window.location.href = '/xadmin/logout/';
                                })
                            }
                            if (data.mtype=='notify_bill_create'){  //话单创建
                                var bid = data['data']['bid'];
                                var cid = data['data']['cid'];
                                notify('弹屏提示');
                                $('#bill-open').attr('href','/xadmin/funcs/partner/'+cid+'/update/').click();
                            }
                            if (data.mtype=='notify_status_change'){  //坐席状态改变
                                var userkey = data['data']['userkey'];
                                var status = data['data']['status'];
                                status_info = status.split('|');
                                $agent = $('#agent-'+userkey);
                                $agent.text(status_info[2]);
                                $agent.attr('uuid', status_info[3]);
				$spybtn = $('button#spy-'+userkey+'');
				if (status_info[3]){
					$spybtn.show();
				}else{
					$spybtn.hide();
				}
                                if (status_info[1]=='idle'){
                                   $agent.removeClass('label-default label-warning').addClass('label-success');
                                   $agent.prev('i').css({'color':'green'});
                                }
                                else if (status_info[1]=='offline'){
                                   $agent.removeClass('label-success label-warning').addClass('label-default');
                                   $agent.prev('i').css({'color':''});
                                }
                                else {
                                   $agent.removeClass('label-success label-default').addClass('label-warning');
                                   $agent.prev('i').css({'color':'yellow'});
                                }
                            }
                            if (data.mtype=='notify_reg_change'){
                                if (data['data']['reg']){
                                    $('#reg-status').removeClass('label-warning').addClass('label-primary').text('话机已注册');
                                    $('#btn-websip').hide();
                                }else{
                                    $('#reg-status').removeClass('label-primary').addClass('label-warning').text('话机未注册');
                                    $('#btn-websip').show();
                                }
                            }
                            if (data.mtype=='notify_number_info'){
                                //notify(data['data']['info']);
                                toastr.options = {
                                    closeButton: false,
                                    progressBar: false,
                                    showMethod: 'slideDown',
                                    timeOut: 20000
                                };
                                toastr.success(data['data']['info']);
                            }
                            if (data.mtype=='call_spy_response'){
                                toastr.options = {
                                    closeButton: false,
                                    progressBar: false,
                                    showMethod: 'slideDown',
                                    timeOut: 2000
                                };
                                if (data.data.code==0){
                                    toastr.success('监听成功！将收到系统来电');
                                }else if (data.data.code==-9){
                                    toastr.warning('无权限的操作');
                                }else{
                                    toastr.error('监听失败,请确认其是否为通话状态');
                                }
                            }
                        };

                        ws.onopen = function () {
                            window.console.info('WebSocket connected!');
                            $("#call-control a").hide();
                            $('#dial-btn').show();
                            notify('上线成功');
                            //$('#line-status').hide();
                            //ws.send(JSON.stringify({'url': window.location.pathname, 'data': data}));
                            if (reconn_interval){
                                clearInterval(reconn_interval);
                                reconn_interval = null;
                            }
                        };

                        ws.onclose = function () {
                            window.console.info('WebSocket disconnected!');
                            ws = null;
                            //$('#dial-btn').hide();
                            $("#call-control a").hide();
                            $('#line-status').show();
                            if (other_login){
                                if (reconn_interval){
                                    clearInterval(reconn_interval);
                                }
                            }else{
                                if (!reconn_interval){
                                    reconn_interval = setInterval(ws_connect,5000);//每隔5s尝试重连一次
                                }
                            }
                       };
                    }
                    else{
                        //ws.send(JSON.stringify({'url': window.location.pathname, 'data': data}));
                    }

                }
                else{
                    alert("Sorry, your browser does not support WebSocket!");
                }

        }
                ws_connect();

                $('#dial-btn').click(function (){// 发起呼叫
                    _number = $('#to_number').val().replace(/-|\s/g,'');
                    if (!_number){
                        notify('请输入有效的号码');
                        return;
                    }
                    _msg = '{"mtype": "req_dial", "data": {"to_number": "'+ _number +'"}}'
                    ws.send(_msg);
                    $("#call-control a").hide();
                    $('#cancel-call').show();
                });
                $('#line-status').click(function (){//重连ws
                    ws_connect();
                });
                $('#cancel-call').click(function (){//取消呼叫
                    _msg = '{"mtype": "req_cancel", "data": {}}'
                    ws.send(_msg);
                    $("#call-control a").hide();
                    $('#dial-btn').show();
                });
                $('#hangup-call-outcall').click(function (){ //挂断
                    _msg = '{"mtype": "req_hangup", "data": {}}'
                    ws.send(_msg);
                    $("#call-control a").hide();
                    $('#dial-btn').show();
                });
                $('#hangup-call-calling').click(function (){// 挂断通话中的电话
                    _msg = '{"mtype": "req_hangup", "data": {}}'
                    ws.send(_msg);
                    $("#call-control a").hide();
                    $('#dial-btn').show();
                });

        // 用户切换状态
        $("a.status-select").click(function(){
            _msg = '{"mtype": "req_change_status", "data": {"status": "'+ $(this).attr('sid')  +'" }}';
            ws.send(_msg);
            if ($(this).attr('sid')=='0'){
                $(".status-selected").removeClass('btn-danger').addClass('btn-success');
            }else{
                $(".status-selected").removeClass('btn-success').addClass('btn-danger');
            }
            var t_text = $(".status-selected").find(".status-display").text();
            var t_sid = $(".status-selected").attr('sid');
            $(".status-selected").find(".status-display").text($(this).text());
            $(".status-selected").attr('sid',$(this).attr('sid'));
            $(this).text(t_text);
            $(this).attr('sid',t_sid);
            $('#agent-status-timer').text('00:00:00');

        });

    // 拨号盘实现
    $('#btn-keyboard').click(function(){
      $("#kb-well").toggle();
    });
    $('#kb-well button').click(function(){
       var $this = $(this); 
       if ($this.text()=='c'){
           $('#to_number').val('');
       }else if ($this.text()=='x'){
           _val = $('#to_number').val();
           $('#to_number').val(_val.substring(0,_val.length-1));
       }else{
           _val = $('#to_number').val();
           $('#to_number').val(_val + $this.text());
       }
    });

    var stateTimeIntervalid = setInterval("timerCount('agent-status-timer')",1000);

    var checkRegInterval = null;

    function check_reg(){
        _msg = '{"mtype": "check_reg_change", "data": {}}';
        ws.send(_msg);
    }
    function clear_check_reg(){
        if (checkRegInterval)clearInterval(checkRegInterval);
    }
    $('#btn-websip').click(function(){
        window.open('/static/client/phone.html','Web Call','height=550,width=340,status=no,toolbar=no,menubar=no,location=no,resizable=no,scrollbars=0,titlebar=no');
        checkRegInterval = setInterval(check_reg,2000);
        setTimeout(clear_check_reg,10000);
    });
    $("button.btn-spy").click(function (){
	    var uuid = $(this).next().attr("uuid");
        _msg = '{"mtype": "do_call_spy", "data": {"uuid":"' + uuid + '"}}';
        ws.send(_msg);
    });

});
