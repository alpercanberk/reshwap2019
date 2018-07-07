import React, { Component } from "react";

import Thumbnail from "../components/thumbnail.js";

import axios from "axios";

import { Form, InputGroup, FormControl } from "react-bootstrap";

let Departments = [
  "All",
  "English",
  "Math",
  "History",
  "Science",
  "Music",
  "Visual Arts",
  "Theater",
  "Religion",
  "Chinese",
  "Spanish",
  "French",
  "Latin",
  "Other"
];

class Books extends Component {
  constructor() {
    super();
    this.state = {
      dep_value: "All",
      data: [],
      search: ""
    };
    this.handleDepChange = this.handleDepChange.bind(this);
    this.handleSearchChange = this.handleSearchChange.bind(this);
  }

  componentWillMount() {
    axios.get(window.CURRENT_HOST + "items?category=Books").then(res => {
      this.setState({ data: res.data });
      console.log(this.state.data);
    });
  }

  handleDepChange(event) {
    this.setState({ dep_value: event.target.value });
    console.log(event.target.value);
  }

  handleSearchChange(event) {
    this.setState({ search: event.target.value });
    console.log(event.target.value);
  }

  render() {
    return (
      <div>
        <h3 className="bold" style={{ textAlign: "center" }}>
          Books
        </h3>

        <div style={{ width: "95%", margin: "5px auto" }} className="row">
          <select
            className="category-select col-xs-4"
            onChange={this.handleDepChange}
            value={this.state.dep_value}
          >
            {Departments.map(department => {
              return <option key={department}>{department}</option>;
            })}
          </select>
          <Form
            className="col-xs-8"
            style={{ paddingRight: "2px", paddingLeft: "6px" }}
          >
            <InputGroup>
              <InputGroup.Addon>🔎</InputGroup.Addon>
              <FormControl
                type="text"
                onChange={this.handleSearchChange}
                value={this.state.search}
              />
            </InputGroup>
          </Form>
        </div>
        {this.state.data.map(item_data => {
          if (
            this.state.search == "" ||
            item_data.title
              .toLowerCase()
              .includes(this.state.search.toLowerCase())
          ) {
            if (this.state.dep_value == "All") {
              return <Thumbnail data={item_data} />;
            } else if (this.state.dep_value == item_data.department) {
              return <Thumbnail data={item_data} />;
            }
          }
        })}
      </div>
    );
  }
}

export default Books;
