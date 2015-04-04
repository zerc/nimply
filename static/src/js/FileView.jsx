var React = require('react'),
    qwest = require('qwest'),
    _ = require('underscore'),
    CommentForm = React.createClass({
        contextTypes: {
            router: React.PropTypes.func
        },

        render: function () {
            return (
                <div className="comment_add_form">
                    <form>
                        <div className="row">
                            <input type="text" name="author" placeholder="name" />
                        </div>
                        <div className="row">
                            <textarea name="message" placeholder="message"></textarea>
                        </div>
                        <div className="row">
                            <div className="six columns">
                                <button role="close" className="second_button">Cancel</button>
                            </div>
                            <div className="six columns">
                                <button role="submit" className="primary_button pull_right">Post</button>
                            </div>
                        </div>
                    </form>
                </div>
            )
        }
    }),

    LineView = React.createClass({
        contextTypes: {
            router: React.PropTypes.func
        },
        getInitialState: function() {
            return {show_form: false};
        },
        toggleForm: function (event) {
            this.setState({show_form: !this.state.show_form});
        },

        formIsVisible: function () {
            return this.state.show_form;
        },

        render: function () {
            var form = this.state.show_form ? <CommentForm /> : null;

            return (
                <div>
                    <span onClick={this.toggleForm}>{this.props['data-line']}</span>
                    <span dangerouslySetInnerHTML={{__html: this.props['data-code'] }}></span>
                    {form}
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
            {_.map(this.state.data.code, function (code, line) {
                return <LineView data-code={code} data-line={line} />
            })}
            </pre>);
        }
        return (<span></span>);
      }
    });


module.exports = FileView;
