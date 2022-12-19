import React, { Component } from 'react'
import client from '../config/socket';

class Trace extends Component {
  constructor(props)
  {
    super(props);
    this.width = window.innerWidth - this.props.width;
    this.height = this.props.height - 50;
    this.img = {
      width : 500,
      height : this.height
    }

    /// Dữ liệu
    client.on("data", (data) => this.onDataSocket(data));

    /// Số hàng + Số cột ma trận
    this.rows = 50;
    this.cols = 50;
    this.size = 5;
  }

  update_canvas(url, __another)
  {
    let { width, height } = this.img;
    let { my_canvas, size } = this;
    let image = new Image();
    image.src = url;
    image.onload = function(__ev)
    {
      let context = my_canvas.getContext("2d");
      context.drawImage(image, my_canvas.width - width, 
        0, width, height);
      let { x, y } = __another;
      /// x, y đây là tọa độ của thuyền
      /// nội suy ra tọa độ trên bảng hành trình
      y += my_canvas.height;
      context.beginPath();
      context.arc(x, y, size, 0, Math.PI * 2);
      context.fillStyle = "green";
      context.fill();
      context.closePath();
    };
  }

  componentDidMount()
  {
    let canvas = document.querySelector("canvas");
    canvas.width = this.width;
    this.my_canvas = canvas;
    /// Khu vực draw matrix
    this.draw_matrix({
      x : 0, y : 0,
      w : canvas.width - this.img.width,
      h : this.height
    }, this.rows, this.cols);
    /// Cập nhật ảnh nền
    this.update_canvas("/avatar.png", { x : 0, y : 0 });
  }

  draw_matrix(rectangle, rows, cols)
  {
    let context = this.my_canvas.getContext("2d");
    this.draw_rows(rows, rectangle.h, context, rectangle.w);
    this.draw_cols(cols, rectangle.w, context, rectangle.h);
  }

  draw_rows(rows, delta_y, context, delta_x)
  {
    /// Vẽ hàng 
    for (let i = 0; i <= rows; i++)
    {
      let y = i * (delta_y / rows);
      /// Ngang là trục width
      /// Dọc là trục height
      context.beginPath();
      context.moveTo(0, y);
      context.strokeStyle = "red";
      context.lineWidth = 1;
      context.lineTo(delta_x, y);
      context.stroke();
    }
  }

  draw_cols(cols, delta_x, context, delta_y)
  {
    /// Vẽ cột
    for (let j = 0; j <= cols; j++)
    {
      let x = j * (delta_x / cols);
      context.beginPath();
      context.moveTo(x, 0);
      context.strokeStyle = "blue";
      context.lineWidth = 1;
      context.lineTo(x, delta_y);
      context.stroke();
    }
  }

  onDataSocket(data)
  {
    let { url } = data;
    this.update_canvas(url, data);
  }

  render() {
    return (
      <canvas id="trace" 
        height={this.height}
        style={{ border : "1px solid black" }}
      ></canvas>
    );
  }
}

export default Trace;