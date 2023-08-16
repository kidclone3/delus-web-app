Number.prototype.round = function (places) {
  // eslint-disable-line
  return +Math.round(`${this}e+${places}e-${places}`);
};

export const wait = (t) =>
  new Promise((res) => {
    setTimeout(() => {
      res();
    }, t);
  });

export const getRandomInt = (min, max) => {
  min = Math.ceil(min);
  max = Math.floor(max);

  return Math.floor(Math.random() * (max - min + 1)) + min;
};

const baseURL =
  process.env.APP_ENV === "dev"
    ? "http://localhost:8000"
    : "https://delusthefirst.tech";

export const api = {};
api.get = async (endpoint) => {
  const res = await fetch(`${baseURL}${endpoint}`);
  if (res.json) return await res.json();
  return res;
};
