$(document).ready(function() {

  var month = document.getElementById("month");
  let date = new Date();
  const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  selectedYear = date.getYear() + 1900;
  selectedMonth = date.getMonth();



  const year = document.createElement("select");
  year.id = "yearDropdown";
  for (let i = 0; i <= date.getYear(); i++) {
    let option = document.createElement("option");
    option.value = i + 1900;
    option.innerText = i + 1900;
    year.appendChild(option);
  }
  year.value = date.getYear() + 1900;
  document.body.insertBefore(year, month);
  year.addEventListener('change', function() {
    selectedYear = this.value;
    document.getElementById("month").querySelectorAll('[id^=day], .empty').forEach(n => n.remove());
    generateDays();
  });

  const months = document.createElement("select");
  months.id = "monthsDropdown";
  for (let i = 0; i < 12; i++) {
    let option = document.createElement("option");
    option.value = i;
    option.innerText = monthNames[i];
    months.appendChild(option);
  }
  months.value = date.getMonth();
  document.body.insertBefore(months, month);
  months.addEventListener('change', function() {
    selectedMonth = this.value;
    document.getElementById("month").querySelectorAll('[id^=day], .empty').forEach(n => n.remove());
    generateDays();
  });

  for (let i = 0; i < 7; i++) {
    var div = document.createElement("div");
    div.id = "wd" + i.toString();

    var weekdaysDiv = document.createElement("div");
    weekdaysDiv.appendChild(document.createTextNode(weekdays[i]));
    weekdaysDiv.className = "weekdays";
    div.appendChild(weekdaysDiv);
    month.appendChild(div);
  }

  generateDays();

  function generateDays() {

    //determine weekday that day1 is on
    var d1 = new Date(selectedYear, selectedMonth, 1);
    for (var i = 0; i < 7; i++) {
      if (i < d1.getDay()) {
        daysBefore = "wd" + (i).toString();
        emptySpot = document.createElement("div");
        emptySpot.className = "empty";
        document.getElementById(daysBefore).appendChild(emptySpot);
      }
    }

    for (var i = 0; i < 31; i++) {
      var d = new Date(selectedYear, selectedMonth, i + 1);
      var weekday = "wd" + (d.getDay()).toString();
      var day = document.createElement("div");
      day.id = "day" + (i + 1).toString();
      document.getElementById(weekday).appendChild(day).appendChild(document.createTextNode((i + 1).toString()));

      day.addEventListener('click', function() {
        const selectedDay = document.querySelector('.selected');
        if (selectedDay) {
          selectedDay.classList.remove('selected');
        }
        this.classList.add('selected');
      });
    }
  }
});