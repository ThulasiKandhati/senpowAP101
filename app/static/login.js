
function clear_alerts()
{
  console.log('Clearing alert')
  const element = document.querySelector('#alert1')
  element.innerHTML = "";
  return element;
}


function submit()
{  
  element = clear_alerts()
  console.log('alert_disp1')
  
  if (post_form() == true)
    {
     console.log('Submmited')
   }
}

function post_form()
{
  const URL = '/resetpwd'
  const xhr = new XMLHttpRequest();
  xhr.open('POST', URL);
  xhr.onreadystatechange = function () {
  // In local files, status is 0 upon success in Mozilla Firefox
  if(xhr.readyState === XMLHttpRequest.DONE) {
    const status = xhr.status;
    if (status === 0 || (status >= 200 && status < 400)) {
      // The request has been completed successfully
     console.log(xhr.responseText);
     element.insertAdjacentHTML('beforeend', '<div class="alert alert-primary">Please submmit with <strong>email verification Code</strong> and <strong>Reset password</strong> details.</div>');
    } else {
      // Oh no! There has been an error with the request!
    }
  }
}
  xhr.send();
return true
}


function doit(val)
{
  element = clear_alerts()
  console.log('alert_disp1')
     element.insertAdjacentHTML('beforeend', '<div class="alert alert-primary">Please submmit with <strong>email verification Code</strong> and <strong>Reset password</strong> details.</div>');
}
