React.createClass({
    displayName: "Hello2",
    render: function () {
        var files = {{ variant.files_list|jsonify }};

        return React.createElement('div', {'class': 'varinat_block'},
            React.createElement('h4', null, 'Select exists file for review:'),
            React.createElement('ol', null,
                _.map(files, function (fname) {
                    return React.createElement('li', null,
                        React.createElement('a', {'href': '?filename='+fname}, fname)
                    )
                })
            )
        );
    }
});
