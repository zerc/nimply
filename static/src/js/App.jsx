var React = require('react'),
    _ = require('underscore'),
    Router = require('react-router'),

    DefaultRoute = Router.DefaultRoute,
    Link = Router.Link,
    Route = Router.Route,
    RouteHandler = Router.RouteHandler,

    FileView = require('./FileView.jsx'),
    VariantsView = require('./VariantsView.jsx'),

    App = React.createClass({
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

Router.run(ROUTES, function (Handler, state) {
    React.render(<Handler />, document.getElementById('content'));
});
