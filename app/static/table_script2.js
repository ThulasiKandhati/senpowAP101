(document).ready(function() {
  alert('Hell')
});

function edit_row(no)
{
 document.getElementById("edit_button"+no).setAttribute("disabled","disabled");
 document.getElementById("save_button"+no).removeAttribute("disabled");
	
 // var activity=document.getElementById("activity"+no);
 var start=document.getElementById("start"+no);
 var start1=document.getElementById("start1"+no);
 var start2=document.getElementById("start2"+no);
 var start3=document.getElementById("start3"+no);
 var start4=document.getElementById("start4"+no);
 var start5=document.getElementById("start5"+no);
 var end=document.getElementById("end"+no);
 
 //var activity_data=activity.innerHTML;
 var start_data=start.innerHTML;
 var start1_data=start1.innerHTML;
 var start2_data=start2.innerHTML;
 var start3_data=start3.innerHTML;
 var start4_data=start4.innerHTML;
 var start5_data=start5.innerHTML;
 var end_data=end.innerHTML;
 
 //activity.innerHTML="<input type='text' id='activity_text"+no+"' value='"+activity_data+"'>";
 start.innerHTML="<input type='number' id='start_text"+no+"' value='"+start_data+"' min='1' max='8'>";
 start1.innerHTML="<input type='number' id='start1_text"+no+"' value='"+start1_data+"' min='1' max='8'>";
 start2.innerHTML="<input type='number' id='start2_text"+no+"' value='"+start2_data+"' min='1' max='8'>";
 start3.innerHTML="<input type='number' id='start3_text"+no+"' value='"+start3_data+"' min='1' max='8'>";
 start4.innerHTML="<input type='number' id='start4_text"+no+"' value='"+start4_data+"' min='1' max='8'>";
 start5.innerHTML="<input type='number' id='start5_text"+no+"' value='"+start5_data+"' min='1' max='8'>";
 end.innerHTML="<input type='number' id='end_text"+no+"' value='"+end_data+"' min='1' max='8'>";
}

function save_row(no)
{
 //var activity_val=document.getElementById("activity_text"+no).value;
 var start_val=document.getElementById("start_text"+no).value;
 var start1_val=document.getElementById("start1_text"+no).value;
 var start2_val=document.getElementById("start2_text"+no).value;
 var start3_val=document.getElementById("start3_text"+no).value;
 var start4_val=document.getElementById("start4_text"+no).value;
 var start5_val=document.getElementById("start5_text"+no).value;
 var end_val=document.getElementById("end_text"+no).value;
 console.log('save1'); 
 //document.getElementById("activity"+no).innerHTML=activity_val;
 document.getElementById("start"+no).innerHTML=start_val;
 document.getElementById("start1"+no).innerHTML=start1_val;
 document.getElementById("start2"+no).innerHTML=start2_val;
 document.getElementById("start3"+no).innerHTML=start3_val;
 document.getElementById("start4"+no).innerHTML=start4_val;
 document.getElementById("start5"+no).innerHTML=start5_val;
 document.getElementById("end"+no).innerHTML=end_val;
 console.log('save2');
 document.getElementById("edit_button"+no).removeAttribute("disabled");
 document.getElementById("save_button"+no).setAttribute("disabled","disabled");
}

function delete_row(no)
{
 document.getElementById("row"+no+"").outerHTML="";
}


