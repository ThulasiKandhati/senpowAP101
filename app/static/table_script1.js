(document).ready(function() {
  alert('Hell')
});

function edit_row(no)
{
 document.getElementById("edit_button"+no).style.display="none";
 document.getElementById("save_button"+no).style.display="block";
	
 var name=document.getElementById("name_row"+no);
 var country=document.getElementById("country_row"+no);
 var age=document.getElementById("age_row"+no);
 var sal=document.getElementById("sal_row"+no);
	
 var name_data=name.innerHTML;
 var country_data=country.innerHTML;
 var age_data=age.innerHTML;
 var sal_data=sal.innerHTML;
	
 name.innerHTML="<input type='text' id='name_text"+no+"' value='"+name_data+"'>";
 country.innerHTML="<input type='text' id='country_text"+no+"' value='"+country_data+"'>";
 age.innerHTML="<input type='number' id='age_text"+no+"' value='"+age_data+"' min='1' max='8'>";
 sal.innerHTML="<input type='number' id='sal_text"+no+"' value='"+sal_data+"' min='1' max='8'>";
}

function save_row(no)
{
 var name_val=document.getElementById("name_text"+no).value;
 var country_val=document.getElementById("country_text"+no).value;
 var age_val=document.getElementById("age_text"+no).value;
 var sal_val=document.getElementById("sal_text"+no).value;

 document.getElementById("name_row"+no).innerHTML=name_val;
 document.getElementById("country_row"+no).innerHTML=country_val;
 document.getElementById("age_row"+no).innerHTML=age_val;
 document.getElementById("sal_row"+no).innerHTML=sal_val;

 document.getElementById("edit_button"+no).style.display="block";
 document.getElementById("save_button"+no).style.display="none";
}

function delete_row(no)
{
 document.getElementById("row"+no+"").outerHTML="";
}

function add_row()
{
  age_tot = 0
  sal_tot = 0
 if (document.getElementById("new_name").value.length == 0)
  {
    alert("Error: Name can't be null")
    return true
  }
 var new_name=document.getElementById("new_name").value;
 var new_country=document.getElementById("new_country").value;
 var new_age=document.getElementById("new_age").value;
 var new_sal=document.getElementById("new_sal").value;
	
 var table=document.getElementById("tblClock");
 var table_len=(table.rows.length)-2;
 for (i = 1; i < table_len; i++) {
   age_tot += Number(document.getElementById("age_row"+i).innerHTML);
   sal_tot += Number(document.getElementById("sal_row"+i).innerHTML);
 }

 document.getElementById("age_tot").innerHTML= age_tot
 document.getElementById("sal_tot").innerHTML= sal_tot
 document.getElementById("age_grandtot").innerHTML= "Week Tot:" + Number(age_tot)+Number(sal_tot)

//adding row to table
var row = table.insertRow(table_len).outerHTML="<tr id='row"+table_len+"'><td id='name_row"+table_len+"'>"+new_name+"</td><td id='country_row"+table_len+"'>"+new_country+"</td><td id='age_row"+table_len+"'>"+new_age+"</td><td id='sal_row"+table_len+"'>"+new_sal+"</td><td><input type='button' id='edit_button"+table_len+"' value='Edit' class='btn btn-dark' onclick='edit_row("+table_len+")'> <input type='button' id='save_button"+table_len+"' value='Save' class='btn btn-dark' onclick='save_row("+table_len+")' style='display: none'> <input type='button' value='Delete' class='btn btn-dark' onclick='delete_row("+table_len+")'></td></tr>";
 //adding new balnk row
 document.getElementById("new_name").value="";
 document.getElementById("new_country").value="";
 document.getElementById("new_age").value="0";
 document.getElementById("new_sal").value="0";
}
