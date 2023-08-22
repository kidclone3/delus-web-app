import React from "react";
import GeoMap from "../src/GeoMap";

export default function Home() {
  return (
    <div className="App">
      <GeoMap />
      <div className="description">
        <p className="mt-6 space-y-7 text-sm text-zinc-600 dark:text-zinc-400">
          <em>Rides</em>
          &nbsp;is my take on building and visualizing a distributed system.
          Read more at
          <a
            className="text-blue-500 hover:text-blue-600 transition-colors"
            href="https://delusthefirst.tech"
            target="_blank"
            rel="noreferrer"
          >
            &nbsp;delusthefirst.tech
          </a>
        </p>
      </div>
    </div>
  );
}
