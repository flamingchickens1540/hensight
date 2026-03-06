module.exports = {
  apps: [
    {
      name: "hensight",
      script: "bun",
      args: "build/index.js",
      interpreter: "none",
      env: {
        PORT: 5300,
        HOST: "0.0.0.0"
      }
    }
  ]
};