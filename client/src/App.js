import React, { Component } from "react";
import {
  BrowserRouter as Router,
  HashRouter,
  Route,
  Link
} from "react-router-dom";
import { Redirect, IndexRedirect } from "react-router-dom";

// import "./assets/react-toolbox/theme.css";
// import theme from "./assets/react-toolbox/theme.js";
// import ThemeProvider from "react-toolbox/lib/ThemeProvider";

import {
  Nav,
  Navbar,
  NavItem,
  MenuItem,
  NavDropdown,
  Modal,
  Jumbotron
} from "react-bootstrap";

import Books from "./pages/books.js";
import MyItems from "./pages/myitems.js";
import Upload from "./pages/upload.js";

import axios from "axios";

import Display from "./components/display.js";

class App extends Component {
  render() {
    return (
      <div>
        <HashRouter>
          <div className="App">
            <div>
              <Navbar inverse collapseOnSelect id="homenav">
                <Navbar.Header>
                  <Navbar.Brand>
                    <img src={"static/Reshwap Backup Logo 6.svg"} />
                  </Navbar.Brand>
                  <Navbar.Toggle />
                </Navbar.Header>
                <Navbar.Collapse>
                  <Nav className="nav-left">
                    <NavItem eventKey={1} href="/#/books">
                      <Link to="/books" className="navlink">
                        Books
                      </Link>
                    </NavItem>
                    <NavItem eventKey={2}>
                      <Link to="/furniture" className="navlink">
                        Furniture
                      </Link>
                    </NavItem>
                    <NavItem eventKey={2}>
                      <Link to="/electronics" className="navlink">
                        Electronics
                      </Link>
                    </NavItem>
                    <NavItem eventKey={2}>
                      <Link to="/other" className="navlink">
                        Other
                      </Link>
                    </NavItem>
                    <NavItem eventKey={2}>
                      <Link to="/upload" className="navlink">
                        <b>Upload</b>
                      </Link>
                    </NavItem>
                    <NavItem eventKey={2}>
                      <Link to="/myitems" className="navlink">
                        <b>My Items</b>
                      </Link>
                    </NavItem>
                  </Nav>
                  <Nav>
                    <NavItem eventKey={1}>
                      <Link to="/logout" className="navlink logout">
                        Log out
                      </Link>
                    </NavItem>
                  </Nav>
                </Navbar.Collapse>
              </Navbar>
            </div>
            <Route exact path="/" render={() => <Redirect to="/books" />} />
            <Route path="/myitems" component={MyItems} />
            <Route path="/books" component={Books} />
            <Route
              path="/furniture"
              component={() => <Display category="Furniture" />}
            />
            <Route
              path="/electronics"
              component={() => <Display category="Electronics" />}
            />
            <Route
              path="/other"
              component={() => <Display category="Other" />}
            />
            <Route path="/upload" component={Upload} />
            <Route
              path="/logout"
              component={() => {
                axios
                  .get("/logout")
                  .then((window.location = window.CURRENT_HOST));
              }}
            />
          </div>
        </HashRouter>
        <footer className="footer">
          Reshwap 2019 - created by Alper Canberk
        </footer>
      </div>
    );
  }
}

export default App;
