
function create_user()
{
 if (document.getElementsByName('.check_0').checked || document.getElementsByName('.check_1').checked || document.getElementsByName('.check_2').checked || document.getElementsByName('.check_3').checked)
 {
     console.log('User already created')
 }
else
  {
     alert('Creating User...');
  } 
}

function resetpwd()
{
   if (document.getElementsByName('.check_0').checked || document.getElementsByName('.check_1').checked || document.getElementsByName('.check_2').checked || document.getElementsByName('.check_3').checked)
 {
     alert('Resetting Password...');
 }
else
  {
     alert('Create user to reset the password!');
  }
}
