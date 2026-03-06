module.exports = {
  apps: [
    {
      name: "hensight",
      script: "build/index.js",
      interpreter: "bun",
      env: {
        PORT: 5300,
        HOST: "0.0.0.0"
      }
    }
  ]
};