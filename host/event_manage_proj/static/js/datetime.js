const startInput = document.getElementById('start');
const endInput = document.getElementById('end');

// Calculate minimum start time as 24 hours from now
window.onload = setminDate;

function setminDate(){
    const now = new Date();
    now.setHours(now.getHours() + 24);
    const minStartTime = now.toISOString().slice(0, 16); // Format as YYYY-MM-DDTHH:mm
//    startInput.min = minStartTime;
    s = document.getElementById('start')
    s.setAttribute('min', minStartTime);
}

// Update end input's min value when start input changes
startInput.addEventListener('input', () => {
  const startTime = new Date(startInput.value);
  startTime.setMinutes(startTime.getMinutes() + 10);
  const minEndTime = startTime.toISOString().slice(0, 16);
  endInput.min = minEndTime;
});