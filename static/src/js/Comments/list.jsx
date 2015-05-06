var L = require('../Libs.js'),
    React = L.React,
    SignalsBus = L.SignalsBus,
    API_URLS = require('../Urls.js'),

    CommentForm = require('./form.jsx'),

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
            SignalsBus.commentAdded.dispatch(comment, 'line-'+this.props.line);
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
    });

module.exports = CommentsList;
