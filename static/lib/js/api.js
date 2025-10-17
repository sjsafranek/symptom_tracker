

// The following function are copying from 
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const Api = {

    fetchClientsByTherapist: function(therapist_id) {
        return fetch(`/api/v1/therapist/${therapist_id}/clients`)
            .then(response => response.json())
            .then(data => data.data.clients);
    },

    fetchSessionsByClient: function(client_id) {
        return fetch(`/api/v1/client/${client_id}/sessions`)
            .then(response => response.json())
            .then(data => data.data.sessions);                
    },

    fetchSymptomsByClient: function(client_id) {
        return fetch(`/api/v1/client/${client_id}/symptoms`)
            .then(response => response.json())
            .then(data => data.data.symptoms);
    },

    fetchSessionProtocol: function(session_id) {
        return fetch(`/api/v1/session/${session_id}/protocol`)
            .then(response => response.json())
            .then(data => data.data.protocol);
    },

    _checkError: function(response) {
        if ('error' === response.status) {
            throw new Error(response.error);
        }
        return response;
    },

    _do: function(api_request) {
        let csrftoken = getCookie('csrftoken');
        return fetch(`/api/v1`, {
            method: "POST",
            headers: { "X-CSRFToken": csrftoken },
            body: JSON.stringify(api_request),
        })
        .then(response => response.json())
        .then(Api._checkError)
    },

    setSessionSymptomScore: function(session_id, symptom_id, symptom_score) {
        return Api._do({
            method: "set_session_symptom_score",
            params: {
                session_id: session_id, 
                symptom_id: symptom_id,
                symptom_score: symptom_score 
            }
        });
    },

    createClientSession: function(client_id, date) {
        return Api._do({
            method: "create_session",
            params: {
                client_id: client_id,
                date: date
            }
        });
    },

    disableSymptom: function(symptom_id) {
        return Api._do({
            method: "disable_symptom",
            params: {
                symptom_id: symptom_id
            }
        });
    },

    setSessionNoShow: function(session_id) {
        return Api._do({
            method: "set_session_no_show",
            params: {
                session_id: session_id
            }
        });
    }

}
