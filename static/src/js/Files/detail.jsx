/*
 * All about file detail
 */
var L = require('../Libs.js'),
    React = L.React,
    API_URLS = require('../Urls.js'),
    CommentsBlock = require('../Comments.jsx'),

    LineView = React.createClass({
        getInitialState: function() {
            return {show_form: false};
        },
        toggleForm: function (event) {
            this.setState({show_form: !this.state.show_form});
        },

        element: function () {
            return this.getDOMNode()
        },

        render: function () {
            var row_cls_name = (!L._.isEmpty(this.props['data-comments']) || this.state.show_form ) ? 'have_comments' : '';

            return (
                <tr className={row_cls_name} id={this.props.id}>
                    <td className="highlight__linenum"
                        onClick={this.toggleForm}
                        data-linenum={this.props['data-line']}>
                    </td>
                    <td className="highlight__code">
                        <span dangerouslySetInnerHTML={{__html: this.props['data-code'] }}></span>
                        <CommentsBlock
                            comments={this.props['data-comments']}
                            showform={this.state.show_form}
                            formcontrol={this.toggleForm}
                            line={this.props['data-line']} />
                     </td>
                </tr>
            );
        }
    }),

    FileDetailView = React.createClass({
        contextTypes: {
            router: React.PropTypes.func
        },
        getInitialState: function() {
            return {};
        },
        getFileId: function () {
            if (this.context.router.getCurrentParams().uuid) {
                return this.context.router.getCurrentParams().uuid;
            }
        },
        loadFile: function() {
            var self = this,
                uuid = self.getFileId();

            L.request.get(
                API_URLS.file_detail(uuid),
                null,
                {responseType: 'json'}
            ).then(function (data) {
                self.setState({data: data});
            });
        },

        componentDidUpdate: function () {
            console.log('rendered');
        },

        render: function () {
            var self = this;

            self.lines = [];

            if (this.getFileId() && L._.isEmpty(this.state)) {
                this.loadFile();
            }

            if (this.state.data) {
                return (
                    <table className="highlight"><tbody>
                    {L._.map(this.state.data.code, function (line, i) {
                        var line_view = <LineView
                            key={'line-'+i}
                            id={'line-'+i}
                            data-code={line.code}
                            data-line={line.line}
                            data-comments={line.comments} />

                        if (line.comments.length > 0) {
                            self.lines.push(line_view);
                        }

                        return line_view;
                    })}
                    </tbody></table>);
            }
            return null;
        }
    });


module.exports = FileDetailView;
