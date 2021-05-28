import React, { Component } from "react";

import axios from "axios";

import Thumbnail from "./thumbnail.js";

import { Form, InputGroup, FormControl } from "react-bootstrap";

class Display extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      search: ""
    };
    this.handleSearchChange = this.handleSearchChange.bind(this);
  }

  componentWillMount() {
    axios
      .get(window.CURRENT_HOST + "items?category=" + this.props.category)
      .then(res => {
        this.setState({ data: res.data });
        console.log(this.state.data);
      });
  }

  handleSearchChange(event) {
    this.setState({ search: event.target.value });
    console.log(event.target.value);
  }

  display() {
    if (this.state.data.length != 0) {
      console.log("there are uploads")
      this.state.data.map(item_data => {
        if (
          this.state.search == "" ||
          item_data.title
            .toLowerCase()
            .includes(this.state.search.toLowerCase())
        ) {
          console.log(item_data.title);
          // return <Thumbnail data={item_data} />;
          // return (<div>Hello 1</div>);
        }
        return "Hello";
      });
    } else {
      console.log("no uploads on this page yet")
      return (
        <div className="empty-page">
          <div className="empty-page-text">
            Sorry, no uploads on this page yet.
          </div>
        </div>
      );
    }

    <div>{(()=>{
      if (this.state.data.length != 0) {
        console.log("there are uploads")
        this.state.data.map(item_data => {
          if (
            this.state.search == "" ||
            item_data.title
              .toLowerCase()
              .includes(this.state.search.toLowerCase())
          ) {
            console.log(item_data.title);
            // return <Thumbnail data={item_data} />;
            // return (<div>Hello 1</div>);
          }
          return "Hello";
        });
      } else {
        console.log("no uploads on this page yet")
        return (
          <div className="empty-page">
            <div className="empty-page-text">
              Sorry, no uploads on this page yet.
            </div>
          </div>
        );
      }
    })()}
    </div>
  }

  render() {
    // console.log(">>>>>", this.display());
    return (
      <div>
        <h3 className="bold" style={{ textAlign: "center" }}>
          {this.props.category}
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



        <div>{(()=>{
          const numbers = [1,2,3,4,5]
          if (this.state.data.length != 0) {
            console.log("there are uploads");
            console.log(">>> data:", this.state.data);
            // this.state.data.map(item_data => {
            //   return <Thumbnail data={item_data} />;
            // });
            // a = numbers.map((number) => <div>{number}</div>)
            // console.log(a);
            // return a;
            let data = this.state.data.map(item_data => <Thumbnail data={item_data} />);
            console.log(data);
            return data;
          } else {
            console.log("no uploads on this page yet")
            return (
              <div className="empty-page">
                <div className="empty-page-text">
                  Sorry, no uploads on this page yet.
                </div>
              </div>
            );
          }

        })()}</div>
      </div>
    );
  }
}

export default Display;
