var L = require('../Libs.js'),
    React = L.React,
    SignalsBus = L.SignalsBus,
    API_URLS = require('../Urls.js'),

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

module.exports = CommentForm;
