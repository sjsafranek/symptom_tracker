

  class App {
    constructor(client_id) {
      this._clientID = client_id;
    
      this.elements = {
        $protocolContainer: $('#protocol-container'),
        $trackingTable: $('#tracking'),
        $protocolTable: $('#protocols')
      }
    }

    init() {
      let self = this;
      $('.btn-add-session').on('click', Forms.createClientSession);

      return this;
    }

    _makeSymptomScoreProgressBar(score, session_id, symptom) {
      return UI.makeSymptomScoreProgressBar(score, session_id, symptom, {
        'dblclick': (event) => { 
          Forms.setSessionSymptomScore(session_id, symptom, score); 
        }
      });
    }

    _makeSessionSymptomScoreButton(session_id, symptom) {
      return UI.makeSessionSymptomScoreButton(session_id, symptom, {
        'click': (event) => {
          Forms.setSessionSymptomScore(session_id, symptom);
        }
      });
    }

    _makeProtocolButton(sessionId) {
      let self = this;
      return UI.makeProtocolButton(sessionId, {
        'click':  function(event) {
          self.renderSessionProtocol(event);
        }
      });
    }

    _makeProtocolColumns(session) {
      let self = this;

      var _getProtocolSites = function(type) {
        return session.protocol.filter(d => {return type == d.type}).map(d => { return d.site; });
      }

      return [
        $('<td>').append(_getProtocolSites('ILF')),
        $('<td>').append(_getProtocolSites('AlphaTheta')),
        $('<td>').append(_getProtocolSites('Frequency Band')),
        $('<td>').append(_getProtocolSites('Synchrony')),
        $('<td>').addClass('text-center').append(
          self._makeProtocolButton(session.id)
        )
      ];
    }

    buildDataset(results) {
      let dataset = {
        symptoms: {},
        baselines: {
          'good': {
            number: null,
            date: 'Baseline: Good Week',
            scores: {}
          },
          'bad': {
            number: null,
            date: 'Baseline: Bad Week',
            scores: {}
          },
          'usual': {
            number: null,
            date: 'Baseline: Usual Week',
            scores: {}
          }
        },
        sessions: {}
      };
      
      let symptoms = results[0];
      for (let i=0; i<symptoms.length; i++) {
        let symptom = symptoms[i];
        dataset.symptoms[symptom.name] = symptom;
        dataset.baselines.good.scores[symptom.name] = symptom.baseline.goodweek;
        dataset.baselines.bad.scores[symptom.name] = symptom.baseline.badweek;
        dataset.baselines.usual.scores[symptom.name] = symptom.baseline.usualweek;
      }

      // 
      let sessions = results[1];
      dataset.sessions = Object.fromEntries(
        sessions.filter(d => !d.no_show)
                .map(session => {
                  // format scores for easier lookup
                  session.scores = Object.fromEntries(session.symptom_scores.map(symptom => [symptom.name, symptom.score]));

                  // This allows for alphanumeric sorting 
                  // and handles multiple sessions on the same day
                  let key = `${session.date}_${session.id}`;  
                  return [key, session];
                })
      );

      return dataset;
    }

    renderSessionProtocol(event) {
      let self = this;
      let session_id = $(event.target).data()['sessionId'];
      Api.fetchSessionProtocol(session_id)
        .then((protocol) => {
          self.elements.$protocolContainer.empty()
            .append(
              protocol.map(UI.makeProtocolCard)
            );
        });
    }

    renderTrackingTable(dataset) {

      let self = this;

      let symptomsNames = Object.values(dataset.symptoms).filter(d => d.is_active).map(d => d.name);

      var _getSymptomByName = function(name) {
        return Object.values(dataset.symptoms).filter(d => d.name == name)[0];
      }

      let $headers = $('<tr>').append(
        $('<th>').append('date'),
        $('<th>').addClass('text-center').append('number'),
        ...symptomsNames.map(name => {
          return $('<th>').addClass('column-symptom')
                          .append(name)
                          .on('contextmenu', (event) => { 
                            event.preventDefault();
                            Forms.disableSymptom(_getSymptomByName(name));
                          });
        })
      )

      this.elements.$trackingTable.append(
        $('<thead>').append($headers),
        $('<tbody>').append(
          (function() {
            let rows = [];

            rows.push(
              $('<tr>').addClass('table-secondary').append(
                $('<td>').append('Good Week'),
                $('<td>').append(''),
                ...symptomsNames.map(d => {
                  let icon = self._makeSymptomScoreProgressBar(dataset.baselines.good.scores[d]);
                  return $('<td>').append(icon);
                })
              )
            );

            rows.push(
              $('<tr>').addClass('table-secondary').append(
                $('<td>').append('Bad Week'),
                $('<td>').append(''),
                ...symptomsNames.map(d => {
                  let icon = self._makeSymptomScoreProgressBar(dataset.baselines.bad.scores[d]);
                  return $('<td>').append(icon);
                })
              )
            );

            rows.push(
              $('<tr>').addClass('table-secondary').append(
                $('<td>').append('Usual Week'),
                $('<td>').append(''),
                ...symptomsNames.map(d => {
                  let icon = self._makeSymptomScoreProgressBar(dataset.baselines.usual.scores[d]);
                  return $('<td>').append(icon);
                })
              )
            );

            for (let key in dataset.sessions) {
              let session = dataset.sessions[key];

              let has_scores = 0 != Object.values(session.scores).filter(d => d).length;
              rows.push(
                $('<tr>').attr('session-id', session.id).append(
                  $('<td>').append(
                    session.date

                    // TODO !has_scores ? mark as no show
                  ),
                  $('<td>').addClass('text-center').append(session.number),
                  ...symptomsNames.map(d => {
                    let icon = self._makeSymptomScoreProgressBar(session.scores[d], session.id, dataset.symptoms[d]) ?? 
                               self._makeSessionSymptomScoreButton(session.id, dataset.symptoms[d]);
                    return $('<td>').append(icon);
                  })
                )
              );
            }

            // rows.push();
            // todo button to create session

            return rows;
          })()
        )
      );

      UI.initDataTable(this.elements.$trackingTable);
    }

    renderProtocolTable(dataset) {
      let self = this;
      this.elements.$protocolTable.find('tbody').append(
        (function(){
          let rows = []
          for (let session_key in dataset.sessions) {
            rows.push(
              $('<tr>').attr('session-id', dataset.sessions[session_key].id).append(
                ...self._makeProtocolColumns(dataset.sessions[session_key])
              )
            );
          }
          return rows;
        })()
      );
      UI.initDataTable(this.elements.$protocolTable);
    }

    renderTableCanvas() {
      //.BEGIN
      let $canvas = $('<canvas id="canvas"></canvas>');
      let canvas = $canvas.get(0);
      let ctx = canvas.getContext("2d");

      function resizeCanvas() {
          // Set canvas dimensions to match the window's inner dimensions
          canvas.width = window.innerWidth;
          canvas.height = window.innerHeight;

          // Optional: Handle high-resolution screens (Retina displays)
          const dpr = window.devicePixelRatio || 1;
          canvas.width = window.innerWidth * dpr;
          canvas.height = window.innerHeight * dpr;
          ctx.scale(dpr, dpr);

          // Redraw your canvas content here after resizing
          // For example: drawContent();
      }

      // Call the resize function initially to set the canvas size on load
      resizeCanvas();

      // Add an event listener to dynamically adjust canvas size on window resize
      window.addEventListener('resize', resizeCanvas);

      $('body').prepend($canvas);
      //.END


      // attach listeners
      $('tr').on('mouseenter', function(event) {
        let $el = $(this);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        $('tr').removeClass('highlight')
        let sessionId = $el.attr('session-id');
        if (sessionId) {
          $(`tr[session-id="${sessionId}"]`).addClass('highlight');

          // Draw indicator on canvas
          let left = $(`#tracking tr[session-id="${sessionId}"]`).get(0).getBoundingClientRect();
          let right = $(`#protocols tr[session-id="${sessionId}"]`).get(0).getBoundingClientRect();
          ctx.beginPath();
          ctx.strokeStyle = "#e2e3e5";
          ctx.lineWidth = 3;
          ctx.moveTo(left.right, left.top);
          ctx.lineTo(right.left, right.top);
          ctx.lineTo(right.left, right.bottom);
          ctx.lineTo(left.right, left.bottom);     
          ctx.closePath(); // Close the triangle
          ctx.fillStyle = "#e2e3e5";
          ctx.fill(); // Fill the triangle
        }
      });

      $('table').on('mouseleave', function(event) {
        $('tr').removeClass('highlight');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      });
    }

    render() {
      let self = this;
      return Promise.all([
        Api.fetchSymptomsByClient(this._clientID),
        Api.fetchSessionsByClient(this._clientID)
      ])
      .then(self.buildDataset)
      .then((dataset) => {
        return Promise.all([
          self.renderTrackingTable(dataset),
          self.renderProtocolTable(dataset)
        ]);
      })
      .then(self.renderTableCanvas);
    }

  };