//https://onehtmlpagechallenge.com/entries/css-calc.html
$(document).ready(function() {
  
  var buttons = document.querySelectorAll( ".number" );
  for ( var counter = 0; counter < buttons.length; counter++)
  {
      buttons[counter].addEventListener("click", function(){
          //****  JavaScript Feature submission - Modification of the DOM **** 
          document.getElementById("display").value += this.innerHTML;
          event.preventDefault();
          
     });
  }
  
  //****  JavaScript Feature submission - Equals Button Event Listener **** 
  document.getElementById("equal").addEventListener( "click", function(){
    var display = document.getElementById("display").value;
    var result = eval(display);
    document.getElementById("display").value = result;
    event.preventDefault();
  });

  //****  JavaScript Feature submission - Radio Button Event Listener **** 
  document.getElementById("dark").addEventListener( "click", function(){
    document.getElementById("calculator").style.backgroundColor = "black";
  });

  document.getElementById("light").addEventListener( "click", function(){
    document.getElementById("calculator").style.backgroundColor = "#e1e6ed";
  });

  //****  JavaScript Feature submission - Alert within event listener **** 
  document.getElementById("favOpDropdown").addEventListener( "change", function(){
    value = document.getElementById("favOpDropdown").value;
    alert("I love "+value+" too!");
  });
  
});
