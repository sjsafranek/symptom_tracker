
const Forms = {

    _getMinSessionDateTime: function(days) {
        days = days || 1;
        let offset = 86400*1000*days;
        let min = new Date();
        min.setTime(min.getTime() - offset);
        return min;
    },

    _getMinSessionDate: function(days) {
        let min = Forms._getMinSessionDateTime();
        return min.toISOString().slice(0, 10);
    },

    _reload(response) {
        window.location.reload();
    },

    createClientSession: function(client_id) {
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
                Api.createClientSession(client_id, result.value)
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
    },

    setSessionNoShow: function(session) {
        Swal.fire({
            title: `Do you want to mark '${session.date}' as a no show?`,
            showCancelButton: true,
            confirmButtonText: "Disable",
            icon: "warning",
        }).then((result) => {
            if (result.isConfirmed) {
                Api.setSessionNoShow(session.id)
                    .then(Forms._reload)
                    .catch(UI.displayError);
            }
        });
    },

    _siteOptions: {
        "A1": "A1",
        "A2": "A2",
        "C3": "C3",
        "C4": "C4",
        "Cz": "Cz",
        "F3": "F3",
        "F4": "F4",
        "F7": "F7",
        "F8": "F8",
        "Fp1": "Fp1",
        "Fp2": "Fp2",
        "Fz": "Fz",
        "O1": "O1",
        "O2": "O2",
        "P3": "P3",
        "P4": "P4",
        "Pz": "Pz",
        "T3": "T3",
        "T4": "T4",
        "T5": "T5",
        "T6": "T6"
    },

    _modalityOptions: {
        'ILF': 'ILF',
        'AlphaTheta': 'AlphaTheta',
        'FrequencyBand': 'FrequencyBand',
        'Synchrony': 'Synchrony'
    },

    _getProtocolSettings: function(modality) {

        function generateModalityFrequencySetting(options) {
            return {
                ...options,
                input: 'number',
                animation: false,
                cancelButtonText: 'Back',
                currentProgressStep: 4
            }
        }

        switch(modality) {
            case "AlphaTheta":
                return [
                    generateModalityFrequencySetting({
                        title: 'Alpha Frequency',
                        inputAttributes: {
                            min: 8.0,
                            max: 13.0,
                            step: 0.000001
                        },
                        inputPlaceholder: "hertz",
                        preConfirm: (value) => {
                            return {
                                type: "frequency_alpha",
                                unit: "hertz",
                                value: value
                            }
                        }                        
                    }),
                    generateModalityFrequencySetting({
                        title: 'Theta Frequency',
                        inputAttributes: {
                            min: 3.5,
                            max: 7.9,
                            step: 0.000001
                        },                        
                        inputPlaceholder: "hertz",
                        preConfirm: (value) => {
                            return {
                                type: "frequency_theta",
                                unit: "hertz",
                                value: value
                            }
                        }
                    })
                ];
            case "ILF":
                return [
                    generateModalityFrequencySetting({
                        title: 'ILF Frequency',
                        inputAttributes: {
                            min: 0.000001,
                            max: 100.0,
                            step: 0.000001
                        },
                        inputPlaceholder: "hertz",
                        preConfirm: (value) => {
                            return {
                                type: "frequency",
                                unit: "millihertz",
                                value: value
                            }
                        }
                    })
                ];
            case "FrequencyBand":
                return [
                    generateModalityFrequencySetting({
                        title: 'FrequencyBand Frequency',
                        inputAttributes: {
                            min: 0.000001,
                            max: 100,
                            step: 0.000001
                        },                        
                        inputPlaceholder: "hertz",
                        preConfirm: (value) => {
                            return {
                                type: "frequency",
                                unit: "hertz",
                                value: value
                            }
                        }
                    })
                ];
            case "Synchrony":
                return [
                    generateModalityFrequencySetting({
                        title: 'Synchrony Frequency',
                        inputAttributes: {
                            min: 0.01,
                            max: 0.05,
                            step: 0.000001
                        },                        
                        inputPlaceholder: "hertz",
                        preConfirm: (value) => {
                            return {
                                type: "frequency",
                                unit: "millihertz",
                                value: value
                            }
                        }
                    })
                ];
            default:
                return [];
        }
    },

    addSessionProtocolSetting: function(session) {
        let self = this;

        const steps = ['1', '2', '3', '4', '5', '6']
        const Queue = Swal.mixin({
            progressSteps: steps,
            showCloseButton: true,
            inputAttributes: { required: true },
            confirmButtonText: 'Next',
            reverseButtons: true,
            // optional classes to avoid backdrop blinking between steps
            showClass: { backdrop: 'swal2-noanimation' },
            hideClass: { backdrop: 'swal2-noanimation' }
        });

        let data = {
            "0": {isConfirmed: false, value: null},
            "1": {isConfirmed: false, value: null},
            "2": {isConfirmed: false, value: null},
            "3": {isConfirmed: false, value: null},
            "4": {isConfirmed: false, value: null},
            "5": {isConfirmed: false, value: null}
        };

        function getStepByIndex(idx) {
            let steps = [
                {
                    title: 'Select a modality',
                    input: 'select',
                    inputOptions: Forms._modalityOptions,
                    inputPlaceholder: 'Select an modality',
                    currentProgressStep: 0,
                    preConfirm: (value) => {
                        return {
                            type: "modality",
                            value: value
                        }
                    }
                },
                {
                    title: 'Duration',
                    input: 'number',
                    inputAttributes: {
                        min: 1,
                        max: 120,
                        step: 1
                    },
                    inputPlaceholder: 'minutes',
                    showCancelButton: true,
                    cancelButtonText: 'Back',
                    animation: false,
                    currentProgressStep: 1,
                    preConfirm: (value) => {
                        return {
                            type: "duration",
                            value: value
                        }
                    }
                },
                {
                    title: 'Select a site',
                    input: 'select',
                    inputOptions: Forms._siteOptions,
                    inputPlaceholder: 'Select an site',
                    showCancelButton: true,
                    cancelButtonText: 'Back',
                    animation: false,
                    currentProgressStep: 2,
                    preConfirm: (value) => {
                        return {
                            type: "site1",
                            value: value
                        }
                    }
                },
                {
                    title: 'Select a site',
                    input: 'select',
                    inputOptions: Forms._siteOptions,
                    inputPlaceholder: 'Select an site',
                    showCancelButton: true,
                    cancelButtonText: 'Back',
                    animation: false,
                    currentProgressStep: 3,
                    preConfirm: (value) => {
                        return {
                            type: "site2",
                            value: value
                        }
                    }
                },
                ...self._getProtocolSettings(data["0"].value && data["0"].value.value),
                {
                    title: 'Notes',
                    input: 'text',
                    inputPlaceholder: 'notes',
                    showCancelButton: true,
                    cancelButtonText: 'Back',
                    animation: false,
                    currentProgressStep: 5,
                    confirmButtonText: 'OK',
                    preConfirm: (value) => {
                        return {
                            type: "notes",
                            value: value
                        }
                    }
                }
            ];

            if (idx >= steps.length) return null;
            return steps[idx];
        }

        //.BEGIN Collect Protocol Info
        (async () => {
            let idx = 0;
            let step = getStepByIndex(idx);
            while(null != step) {
                await Queue.fire(step)
                        .then((result) => {
                            data[`${idx}`] = result;
                            if (result.isConfirmed) idx++;
                            if (result.isDismissed) idx--;
                            if ("close" == result.dismiss) idx = 100;
                        });
                step = getStepByIndex(idx);
            }

            if (100 != idx) {
                let settings = {};
                let values = Object.values(data).map(d => {return d.value})
                for (let i=0; i<values.length; i++) {
                    let k = values[i].type;
                    let v = values[i].value;
                    settings[k] = v;
                }
                Api.addSessionProtocolSetting(session.id, settings)
                    .then(Forms._reload)
                    .catch(UI.displayError);
            }

        })();
        //.END Collect Protocol Info
    }

}
