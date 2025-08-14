$(document).ready(function() {

  $(theRedButton).click(function(){
    //$("h1, h2, h3").css("color", "red");
    $("h1, h2, h3").addClass("redElements");
  });
   $(theSpeakersButton).click(function(){
    $("#speakerHeading").fadeOut(1000);
  });
  
  
});