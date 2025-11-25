const path = require("path")
const HTMLWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  entry: "./app/index.js",
  module: {
    rules: [
      {
        test: /\.svg$/,
        use: "svg-inline-loader",
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.(js)$/,
        use: "babel-loader",
      type: "javascript/auto",
      },
    ],
  },
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "bundle.js",
  },
  plugins:[new HTMLWebpackPlugin()],
   mode: process.env.NODE_ENV === "production" ? "production":"development" , 
};
