
const UI = {

  colorScale: d3.scaleLinear()
    .domain([0, 10]) // Input data range
    .range(["blue", "red"]), // Output color range

  makeSymptomScoreProgressBar: function(score, session_id, symptom, listeners) {
    if (score !== undefined) {
      let percentage = (score/10)*100;
      let $progressBar = $(`
      <div class="progress session-symptom-score" role="progressbar" aria-label="Basic example" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
        <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: ${percentage}%; background-color: ${UI.colorScale(score)}">${score}</div>
      </div>`);
      $progressBar.on(listeners);
      return $progressBar;
    }
  },

  makeSessionSymptomScoreButton: function(session_id, symptom, listeners) {
    return $(`<button class="btn btn-sm btn-info btn-symptom-score"> Set </button>`)
      .on(listeners);
  },

  makeProtocolButton: function(sessionId, listeners) {
      return $('<span>')
        .addClass('btn-protocol')
        .data('session-id', sessionId)
        .append('View')
        .on(listeners);
  },

  makeProtocolCard: function(protocol) {
    return $('<div>').addClass('card mt-3').append(
      $('<div>').addClass('card-body').append(
        $('<h5>').addClass('card-title').append(protocol.site),
        $('<h6>').addClass('card-subtitle mb-2 text-body-secondary').append(protocol.type),
        $('<div>').append(protocol.duration + ' minutes'),
        ...protocol.settings.map(d => {
          let type = d.type ?? '';
          return $('<div>').append(type + ' ' + d.frequency + ' ' + d.unit);
        })
      )
    );
  },

  initDataTable: function($el) {
    let options = {
      ordering: false,
      paging: false,
      searching: false,
      info: false
    };
    let dataTable = new DataTable($el, options);
    return dataTable;
  },

  displayError: function(error) {
    message = error.error || error;
    return Swal.fire({
      icon: "error",
      title: "Oops...",
      text: message
    });
  }    

}