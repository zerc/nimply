/* Common libs includes */
var Signal = require('signals');

module.exports = {
    React: require('react'),
    Router: require('react-router'),

    request: require('qwest'),
    _: require('underscore'),

    SignalsBus: {
        commentAdded: new Signal()
    }
}
