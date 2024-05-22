module.exports = {
  env: {
    APP_ENV: process.env.APP_ENV,
    APP_API: process.env.APP_API,
  },
  webpack: (config) => {
    config.resolve.extensions.push(".ts", ".tsx");
    return config;
  },
};
