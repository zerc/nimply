/*
 * Module for works with files.
 */
var L = require('./Libs.js'),
    React = L.React,
    API_URLS = require('./Urls.js'),
    CommentsBlock = require('./Comments.jsx'),

    LineView = React.createClass({
        getInitialState: function() {
            return {show_form: false};
        },
        toggleForm: function (event) {
            this.setState({show_form: !this.state.show_form});
        },

        render: function () {
            var row_cls_name = !L._.isEmpty(this.props['data-comments']) ? 'have_comments' : '';

            return (
                <tr className={row_cls_name}>
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

    FileView = React.createClass({
      contextTypes: {
        router: React.PropTypes.func
      },
      getInitialState: function() {
        return {};
      },
      getFileId: function () {
        if (this.context.router.getCurrentParams().fname) {
          return this.context.router.getCurrentParams().fname;
        }
      },
      loadFile: function() {
        var self = this,
            fname = self.getFileId();

        L.request.get(
            API_URLS.file_detail(fname),
            null,
            {responseType: 'json'}
        ).then(function (data) {
            self.setState({data: data});
        });
      },

      render: function () {
        if (this.getFileId() && L._.isEmpty(this.state)) {
          this.loadFile();
        }

        if (this.state.data) {
          return (
            <table className="highlight"><tbody>
            {L._.map(this.state.data.code, function (line) {
                return <LineView
                    data-code={line.code}
                    data-line={line.line}
                    data-comments={line.comments} />
            })}
            </tbody></table>);
        }
        return null;
      }
    });


module.exports = FileView;
