
const Forms = {

    _getMinSessionDateTime: function(days) {
        days = days || 1;
        let offset = 86400*1000*days;
        let min = new Date();
        min.setTime(min.getTime() - offset);
        return min;
    },

    _getMinSessionDate: function(days) {
        let min = UI._getMinSessionDateTime();
        return min.toISOString().slice(0, 10);
    },

    _reload(response) {
        window.location.reload();
    },

    createClientSession: function() {
        return Swal.fire({
            title: `Add Session`,
            showCancelButton: true,
            showCloseButton: true,
            input: "date",
            inputAttributes: {
                min: Forms._getMinSessionDate()
            },
            inputValidator: (value) => {
                // TODO :: check in future??
            }
        })
        .then((result) => {
            if (result.isConfirmed) {
                Api.createClientSession(self._clientID, result.value)
                    .then(Forms._reload)
                    .catch(UI.displayError);
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
                min: '0',    // Sets the minimum allowed value to 1
                max: '10', // Sets the maximum allowed value to 100
                step: '1'    // Optional: defines the step increment for the input
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
                    .then(Forms._reload)
                    .catch(UI.displayError);
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
                    .then(Forms._reload)
                    .catch(UI.displayError);
            }
        });
    }

}
