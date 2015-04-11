React.createClass({
    contextTypes: {
        router: React.PropTypes.func
    },
    displayName: "FilesListVariant",

    render: function () {
        var self = this,
            files = {{ variant.files_list|jsonify }};

        return React.createElement('div', {'class': 'varinat_block'},
            React.createElement('h4', null, 'Select exists file for review:'),
            React.createElement('ol', null,
                _.map(files, function (fname) {
                    var href = self.context.router.makeHref('fileview', {'fname': fname});
                    return React.createElement('li', null,
                        React.createElement('a', {'href': href}, fname)
                    )
                })
            )
        );
    }
});
