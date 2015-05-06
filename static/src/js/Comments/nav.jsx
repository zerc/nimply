/*
 * Navigation over affected lines by comments
 */
var L = require('../Libs.js'),
    React = L.React,
    SignalsBus = L.SignalsBus,
    API_URLS = require('../Urls.js'),

    NavPanel = React.createClass({
        componentDidMount: function () {
            var self = this;

            SignalsBus.commentAdded.add(function (comment, line_id) {
                self.state.lines.push(line_id);
                self.setState({lines_count: self.state.lines_count + 1});
            });

            window.onscroll = function () {
                // Very dirty - 46 its is HEADER height
                if (window.scrollY > 46) {
                    self.setState({'css_class': 'nav_panel_block-fixed'});
                } else {
                    self.setState({'css_class': 'nav_panel_block'});
                }
            }
        },

        getInitialState: function() {
            var lines = this.props['data-comments-lines'] || [],
                line = L._.isEmpty(lines) ? null : 0,
                lines_count = lines.length;

            return {'lines': lines,
                    'current_line': line,
                    'lines_count': lines_count,
                    'css_class': 'nav_panel_block'}
        },

        _prepare_comment_line: function () {
            if (L._.isNull(this.state.current_line)) {
                return null;
            }

            var line = this.state.current_line,
                val = this.state.lines[line],
                el = document.getElementById(val);

            el.scrollIntoViewIfNeeded();

            return el;
        },

        next_comment_line: function () {
            var el = this._prepare_comment_line(),
                line;

            if (!L._.isNull(el)) {
                if (this.state.current_line === this.state.lines_count - 1) {
                    line = 0;
                } else {
                    line = this.state.current_line + 1;
                }
                this.setState({current_line: line});
            }
        },

        prev_comment_line: function () {
            var el = this._prepare_comment_line(),
                line;

            if (!L._.isNull(el)) {
                if (this.state.current_line === 0) {
                    line = this.state.lines_count - 1;
                } else {
                    line = this.state.current_line - 1;
                }
                this.setState({current_line: line});
            }
        },

        current_line_display: function () {
            if (L._.isNull(this.state.current_line) || this.state.current_line > 0) {
                return (<i className="fa fa-paperclip fa-2x nav_panel_block__comment_count">
                        {this.state.lines_count}
                    </i>);
            }

            if (this.state.current_line === 0) {
                return (
                    <i className="fa fa-paperclip fa-2x nav_panel_block__comment_count">
                        {this.state.lines_count}
                        <span className="nav_panel_block__delimetr">/</span>
                        <span className="nav_panel_block__current_line">
                            {this.state.current_line+1}
                        </span>
                    </i>);
            }
        },

        line_is_visble: function (line) {
            var line_id = this.state.lines[line],
                el = document.getElementById(line_id),
                current_scroll = window.scrollY;
            return (el.offsetTop <= current_scroll && current_scroll <= (el.offsetTop + el.offsetHeight));
        },

        render: function () {
            var current_line = this.current_line_display();
            return (
                <div className={this.state.css_class}>
                    <i className="fa fa-angle-double-down fa-2x nav_panel_block__next_comment"
                       onClick={this.next_comment_line}
                       title="Next line with comments"></i>

                    <span className="nav_panel__filename">{this.props['data-filename']}</span>

                    <i className="fa fa-angle-double-up fa-2x nav_panel_block__prev_comment"
                       onClick={this.prev_comment_line}
                       title="Prev line with comments"></i>
                </div>
            );
        }
    });

module.exports = NavPanel;
