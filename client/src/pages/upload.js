import React, { Component } from "react";

import { Button } from "react-bootstrap";

import axios from "axios";

import S3FileUpload from "../components/s3uploader/ReactS3.js";

var uploadURL = window.CURRENT_HOST + "upload";
let form_style = { margin: "0px 10px" };

const config = {
  bucketName: "reshwapimages",
  region: "us-east-2",
  accessKeyId: "AKIAIRCRJSX4GBPH3CXA",
  secretAccessKey: "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"
};

class Upload extends Component {
  constructor() {
    super();
    this.state = {
      category_value: "Books",
      money_value: "",
      exchange_value: "",
      details_value: "",
      dep_value: "English",
      title_value: "",
      files: [],
      loading: false
    };
    this.handleCategoryChange = this.handleCategoryChange.bind(this);
    this.handleDetailsChange = this.handleDetailsChange.bind(this);
    this.handleDepChange = this.handleDepChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleTitleChange = this.handleTitleChange.bind(this);
    this.handleMoneyChange = this.handleMoneyChange.bind(this);
    this.handleExChange = this.handleExChange.bind(this);

    this.fileInput = React.createRef();
  }

  handleCategoryChange(event) {
    this.setState({ category_value: event.target.value });
    console.log(event.target.value);
  }
  handleMoneyChange(event) {
    this.setState({ money_value: event.target.value });
    console.log(event.target.value);
  }
  handleExChange(event) {
    this.setState({ exchange_value: event.target.value });
    console.log(event.target.value);
  }
  handleDetailsChange(event) {
    this.setState({ details_value: event.target.value });
    console.log(event.target.value);
  }
  handleDepChange(event) {
    this.setState({ dep_value: event.target.value });
    console.log(event.target.value);
  }
  handleTitleChange(event) {
    this.setState({ title_value: event.target.value });
    console.log(event.target.value);
  }

  handleSubmit() {
    var allUploadPromises = [];
    let i;
    var p;

    let isValid =
      this.state.title_value.length > 0 && this.state.details_value.length > 0;

    if (isValid) {
      this.setState({ loading: true });

      console.log(this.state.files);

      const newFiles = Array.from(this.state.files).map((file, index) => {
        const name =
          index.toString() +
          Date.now() +
          Math.floor(Math.random() * 10) +
          file.name.substring(file.name.lastIndexOf("."));
        return new File([file], name, { type: file.type });
      });

      console.log(newFiles);

      for (i = 0; i < newFiles.length; i++) {
        p = S3FileUpload.uploadFile(newFiles[i], config)
          .then(data => {
            return data;
          })
          .catch(err => {
            console.log(err);
          });
        allUploadPromises.push(p);
      }

      Promise.all(allUploadPromises).then(data => {
        var images = data.map(file => file.location);
        console.log("IMAGE URLS:");
        console.log(images);
        console.log(images[0]);
        axios
          .post(uploadURL, {
            uploader: window.currentUser,
            category: this.state.category_value,
            title: this.state.title_value,
            department: this.state.dep_value,
            details: this.state.details_value,
            money: this.state.money_value,
            exchange: this.state.exchange_value,
            imageUrls: images
          })
          .then(() => {
            alert("Upload successful!");
            window.location = window.CURRENT_HOST + "#/myitems";
          });
      });
    } else {
      alert("Have you filled out all forms?");
    }
  }

  componentDidMount() {
    var self = this;
    console.log(window.currentUser);
  }

  render() {
    let Departments = [
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

    var book_details = (
      <div>
        <h4 style={{ marginLeft: "10px" }}>Department</h4>
        <div style={form_style}>
          <select
            className="form-control"
            onChange={this.handleDepChange}
            value={this.state.dep_value}
          >
            {Departments.map(department => {
              return <option key={department}>{department}</option>;
            })}
          </select>
        </div>
      </div>
    );
    if (this.state.category_value != "Books") {
      book_details = <div />;
    }

    let loading = (
      <button className="upload-button" onClick={this.handleSubmit}>
        <b>UPLOAD ITEM TO RESHWAP</b>
      </button>
    );
    if (this.state.loading) {
      loading = (
        <div>
          <h5 style={{ marginLeft: "10px" }}>Loading...</h5>
        </div>
      );
    }

    return (
      <div>
        <h3 className="bold" style={{ textAlign: "center" }}>
          Upload
        </h3>

        <h4 style={{ marginLeft: "10px" }}>Category</h4>
        <div style={form_style}>
          <select
            className="form-control"
            value={this.state.category_value}
            onChange={this.handleCategoryChange}
          >
            <option>Books</option>
            <option>Furniture</option>
            <option>Electronics</option>
            <option>Other</option>
          </select>
        </div>

        {book_details}

        <h4 style={{ marginLeft: "10px" }}>Title</h4>
        <div className="form-group" style={form_style}>
          <textarea
            maxLength="70"
            className="form-control"
            rows="1"
            onChange={this.handleTitleChange}
            value={this.state.title_value}
          />
        </div>

        <h4 style={{ marginLeft: "10px" }}>Details</h4>
        <div className="form-group" style={form_style}>
          <textarea
            maxlength="350"
            className="form-control"
            rows="3"
            onChange={this.handleDetailsChange}
            value={this.state.details_value}
          />
        </div>

        <h4 style={{ marginLeft: "10px" }}>Value</h4>
        <div>
          <div className="col-xs-3">
            <h5>Money 💰</h5>
            <textarea
              maxlength="50"
              onChange={this.handleMoneyChange}
              value={this.state.money_value}
              className="form-control"
              rows="3"
              style={{ marginBottom: "10px" }}
            />
          </div>
          <div className="col-xs-9">
            <h5>Exchange ⚖️ (would exchange for...)</h5>
            <textarea
              maxlength="100"
              onChange={this.handleExChange}
              value={this.state.exchange_value}
              className="form-control"
              rows="3"
              style={{ marginBottom: "30px" }}
            />
          </div>
        </div>

        <h4 style={{ marginLeft: "10px" }}>
          Image (You can now choose up to 4 images)
        </h4>

        <input
          className="inputfile"
          style={{ marginLeft: "10px" }}
          type="file"
          name="file"
          id="file"
          accept="image/*"
          multiple
          ref={this.fileInput}
          onChange={() => {
            if (this.fileInput.current.files.length > 4) {
              alert("Too many files, only 4 chosen");
              this.setState(
                {
                  files: [
                    this.fileInput.current.files[0],
                    this.fileInput.current.files[1],
                    this.fileInput.current.files[2],
                    this.fileInput.current.files[3]
                  ]
                },

                console.log("files:", this.state.files)
              );
            } else {
              this.setState({ files: this.fileInput.current.files }, () =>
                console.log("files:", this.state.files)
              );
            }
          }}
        />
        <div style={{ marginLeft: "10px" }}>
          <label for="file">
            <i className="glyphicon glyphicon-inbox" /> Choose files
          </label>
          <span style={{ marginLeft: "10px" }}>
            {this.state.files.length > 0
              ? this.state.files.length + " files chosen"
              : "No files chosen"}
          </span>
        </div>
        <hr className="upload-hr" />
        {loading}
      </div>
    );
  }
}

export default Upload;
