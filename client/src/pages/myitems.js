import React, { Component } from "react";

import axios from "axios";

import Thumbnail from "../components/thumbnail.js";

import { Form, InputGroup, FormControl } from "react-bootstrap";

class MyItems extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      search: ""
    };
    this.handleSearchChange = this.handleSearchChange.bind(this);
    this.complete = this.complete.bind(this);
  }

  componentWillMount() {
    console.log("test!");
    console.log(window.currentUser);
    var item = "items/i";
    if (window.currentUser == "acanberk21@lawrenceville.org") {
      item = "allitems";
      console.log("welcome, master!");
    }
    axios.get(window.CURRENT_HOST + item).then(res => {
      this.setState({ data: res.data });
      console.log(this.state.data);
    });
  }

  handleSearchChange(event) {
    this.setState({ search: event.target.value });
    console.log(event.target.value);
  }

  complete() {
    this.forceUpdate();
    this.setState();
  }

  display() {
    console.log(this.state.data);
    console.log(this.state.data.length);
    if (this.state.data.length != 0) {
      console.log("There's data!");
      this.state.data.map(item_data => {
        if (
          this.state.search == "" ||
          item_data.title
            .toLowerCase()
            .includes(this.state.search.toLowerCase())
        ) {
          console.log("displaying..");

          // return <Thumbnail data={item_data} deleteFunc={this.complete} />;
          // THIS PART FIXED ITSELF FOR SOME REASON
        }
      });
    } else {
      return (
        <div className="empty-page">
          <div className="empty-page-text">
            Nope, you don't have a single upload on Reshwap.
          </div>
        </div>
      );
    }
  }

  render() {
    return (
      <div>
        <h3 className="bold" style={{ textAlign: "center" }}>
          My Items
        </h3>
        <Form style={{ width: "95%", margin: "10px auto" }}>
          <InputGroup>
            <InputGroup.Addon>🔎</InputGroup.Addon>
            <FormControl
              type="text"
              onChange={this.handleSearchChange}
              value={this.state.search}
            />
          </InputGroup>
        </Form>
        <div>
          {this.state.data.map(item_data => {
            if (
              this.state.search == "" ||
              item_data.title
                .toLowerCase()
                .includes(this.state.search.toLowerCase())
            ) {
              return <Thumbnail data={item_data} deleteFunc={this.complete} />;
            }
          })}
          {this.display()}
        </div>
      </div>
    );
  }
}

export default MyItems;
