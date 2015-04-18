/*
 * File upload
 */
var L = require('../Libs.js'),
    API_URLS = require('../Urls.js'),
    React = L.React,

    FileUploadView = React.createClass({
        contextTypes: {
            router: React.PropTypes.func
        },

        doUpload: function (event) {
            var files = event.target.files,
                form_data = new FormData(),
                self = this;

            form_data.append('file', files[0]);

            L.request.post(
                API_URLS.FILES_BASE,
                form_data,
                {responseType: 'json'}
            ).then(function (response) {
                self.context.router.transitionTo(
                    'fileview', {'uuid': response.uuid}
                );
            });
        },

        render: function () {
            var self = this;

            return (<div className="varinat_block">
                <h4>{'Upload file:'}</h4>
                <input type="file" name="file" ref="fileInput" onChange={self.doUpload} />
                </div>
            );
        }
    });

module.exports = FileUploadView;
