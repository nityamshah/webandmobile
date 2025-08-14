// builds grid of numRows x numCols <div> elements
var buildEtch = function(sz) {

  var boxSize = $('.container').height() / sz;
  console.log("boxSize =", boxSize)

  for (let i = 0; i < sz; i++) {
    let row = document.createElement("div");
    row.className = "row";
    row.id = "row" + i.toString();
    $(".container").append(row);
    $(row).css("height", boxSize);
    for (let j = 0; j < sz; j++) {
      let box = document.createElement("div");
      box.className = "box";
      box.id = "box" + j.toString();
      $(row).append(box);
      $(box).css("width", boxSize).css("height", boxSize);
    }
  }
};

$(document).ready(function() {

  ifRandom = false;
  color = "black";
  size = 50;
  buildEtch(size)

  //function to get random color called getRandomColor
  function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  $('#resChange').click(function() {
    $('.container').empty();
    color = "black";
    ifRandom = false;

    haveSize = false;
    while (haveSize === false) {
      oldSize = size;
      size = prompt("Please enter a grid size from 1-128");
      if (size > 0 && size <= 128) {
        haveSize = true
      } else if (size === null) {
        size = oldSize;
        haveSize = true
      } else {
        alert("The number you entered is outside the range!")
      };
    };
    buildEtch(size);
    $('.box').mouseover(function() {
      if (ifRandom) {
        $(this).css("background-color", getRandomColor());
      } else {
        $(this).css("background-color", color);
      }
    });
  });

  $('.box').mouseover(function() {
    if (ifRandom) {
      $(this).css("background-color", getRandomColor());
    } else {
      $(this).css("background-color", color);
    }
  });

  $('#cTBlack').click(function() { color = "black"; ifRandom = false; });
  $('#cTRed').click(function() { color = "red"; ifRandom = false; });
  $('#cTBlue').click(function() { color = "blue"; ifRandom = false; });
  $('#cTYellow').click(function() { color = "yellow"; ifRandom = false; });
  $('#rand').click(function() {
    ifRandom = true;
  });
})
