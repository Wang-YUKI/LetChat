import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import './App.css';

import HomePage from './pages/HomePage';
import ChannelPage from './pages/ChannelPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import ResetPasswordPage from './pages/ResetPasswordPage';
import ProfilePage from './pages/ProfilePage';
import ProtectedRoute from './components/Layout/ProtectedRoute';

import { AuthProvider } from './AuthContext';

function App() {
  const [authDetails, setAuthDetails] = React.useState(
    localStorage.getItem('token')
  );

  function setAuth(token) {
    localStorage.setItem('token', token);
    setAuthDetails(token);
  }
  return (
    <AuthProvider value={authDetails}>
      <Router>
        <Switch>
          <Route
            exact
            path="/login"
            render={(props) => {
              return <LoginPage {...props} setAuth={setAuth} />;
            }}
          />
          <Route
            exact
            path="/register"
            render={(props) => {
              return <RegisterPage {...props} setAuth={setAuth} />;
            }}
          />
          <Route exact path="/forgot_password" component={ForgotPasswordPage} />
          <Route exact path="/reset_password" component={ResetPasswordPage} />
          <ProtectedRoute exact path="/" component={HomePage} />
          <ProtectedRoute path="/profile/:profile" component={ProfilePage} />
          <ProtectedRoute path="/channel/:channel_id" component={ChannelPage} />
        </Switch>
      </Router>
    </AuthProvider>
  );
}

export default App;
