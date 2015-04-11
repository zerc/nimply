var L = require('./Libs.js'),
    React = L.React,
    RouteHandler = L.Router.RouteHandler,
    Route = L.Router.Route,
    DefaultRoute = L.Router.DefaultRoute,

    FileView = require('./FileView.jsx'),
    VariantsView = require('./VariantsView.jsx'),

    App = L.React.createClass({
        render: function () {
          return (
            <div>
              <RouteHandler/>
            </div>
          );
        }
    }),

    ROUTES = (
        <Route name="app" path="/" handler={App}>
            <Route name="fileview" path="/file/?:fname?" handler={FileView} />
            <DefaultRoute handler={VariantsView} />
        </Route>
    );

L.Router.run(ROUTES, function (Handler, state) {
    React.render(<Handler />, document.getElementById('content'));
});
