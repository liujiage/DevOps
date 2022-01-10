
//response
socket.on('response', function(msg) {
    //process the event of system
    if(msg.event == 'connect'){
       log("The console's status connection is "+msg.data);
       //process the event of log
    }else if(msg.event == 'log'){
       log(msg.data);
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
     if($("#log").val().length > 0){
         var s = $("#log").val() + '\n';
         v = s + v;
     }
     $("#log").val(v);
     $("#log").scrollTop( $("#log")[0].scrollHeight - $("#log").height() );
}
function clear(){
   $('#log').val('');
}

// The button will be try to write something into the text area.
$('#writeLog').click(function() {
  log('Hello welcome here.');
});

// The button will be try to write something into the text area.
$('#clearLog').click(function() {
  clear();
});
// submit deploy request to backend server
// the data format version-100,tiny-192.168.1.0,tiny-192.168.1.2,.....
function deploySubmit(version){
        var t = $('#html').jstree(true);
		if(!chooseServiceCheck()) {
		     $.alert('Please choose service you want to deploy! ');
		     return ;
		}
		v = []
		v.push('version-'+version);
        for (let i = 0; i < a.length; i++) {
            v.push(t.get_node(a[i]).text)
        }
        dv = v.join(",")
        //$.alert(dv)
		socket.emit('request', {event: 'start_deploy', data: dv});
}
// check deploy servers before submit it to backend server
function chooseServiceCheck(){
        var t = $('#html').jstree(true);
		a = t.get_bottom_checked()
		if(a.length == 0) {
		     //$.alert('Please choose service you want to deploy! ');
		     return false
		}
		return true
}
//prepare deploy the service
$('#evts_button').on('click', function(){
//check select services
if(!chooseServiceCheck()) {
	  $.alert('Please choose service you want to deploy! ');
	  return;
}
//display prompt window to deploy
$.confirm({
    title: 'Deploy Confirm',
    content: '' +
    '<form action="" class="formName">' +
    '<div class="form-group">' +
    '<label>Enter Deploy Version Number</label>' +
    '<input type="number" placeholder="Deploy Version Number" class="name form-control" min="1" max="999999" step="1" required />' +
    '</div>' +
    '</form>',
    buttons: {
        formSubmit: {
            text: 'Submit',
            btnClass: 'btn-blue',
            action: function () {
                var version = this.$content.find('.name').val();
                if(!version){
                    $.alert('Provide a valid the number of version! ');
                    return false;
                }
                //$.alert('Your name is ' + name);
                deploySubmit(version)
            }
        },
        cancel: function () {
            //close
        },
    },
    onContentReady: function () {
        // bind to events
        var jc = this;
        this.$content.find('form').on('submit', function (e) {
            // if the user submits the form by pressing enter in the field.
            e.preventDefault();
            jc.$$formSubmit.trigger('click'); // reference the button and click it
        });
    }
});
});
//initial a tree
$('#html').on("select_node.jstree", function (event, data ) {
            var t = $('#html').jstree(true);
		    a = t.get_bottom_checked()
		    if(a.length == 0) return;
            for (let i = 0; i < a.length; i++) {
                  root = t.get_node(a[i]).text.split("-")[0]
                  if(!data.node.text.includes(root)){
                        $.alert({
                                title: 'Alert!',
                                content: "One time, Choose one service only! You choose service is "+ root + " Now!",
                        });
                     //$('#html').jstree('uncheck_node', data.node.id);
                     t.deselect_node(data.node);
                     event.stopImmediatePropagation();
                     return;
                  }
            }
		}).jstree({
		      "checkbox" : {
                   "keep_selected_style" : false
               },
               "plugins" : [ "wholerow", "checkbox" ]
		});
