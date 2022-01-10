//response
socket.on('response', function(msg) {
    //process the event of system
    if(msg.event == 'connect'){
       log("The console's status connection is "+msg.data);
       //process the event of log
    }else if(msg.event == 'log-memory'){
       log(msg.data)
       //process error
    }else{
       log("Error: response a wrong message. event: "+msg.event+" message: "+ msg.data);
    }
});
/**
* Log a text message
* @param {String} txt
*/
function log(v) {
     $("#queryStatus").text("")
     if($("#log-memory").val().length > 0){
         var s = $("#log-memory").val() + '\n';
         v = s + v;
     }
     $("#log-memory").val(v);
     $("#log-memory").scrollTop( $("#log-memory")[0].scrollHeight - $("#log-memory").height() );
}
function clear(){
   $('#log-memory').val('');
}

function query(){
   clear()
   $("#queryStatus").text("   querying...")
   socket.emit('request', {event: 'query_memory', data: ""})
}

