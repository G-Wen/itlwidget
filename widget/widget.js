'use strict';
// Change this to be the same as your ITL entrant id
const entrant_id = 1;

// Use this to override the name that displays on the widget
// Useful if your ITL/GS name is over 11 characters
const override_name = "";

// Use this to override the avatar source
// Useful if you want to use a non-png file as an avatar
const avatar_source = "";

const endpoint = "http://40.113.237.101:8080/entrant/";

const e = React.createElement;
const default_state = {"id":"--","name":"--","ranking_points":"--","total_points":"--","song_points":"--","bonus_points":"--","passes":"---","full_combos":"--","full_excellent_combos":"--","quad_stars":"--","quint_stars":"-","rival1":null,"rival2":null,"rival3":null,"rank":"---","ladder":[]};
// const test_state = {"id":16,"name":"TommyLongName","ranking_points":179793,"total_points":2008157,"song_points":198157,"bonus_points":2000,"passes":144,"full_combos":12,"full_excellent_combos":4,"quad_stars":0,"quint_stars":0,"rival1":"BrotherMojo","rival2":"Zankoku","rival3":null,"rank":92,"ladder":[{"rank":43,"name":"Zankoku","ranking_points":240328,"is_rival":true,"is_entrant":false,"type":"rival","difference":-60535},{"rank":54,"name":"BrotherMojo","ranking_points":228217,"is_rival":true,"is_entrant":false,"type":"rival","difference":-48424},{"rank":90,"name":"Darkuo","ranking_points":181679,"is_rival":false,"is_entrant":false,"type":"neutral","difference":-1886},{"rank":91,"name":"BSENSS6","ranking_points":180422,"is_rival":false,"is_entrant":false,"type":"neutral","difference":-629},{"rank":92,"name":"GWen","ranking_points":179793,"is_rival":false,"is_entrant":true,"type":"self","difference":0},{"rank":93,"name":"centripital","ranking_points":179490,"is_rival":false,"is_entrant":false,"type":"neutral","difference":303}]}

class ITLWidget extends React.Component {
  constructor(props) {
    super(props);
    this.state = default_state;
    // this.state = test_state;
  }

  componentDidMount() {
    get_info.bind(this)();
    this.interval = setInterval(get_info.bind(this), 150*1000);
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
        e('div', null, "Rank: " + this.state.rank),
      ),
      e('div', {className: "entrant_points"}, 
        e('div', null, "RP:"),
        e('div', null, ""),
        e('div', null, this.state.ranking_points),
      ),
      e('div', {className: "entrant_points"}, 
        e('div', null, "TP:"),
        e('div', null, ""),
        e('div', null, this.state.total_points),
      ),
    )

    var song_info = e('div', {className: "clear_info"}, 
      e('div', {className: "passes"},
        e('div', null, "Passes:"),
        e('div', null, this.state.passes)
      ),
      e('div', {className: "fcs"},
        e('div', null, "FCs:"),
        e('div', null, this.state.full_combos)
      ),
      e('div', {className: "fecs"},
        e('div', null, "FECs:"),
        e('div', null, this.state.full_excellent_combos)
      ),
      e('div', {className: "quads"},
        e('div', null, "Quads:"),
        e('div', null, this.state.quad_stars)
      ),
      e('div', {className: "quints"},
        e('div', null, "Quints:"),
        e('div', null, this.state.quint_stars)
      ),
    )

    var ladder_entries = this.state.ladder.map((item, index) =>
      e('div', {'key': index, className: item.type}, 
        e('div', {className: "ladder_rank"}, item.rank + ". " + item.name),
        e('div', {}, format_difference(item.difference))
      )
    );

    var ladder = e('div', {className: "ladder"}, 
      e('div', {className: "ladder_title"}, "ITL Ladder"),
      ladder_entries
    );

    return e('div', {className: "wrapper"}, 
      e('div', null, e('img', {src: (avatar_source == "" ? "Avatar.png" : avatar_source), width: "100px", height: "100px"}, null)),
      entrant_info, 
      song_info,
      ladder
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
