var React = require('react'),
    qwest = require('qwest'),
    _ = require('underscore'),
    Comment = React.createClass({
        render: function () {
            return (
                <div className="comments__block">
                    <div className="comments__block__header">
                        {this.props.date} / {this.props.author}
                    </div>
                    <div className="comments__block__message">
                        {this.props.message}
                    </div>
                </div>
            );
        }
    }),

    CommentsList = React.createClass({
        render: function () {
            var comments = this.props.comments || [];

            return (
                <div className="comments">
                    {_.map(comments, function (comment) {
                        return <Comment
                            author={comment.author}
                            date={comment.date}
                            message={comment.message} />
                    })}
                </div>
            )
        }
    }),

    CommentForm = React.createClass({
        contextTypes: {
            router: React.PropTypes.func
        },

        hideForm: function () {
            return this.props.formcontrol();
        },

        postForm: function () {
            var self = this,
                author = React.findDOMNode(this.refs.author).value.trim(),
                message = React.findDOMNode(this.refs.message).value.trim(),
                form_data = {
                    line: this.props.line,
                    'filename': this.context.router.getCurrentParams().fname
                };

            if (!author || !message) {
                return false;
            }

            form_data['message'] = message;
            form_data['author'] = author;

            qwest
                .post('/comment/', form_data, {responseType: 'json'})
                .then(function (response) {
                    self.props.callback(response);
                    self.hideForm();
                });
        },

        render: function () {
            return (
                <div className="comment_add_form">
                    <div className="row">
                        <input type="text" name="author" placeholder="name" ref="author"/>
                    </div>
                    <div className="row">
                        <textarea name="message" placeholder="message" ref="message"></textarea>
                    </div>
                    <div className="row">
                        <div className="six columns">
                            <button role="close" className="second_button" onClick={this.hideForm}>Cancel</button>
                        </div>
                        <div className="six columns">
                            <button role="submit" className="primary_button pull_right" onClick={this.postForm}>Post</button>
                        </div>
                    </div>
                </div>
            )
        }
    }),

    CommentsBlock = React.createClass({
        getInitialState: function() {
            return {comments: this.props.comments || []};
        },

        appendComment: function (comment) {
            this.state.comments.push(comment);
            this.forceUpdate();
        },

        render: function () {
            var form = null;

            if (this.props.showform) {
                form = <CommentForm formcontrol={this.props.formcontrol}
                                    line={this.props.line}
                                    callback={this.appendComment} />;
            }

            return (
                <div className="comments">
                    <CommentsList comments={this.state.comments} />
                    {form}
                </div>
            );
        }
    });


module.exports = CommentsBlock;
