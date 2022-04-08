'use strict';
// Change this to be the same as your ITL entrant id
const entrant_id = 18;

// Use this to override the name that displays on the widget
// Useful if your ITL/GS name is over 11 characters
const override_name = "";

const e = React.createElement;
const default_state = {"id":18,"name":"--","ranking_points":"--","total_points":"--","song_points":"--","bonus_points":"--","passes":"---","full_combos":"--","full_excellent_combos":"--","quad_stars":"--","quint_stars":"-","rival1":null,"rival2":null,"rival3":null,"rank":"---","ladder":[]};
const endpoint = "http://40.113.237.101:8080/v2/entrant/"

class ITLWidget extends React.Component {
  constructor(props) {
    super(props);
    this.state = default_state;
  }

  componentDidMount() {
    get_info.bind(this)();
    this.interval = setInterval(get_info.bind(this), 60*1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  render() {
    var entrant_info = e('div', {className: "entrant_info"}, 
      e('div', {className: "entrant_name"}, 
        (override_name == "" ? this.state.name : override_name)
      ),
      e('div', {className: "entrant_id"},
        e('div', null, "ID: " + this.state.id),
      ),
      e('div', {className: "entrant_rank"},
        e('div', null, "Rank " + this.state.rank),
      ),
      e('div', {className: "entrant_points"}, 
        e('div', null, "RP"),
        e('div', null, ""),
        e('div', null, this.state.ranking_points),
      ),
      e('div', {className: "entrant_points"}, 
        e('div', null, "TP"),
        e('div', null, ""),
        e('div', null, this.state.total_points),
      ),
    )

    var song_info = e('div', {className: "clear_info"}, 
       e('div', {className: "passes"},
        e('div', null, "✔"),
        e('div', null, this.state.passes)
      ),
      e('div', {className: "fcs"},
        e('div', null, "FC"),
        e('div', null, this.state.full_combos)
      ),
      e('div', {className: "fecs"},
        e('div', null, "FEC"),
        e('div', null, this.state.full_excellent_combos)
      ),
      e('div', {className: "quads"},
        e('div', null, e('img', {src: "quad.png", width: "24px", height: "24px"}, null)),
        e('div', null, this.state.quad_stars)
      ),
      e('div', {className: "quints"},
        e('div', null, e('img', {src: "quint.png", width: "24px", height: "24px"}, null)),
        e('div', null, this.state.quint_stars)
      ),
    )

    var ladder_entries = this.state.ladder.map((item, index) =>
      e('div', {'key': index, className: item.type}, 
        e('div', {}, item.rank + ". " + item.name),
        e('div', {}, format_difference(item.difference))
      )
    );

    var ladder = e('div', {className: "ladder"}, 
      e('div', null, ""),
      ladder_entries
    );

    return e('div', {className: "wrapper"}, 
      entrant_info, 
      song_info,
      ladder,
    )
  }
}

function get_info() {
  fetch(endpoint + entrant_id)
    .then((response) => {
      if (response.ok) { 
        return response.json();
       }
      return Promise.reject(response); 
    })
    .then((data) => {
      this.setState(data);
    })
    .catch((error) => {
      console.error('Error', error);
    })
}

function format_difference(diff) {
  if (diff == 0) {
    return "--";
  } 
  else if (diff > 0) {
    return "+" + diff;
  }
  else {
    return diff;
  }
}

var domContainer = document.querySelector('.entrant');
ReactDOM.render(React.createElement(ITLWidget), domContainer);