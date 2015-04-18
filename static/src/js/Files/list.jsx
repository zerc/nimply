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

            return (
                <div className="varinat_block">
                    <h4>{'Select exists file for review:'}</h4>
                    <ol>
                    {L._.map(files, function (fobj) {
                        var href = self.context.router.makeHref('fileview', {'uuid': fobj.uuid});
                        return (<li><a href={href}>{fobj.name}</a></li>);
                    })}
                    </ol></div>);
        }
    });


module.exports = FileListView;
