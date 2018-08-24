import React from "react";

import { Carousel } from "react-bootstrap";

import axios from "axios";

let outerImgStyle = {
  backgroundColor: "black",
  height: "270px",
  margin: "0 auto",
  overflow: "hidden",
  position: "relative",
  borderRadius: "5px"
};

let innerImgStyle = {
  margin: "auto",
  maxHeight: "100%",
  maxWidth: "100%",
  position: "absolute",
  top: "0",
  bottom: "0",
  left: "0",
  right: "0"
};

let carouselStyle = {
  height: "270px",
  margin: "0 auto",
  overflow: "hidden",
  borderRadius: "5px"
};

let carouselItemStyle = {
  backgroundColor: "black",
  height: "270px",
  margin: "0 auto",
  overflow: "hidden"
};

let innerCarouselStyle = {
  margin: "auto",
  position: "absolute",
  maxHeight: "100%",
  maxWidth: "100%",
  top: "0",
  bottom: "0",
  left: "0",
  right: "0"
};

const Thumbnail = ({ data, deleteFunc }) => {
  console.log(data);

  let carousel = (
    <div style={outerImgStyle}>
      <img
        src={data.image_one ? data.image_one : "static/emptyImage.png"}
        style={innerImgStyle}
      />
    </div>
  );

  let images = [
    data.image_one,
    data.image_two,
    data.image_three,
    data.image_four
  ];

  if (data.image_two) {
    carousel = (
      <Carousel style={carouselStyle}>
        {images.map(image => {
          if (image != "") {
            return (
              <Carousel.Item style={carouselItemStyle}>
                <img src={image} style={innerCarouselStyle} />
              </Carousel.Item>
            );
          }
        })}
      </Carousel>
    );
  }

  return (
    <div className="item-thumbnail-wrapper">
      <div className="item-thumbnail">
        <div className="row">
          <div className="col-md-3">
            <div>{carousel}</div>
          </div>
          <div className="col-md-9">
            <div style={{ marginLeft: "10px" }}>
              <h2>{data.title}</h2>
              <p style={{ fontSize: "15px" }}>{data.details}</p>

              <div className="row">
                {data.money ? (
                  <div className="col-md-6">
                    <h5>💰 Money Value:</h5>
                    <p>{data.money}</p>
                  </div>
                ) : (
                  <div />
                )}
                {data.exchange ? (
                  <div className="col-md-6">
                    <h5>⚖️ Exchange Value:</h5>
                    <p>{data.exchange}</p>
                  </div>
                ) : (
                  <div />
                )}
              </div>

              {!deleteFunc ? (
                <p style={{ marginTop: "10px" }}>
                  Uploaded by{" "}
                  <a
                    style={{
                      color: "#F2A93B",
                      textDecoration: "none"
                    }}
                    href={"mailto:" + data.uploader}
                  >
                    {data.uploader}
                  </a>
                </p>
              ) : (
                <button
                  className="btn btn-danger"
                  style={{ marginTop: "10px" }}
                  onClick={() => {
                    if (
                      window.confirm(
                        "Do you really want to delete " + data.title + "?"
                      )
                    ) {
                      axios
                        .delete(window.CURRENT_HOST + "/complete?id=" + data.id)
                        .then(window.location.reload());
                    }
                  }}
                >
                  DELETE/COMPLETE ITEM
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Thumbnail;
