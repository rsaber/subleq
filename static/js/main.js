function step(len,height){
	var maxCell = len*height;
	currState = {};
	for(i = 0; i < maxCell; i++){
		currState[i] = document.getElementById(i.toString()).value;
	}
	currState.pc = document.getElementsByName('pc')[0].id;
	currState.len = len;
	currState.height = height;
	$.get("/step",currState,function(r){setState(r)}, 'json');
}

function run(len,height){
	var maxCell = len*height;
	currState = {};
	for(i = 0; i < maxCell; i++){
		currState[i] = document.getElementById(i.toString()).value;
	}
	currState.pc = document.getElementsByName('pc')[0].id;
	currState.len = len;
	currState.height = height;
	$.get("/run",currState,function(r){setState(r)}, 'json');
}

function pcReset(){
	// unset previous pc cell
	document.getElementsByName('pc')[0].parentNode.style.backgroundColor = "";
	document.getElementsByName('pc')[0].name = ''
	// set new pc cell
	document.getElementById('0').parentNode.style.backgroundColor = "rgba(51,122,183,0.2)";
	document.getElementById('0').name = 'pc';
}

function submit(len,height,chall){
	var maxCell = len*height;
	currState = {};
	for(i = 0; i < maxCell; i++){
		currState[i] = document.getElementById(i.toString()).value;
	}
	currState.pc = document.getElementsByName('pc')[0].id;
	currState.len = len;
	currState.height = height;
	$.get("/test/"+chall.toString(),currState,function(r){
		if(r.hasOwnProperty('error')){
			bootbox.alert({
				message: r.error,
				backdrop: true
			})
		}
		else if(r.output == true){
			bootbox.alert({
				message: "All Tests Passed!",
				backdrop: true
			})
		}else{
			console.log(r)
			bootbox.alert({
				message: "Test Failed!",
				backdrop: true
			})
		}
	}, 'json');
}

function setState(response){
	if(response.hasOwnProperty('error')){
		bootbox.alert({
			message: response.error,
			backdrop: true
		})
		return
	}
	var maxCell = response.len*response.height;
	for(i = 0; i < maxCell; i++){
		document.getElementById(i.toString()).value = response[i]
	}
	// unset previous pc cell
	document.getElementsByName('pc')[0].parentNode.style.backgroundColor = "";
	document.getElementsByName('pc')[0].name = ''
	// set new pc cell
	document.getElementById(response['pc']).parentNode.style.backgroundColor = "rgba(51,122,183,0.2)";
	document.getElementById(response['pc']).name = 'pc';
}