React.createClass({
    displayName: "Hello",
    render: function () {
        return React.createElement(
            'div', {'class': 'hello_world'}, 'Hello World');
    }
});
