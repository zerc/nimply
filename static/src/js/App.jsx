var L = require('./Libs.js'),
    React = L.React,
    RouteHandler = L.Router.RouteHandler,
    Route = L.Router.Route,
    DefaultRoute = L.Router.DefaultRoute,

    Files = require('./Files/init.js'),
    FileDetailView = Files.FileDetailView,
    FileListView = Files.FileListView,
    FileUploadView = Files.FileUploadView,

    App = React.createClass({
        render: function () {
          return (
            <div>
              <RouteHandler/>
            </div>
          );
        }
    }),

    IndexPageView = React.createClass({
        render: function () {
            return (
                <div>
                    <FileListView />
                    <FileUploadView />
                </div>
            );
        }
    });

    ROUTES = (
        <Route name="app" path="/" handler={App}>
            <Route name="fileview" path="/file/?:uuid?" handler={FileDetailView} />
            <DefaultRoute handler={IndexPageView} />
        </Route>
    );

L.Router.run(ROUTES, function (Handler, state) {
    React.render(<Handler />, document.getElementById('content'));
});
