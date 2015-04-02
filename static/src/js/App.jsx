var React = require('react'),
    _ = require('underscore'),
    Box = React.createClass({
      getChilds: function () {
        var self = this;
        return _.map(window.VARIANTS, function(f) {
          return React.createElement(f.call(self, React, _), null);
        });
      },

      render: function () {
        var childs = this.getChilds();
        return (
          React.createElement(
            'div', {'class': 'container'}, childs)
        );
      }
    });

module.exports = Box;

React.render(<Box />, document.getElementById('content'));
