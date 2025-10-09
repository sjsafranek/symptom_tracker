

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
  }
  
}
