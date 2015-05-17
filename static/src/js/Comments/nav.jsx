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
                if (!self.state.lines_dict[line_id]) {
                    self.state.lines.push(line_id);
                    self.state.lines_dict[line_id] = true;
                    self.setState({'lines_count': self.state.lines_count + 1});
                }
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
                lines_dict = {},
                lines_count = lines.length;

            L._.each(lines, function (line) {
                lines_dict[line] = true; // TODO: store comments count
            });

            return {'lines': lines,
                    'current_line': null,
                    'lines_dict': lines_dict,
                    'lines_count': lines_count,
                    'css_class': 'nav_panel_block'}
        },

        goToLine: function (line) {
            var el = document.getElementById(line);

            if (!L._.isNull(el)) {
                el.scrollIntoViewIfNeeded();
                this.setState({'current_line': line});
            }
        },

        render: function () {
            var self = this,
                summary = L._.map(this.state.lines, function (line) {
                    var go = function () { return self.goToLine(line); },
                        css_class = 'nav_panel__summary__item' + (self.state.current_line === line ? ' nav_panel__summary__item__active': '');

                    return <span
                        className={css_class}
                        onClick={go}>{line}</span>
                });

            return (
                <div className={this.state.css_class}>
                    <span className="nav_panel__filename">{this.props['data-filename']}</span>
                    <span className="nav_panel__filename_triangle"></span>

                    <span className="nav_panel__summary">{summary}</span>
                </div>
            );
        }
    });

module.exports = NavPanel;
