var React = require('react'),
    qwest = require('qwest'),
    _ = require('underscore'),
    CommentsBlock = require('./Comments.jsx'),

    LineView = React.createClass({
        getInitialState: function() {
            return {show_form: false};
        },
        toggleForm: function (event) {
            this.setState({show_form: !this.state.show_form});
        },

        render: function () {
            return (
                <div>
                    <span onClick={this.toggleForm}>{this.props['data-line']}</span>
                    <span dangerouslySetInnerHTML={{__html: this.props['data-code'] }}></span>
                    <CommentsBlock
                        comments={this.props['data-comments']}
                        showform={this.state.show_form}
                        formcontrol={this.toggleForm}
                        line={this.props['data-line']} />
                </div>
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

        qwest.get(
            '/api/media/'+fname,
            null,
            {responseType: 'json'}
        ).then(function (data) {
            self.setState({data: data});
        });
      },

      render: function () {
        if (this.getFileId() && _.isEmpty(this.state)) {
          this.loadFile();
        }

        if (this.state.data) {
          return (<pre className="highlight">
            {_.map(this.state.data.code, function (line) {
                return <LineView
                    data-code={line.code}
                    data-line={line.line}
                    data-comments={line.comments} />
            })}
            </pre>);
        }
        return (<span></span>);
      }
    });


module.exports = FileView;
