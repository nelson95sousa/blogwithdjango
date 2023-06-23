// CHANGE PROFILE PICTURE
function read(val) {
    const reader = new FileReader();
  
    reader.onload = (event) => {
      document.getElementById("display-img-upload").src = event.target.result;
      document.getElementById("display-img-upload").style.display = 'block';
    }
  
    reader.readAsDataURL(val.files[0]);
  }

  // autosize(document.getElementById("id_comment"));

// function getDiv(elem){
//   var div = elem.getAttribute('data-movie-id')
//   document.getElementById(div).style.display="flex";}

// View comments of a comment

// document.addEventListener("click", getDiv(this));

// function GetId(){
//   var v1=document.getElementsByClassName
// }

function getDiv(elem){
  var div = elem.getAttribute('data-movie-id')
  var final_div = document.getElementById(div)

  if (elem.value=="True"){final_div.style.display="none";elem.innerHTML="see more", elem.value="False"; }
  else if (elem.value=="False"){final_div.style.display="flex"; elem.innerHTML="see less",elem.value="True"; }


  // if (final_div.style.display=="flex"){final_div.style.display="none";elem.innerHTML="see more"}
  // if(final_div.style.display=="none") {final_div.style.display="flex"; elem.innerHTML="see less"}

}

// Add Comment of Comment
function getCmt(elem){
  var div = elem.getAttribute('data-movie-id')
  var final_div = document.getElementById(div)
  
  if (elem.value=="True"){final_div.style.display="none";elem.innerHTML="add comment", elem.value="False"; }
  else if (elem.value=="False"){final_div.style.display="flex"; elem.innerHTML="do not add comment",elem.value="True"; }

}



// HAVE TO DO 2 FUNCTIONS, ONE FOR COMMeNT, ANOTHER TO SEE MORE