// availability.js

function disableAndStyleWeek(week) {
    var inputWeek = document.getElementById('week');
    var weekInputValue = inputWeek.value;
  
    if (weekInputValue === week) {
      inputWeek.classList.add('unavailable-week');
    }
  
    inputWeek.addEventListener('input', function() {
      if (inputWeek.value === week) {
        inputWeek.classList.add('unavailable-week');
      } else {
        inputWeek.classList.remove('unavailable-week');
      }
    });
  }
  