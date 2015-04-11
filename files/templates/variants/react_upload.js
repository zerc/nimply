React.createClass({
    contextTypes: {
        router: React.PropTypes.func
    },
    displayName: "UploadReactVariant",

    doUpload: function (event) {
        var files = event.target.files,
            form_data = new FormData(),
            self = this;

        form_data.append('file', files[0]);

        qwest.post('/api/upload/', form_data, {responseType: 'json'})
            .then(function (response) {
              self.context.router.transitionTo(
                'fileview', {'fname': response.filename});
        });
    },

    render: function () {
        var self = this;

        return React.createElement('div', {'class': 'varinat_block'},
            React.createElement('h4', null, 'Upload file:'),
            React.createElement('input', {'type': 'file', 'name': 'file', 'ref': 'fileInput', 'onChange': self.doUpload})
        );
    }
});
