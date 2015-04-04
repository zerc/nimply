var React = require('react'),
    qwest = require('qwest'),
    _ = require('underscore'),
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
          return (
            <div dangerouslySetInnerHTML={{__html: this.state.data.code}}></div>
          );
        }
        return (<span></span>);
      }
    });


module.exports = FileView;
