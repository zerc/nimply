var React = require('react'),
    _ = require('underscore'),
    qwest = require('qwest'),
    VariantsView = React.createClass({
      getChilds: function () {
        var self = this;
        return _.map(window.VARIANTS, function(f, key) {
          return React.createElement(f.call(self, React, _, qwest), {'key': key});
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

module.exports = VariantsView;
