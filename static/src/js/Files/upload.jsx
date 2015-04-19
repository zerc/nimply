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

        upload: function (file) {
            var self = this,
                form_data = new FormData();

            form_data.append('file', file);

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

        doUpload: function (event) {
            var file = event.target.files[0];

            event.preventDefault();

            if (file) {
                this.upload(file);
            }
        },

        doDrop: function (event) {
            var file = event.dataTransfer.files[0];

            event.preventDefault();

            if (file) {
                this.upload(file);
            }
        },

        preventDefault: function (event) {
            event.preventDefault();
        },

        render: function () {
            var self = this,
                drop_support = !(typeof(window.FileReader) == 'undefined'),
                css_class = 'file_add__upload_area';

            if (!drop_support) {
                css_class = css_class + '-' + 'drop_disabled';
            }

            return (
                <div className="file_add">
                    <h5>Add file using:</h5>
                    <div className={css_class}
                         onDragOver={self.preventDefault}
                         onDrop={self.doDrop}>
                        <div className="file_add__button button button-primary">
                            <span>Upload</span>
                            <input className="file_add__button"
                                   type="file"
                                   name="file"
                                   ref="fileInput"
                                   onChange={self.doUpload} />
                        </div>
                    </div>
                </div>
            );
        }
    });

module.exports = FileUploadView;
