/*
 * All about file listing
 */
var L = require('../Libs.js'),
    API_URLS = require('../Urls.js'),
    React = L.React,

    FileListView = React.createClass({
        contextTypes: {
            router: React.PropTypes.func
        },

        getInitialState: function() {
            return {'files': []};
        },

        componentWillMount: function () {
            this.loadData();
        },

        loadData: function () {
            var self = this;

            L.request.get(
                API_URLS.FILES_BASE,
                null,
                {responseType: 'json'}
            ).then(function (data) {
                self.setState({files: data});
            });
        },

        render: function () {
            var self = this,
                files = this.state.files;

            return (<ul className="files_list">
                <li className="files_list__title">
                    <h5>Public reviews</h5>
                </li>
                {L._.map(files, function (fobj) {
                    var href = self.context.router.makeHref('fileview', {'uuid': fobj.uuid});
                    return (
                        <li className="files_list__item">
                            <span className="files_list__item__comments" title="comments count">
                                {fobj.comments || 0}
                            </span>
                            <a href={href}>{fobj.name}</a>
                        </li>);
                })}
                </ul>);
        }
    });


module.exports = FileListView;
