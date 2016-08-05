'use strict';

var DashboardApp = React.createClass({
  _timer_render: null,
  _start: 0,
  _display_msg: '',


  getInitialState: function() {
    var self = this;

    self._start_render_timer();

    return {};
  },

  _start_render_timer: function(){
    var self = this;

    self._timer_render = setTimeout($.proxy(function(){
      self._refresh_camera_state();
    }, self), 1000);
  },

  _refresh_camera_state: function(){
    var self = this;

    $.ajax({
      url: '/api/camera',
      data: null,
      success: $.proxy(self._callback_success, self),
      error: $.proxy(self._callback_error, self)
    });
  },

  render: function() {
    var self = this;

    return React.DOM.p(null, self._display_msg);
  },

  _callback_success: function(data){
    var self = this;

    console.log( 'GOT A RESPONSE.' );
    console.log( data );

    self._display_msg = 'Bot status: ' + data.toString();

    self.forceUpdate();
    self._start_render_timer();
  },

  _callback_error: function(){
    console.log( 'ERROR in camera state retrieve.' );
  }
});

var DashboardAppFactory = React.createFactory(DashboardApp);
var start = new Date().getTime();


$(document).ready(function(){
  ReactDOM.render(
    DashboardAppFactory(),
    document.getElementById('container')
  );
});
