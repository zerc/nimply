/*
 * Module for work with comments.
 */
var L = require('./Libs.js'),
    React = L.React,
    API_URLS = require('./Urls.js'),

    Comment = React.createClass({
        render: function () {
            return (
                <div className="comments__block">
                    <div className="comments__block__header">
                        <span className="comments__block__header__author">
                            {this.props.author}
                        </span>
                        <span className="comments__block__header__date">
                            {this.props.date}
                        </span>
                    </div>
                    <div className="comments__block__message">
                        {this.props.message}
                    </div>
                </div>
            );
        }
    }),

    CommentsList = React.createClass({
        getInitialState: function() {
            return {comments: this.props.comments || []};
        },

        appendComment: function (comment) {
            this.state.comments.unshift(comment);
            this.forceUpdate();
        },

        render: function () {
            var form = null,
                comments = this.state.comments || [];

            if (this.props.showform) {
                form = <CommentForm formcontrol={this.props.formcontrol}
                                    line={this.props.line}
                                    callback={this.appendComment} />;
            }

            return (
                <div className="comments">
                    {L._.map(comments, function (comment) {
                        return <Comment
                            author={comment.author}
                            date={comment.date}
                            message={comment.message} />
                    })}
                    {form}
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
                uuid = this.context.router.getCurrentParams().uuid,
                form_data = {line: this.props.line,};

            if (!author || !message) {
                return false;
            }

            form_data['message'] = message;
            form_data['author'] = author;

            L.request
                .post(API_URLS.comments_add(uuid),
                      form_data,
                      {responseType: 'json'})
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
                        <div>
                            <div className="six columns">&nbsp;</div>
                            <div className="six columns">
                                <button className="second_button" onClick={this.hideForm}>Cancel</button>
                                <button className="primary_button pull_right" onClick={this.postForm}>Post</button>
                            </div>
                        </div>
                    </div>
                </div>
            )
        }
    });


module.exports = CommentsList;
