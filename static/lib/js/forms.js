
const Forms = {

  _getMinSessionDate: function(days) {
    days = days || 1;
    let offset = 86400*1000*days;
    let min = new Date();
    min.setTime(min.getTime() - offset);
    return min;
  },

  createClientSession: function() {
    return Swal.fire({
      title: `Add Session`,
      showCancelButton: true,
      showCloseButton: true,
      input: "date",
      inputAttributes: {
        min: Forms._getMinSessionDate().toISOString().slice(0, 10)
      },
      inputValidator: (value) => {
        // TODO :: check in future??
      }
    })
    .then((result) => {
      if (result.isConfirmed) {
        Api.createClientSession(self._clientID, result.value)
          .then((response) => {
            if ('error' == response.status) return UI.displayError(response);
            window.location.reload();
          });
      }
    });
  },

  setSessionSymptomScore: function(session_id, symptom, score) {
    return Swal.fire({
      title: `${symptom.name}`,
      showCancelButton: true,
      showCloseButton: true,
      input: "number",
      inputValue: score,
      inputAttributes: {
        min: '0',  // Sets the minimum allowed value to 1
        max: '10', // Sets the maximum allowed value to 100
        step: '1'  // Optional: defines the step increment for the input
      },
      inputValidator: (value) => {
        if (value === '' || isNaN(value)) {
          return 'Please enter a valid number!';
        }
        const numValue = parseInt(value);
        if (numValue < 0 || numValue > 10) {
          return 'Number must be between 1 and 10!';
        }
        return null; // No error
      }
    })
    .then((result) => {
      if (result.isConfirmed) {
        Api.setSessionSymptomScore(session_id, symptom.id, parseInt(result.value))
          .then((response) => {
            if ('error' == response.status) return UI.displayError(response);
            window.location.reload();
          });
      }
    });
  },

  disableSymptom: function(symptom) {
    Swal.fire({
      title: `Do you want to disable '${symptom.name}'?`,
      showCancelButton: true,
      confirmButtonText: "Disable",
      icon: "warning",
    }).then((result) => {
      if (result.isConfirmed) {
        Api.disableSymptom(symptom.id)
          .then((response) => {
            if ('error' == response.status) return UI.displayError(response);
            window.location.reload();
          });
      }
    });
  }

}
