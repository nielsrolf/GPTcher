
import { useState, useEffect } from 'react';

const Starfield = () => {

  useEffect(() => {
    const starfield = document.getElementById("starfield");

    const generateStar = () => {
      const star = document.createElement("div");
      star.classList.add("star");
      star.style.top = Math.random() * 98 + "%";
      star.style.left = Math.random() * 98 + "%";
      star.style.width = Math.random() * 2 + 1 + "px";
      star.style.height = star.style.width;
      star.style.opacity = Math.random();
      starfield.appendChild(star);
      
      // setTimeout(() => {
      //   star.style.opacity = 0;
      //   setTimeout(() => {
      //     star.remove();
      //     generateStar();
      //   }, 500);
      // }, Math.random() * 100000);
    }

    for (let i = 0; i < 1000; i++) {
      generateStar();
    }
  }, []);

  return (
    <div id="starfield"></div>
  )
}

export default Starfield;