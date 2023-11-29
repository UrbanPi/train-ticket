function onLoadBody(){
    //请求信息封装
    var url = location.search;
    var request = new Object();
    if(url.indexOf("?") != -1) {
        var str = url.substr(1)　//去掉?号
        strs = str.split("&");
        for(var i = 0;i<strs.length;i++)
        {
            request[strs[i ].split("=")[0]]=unescape(strs[ i].split("=")[1]);
        }
    }
    var requestInfo = new Object();
    requestInfo.orderId = request["orderId"];
    var tripType = request["train_number"].charAt(0);
    if(tripType == 'G' || tripType == 'D'){
        requestInfo.type = 1;
    }else{
        requestInfo.type = 0;
    }
    var data = JSON.stringify(requestInfo);

    //发送请求
    var ajaxTimeOut = $.ajax({
        type: "post",
        url: "/getVoucher",
        contentType: "application/json",
        dataType: "json",
        timeout: 5000,
        data:data,
        success: function(result){
            document.getElementById("voucher_id").innerText = "10000" + result.voucher_id;
            document.getElementById("order_id").innerText = result.order_id;
            document.getElementById("travel_date").innerText = result.travelDate;;
            document.getElementById("passenger_name").innerText = result.contactName;
            document.getElementById("train_number").innerText = result.train_number;
            document.getElementById("seat_number").innerText = result.seat_number;
            document.getElementById("start_station").innerText = result.start_station;
            document.getElementById("dest_station").innerText = result.dest_station;
            document.getElementById("price").innerText = result.price;
        },
        complete: function(XMLHttpRequest,status){
            if(status=='timeout'){//超时,status还有success,error等值的情况
                ajaxTimeOut.abort(); //取消请求
                alert("Timeout!");
            }
        }
    });
}