function add_row()
{
 lact = document.getElementById("new_activity");
 var act = lact.options[lact.selectedIndex].text;
 console.log(act);
 if (act == "Select Activity")
  {
    alert("Error: Select activity")
    return true
  }
  console.log('val1 pass');
 if ((document.getElementById("new_start").value.length <= 0) || (document.getElementById("new_start1").value.length <= 0) || (document.getElementById("new_start2").value.length <= 0) || (document.getElementById("new_start3").value.length <= 0) || (document.getElementById("new_start4").value.length <= 0) || (document.getElementById("new_start5").value.length <= 0) || (document.getElementById("new_end").value.length <= 0))
  {
    alert("Error: can't clock less than zero")
    return true
  }
 console.log('val2 pass');
 if ((document.getElementById("new_start").value < 0) || (document.getElementById("new_start1").value < 0) || (document.getElementById("new_start2").value < 0) || (document.getElementById("new_start3").value < 0) || (document.getElementById("new_start4").value < 0) || (document.getElementById("new_start5").value < 0) || (document.getElementById("new_end").value < 0))
  {
    alert("Error: can't clock less than zero")
    return true
  }
 console.log('val3 pass');
 var new_activity=act;
 var new_start=document.getElementById("new_start").value;
 var new_start1=document.getElementById("new_start1").value;
 var new_start2=document.getElementById("new_start2").value;
 var new_start3=document.getElementById("new_start3").value;
 var new_start4=document.getElementById("new_start4").value;
 var new_start5=document.getElementById("new_start5").value;
 var new_end=document.getElementById("new_end").value;
 console.log('add row, get elements')	
 var table=document.getElementById("tblClock");
 console.log('summed')
 var table_len = reset_tot('NEW');
 console.log(start_t)
console.log(table_len)
var row = table.insertRow(table_len).outerHTML="<tr id='row"+table_len+"'><td id='activity"+table_len+"'>"+new_activity+"</td><td id='start"+table_len+"'>"+new_start+"</td><td id='start1"+table_len+"'>"+new_start1+"</td><td id='start2"+table_len+"'>"+new_start2+"</td><td id='start3"+table_len+"'>"+new_start3+"</td><td id='start4"+table_len+"'>"+new_start4+"</td><td id='start5"+table_len+"'>"+new_start5+"</td><td id='end"+table_len+"'>"+new_end+"</td><td><input type='button' id='edit_button"+table_len+"' value='Edit' class='btn btn-dark' onclick='edit_row("+table_len+")'> <input type='button' id='save_button"+table_len+"' value='Save' class='btn btn-dark' onclick='save_row("+table_len+")' disabled> <input type='button' value='Delete' class='btn btn-dark' onclick='delete_row("+table_len+")'></td></tr>";
 //adding new balnk row
 document.getElementById("new_activity").value="Select Activity";
 document.getElementById("new_start").value="0";
 document.getElementById("new_start1").value="0";
 document.getElementById("new_start2").value="0";
 document.getElementById("new_start3").value="0";
 document.getElementById("new_start4").value="0";
 document.getElementById("new_start5").value="0";
 document.getElementById("new_end").value="0";

}

function save()
{
  const element = document.querySelector('#alert-container')
  element.insertAdjacentHTML('beforeend', '<div class="alert alert-success alert-dismissible"><button type="button" class="btn-close" data-bs-dismiss="alert"></button> <strong>Success!</strong>.Timesheet submitted.</div>');
}

function cancel()
{
  const element = document.querySelector('#alert-container')
  element.insertAdjacentHTML('beforeend', '<div class="alert alert-danger alert-dismissible"><button type="button" class="btn-close" data-bs-dismiss="alert"></button><strong>Error!</strong>.Timesheet not submitted.</div>');
}

function reset_tot(call)
{
  start_t = 0
  start1_t = 0
  start2_t = 0
  start3_t = 0
  start4_t = 0
  start5_t = 0
  end_t = 0
  var table=document.getElementById("tblClock");
  var table_len=(table.rows.length)-2;
  for (i = 1; i < table_len; i++) {
    start_t += Number(document.getElementById("start"+i).innerHTML);
    start1_t += Number(document.getElementById("start1"+i).innerHTML);
    start2_t += Number(document.getElementById("start2"+i).innerHTML);
    start3_t += Number(document.getElementById("start3"+i).innerHTML);
    start4_t += Number(document.getElementById("start4"+i).innerHTML);
    start5_t += Number(document.getElementById("start5"+i).innerHTML);
    end_t += Number(document.getElementById("end"+i).innerHTML);
  }
  if (call == 'NEW')
  {
    start_t += Number(document.getElementById("new_start").value);
    start1_t += Number(document.getElementById("new_start1").value);
    start2_t += Number(document.getElementById("new_start2").value);
    start3_t += Number(document.getElementById("new_start3").value);
    start4_t += Number(document.getElementById("new_start4").value);
    start5_t += Number(document.getElementById("new_start5").value);
    end_t += Number(document.getElementById("new_end").value);
  }
  document.getElementById("start_tot").innerHTML= start_t ;
  document.getElementById("start1_tot").innerHTML= start1_t;
  document.getElementById("start2_tot").innerHTML= start2_t;
  document.getElementById("start3_tot").innerHTML= start3_t
  document.getElementById("start4_tot").innerHTML= start4_t
  document.getElementById("start5_tot").innerHTML= start5_t
  document.getElementById("end_tot").innerHTML= end_t
  document.getElementById("c_grandtot").innerHTML= "Week Tot:" + Number(start_t)+Number(end_t)
 return table_len;
}
