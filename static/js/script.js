const carousel = document.querySelectorAll(".slider-container");

for(let car of carousel){
  let innerSlider = car.querySelector('.inner-slider');
  
  let pressed = false;
  let startX;
  let x;

  car.addEventListener('mousedown', (e) => {
    pressed = true;
    startX = e.offsetX - innerSlider.offsetLeft;
    car.style.cursor = "grabbing";
  })
  
  car.addEventListener('touchstart', (e) => {
    pressed = true;
    startX = e.offsetX - innerSlider.offsetLeft;
    car.style.cursor = "grabbing";
  })
  
  car.addEventListener("mouseenter", () => {
    car.style.cursor = "grab";
  });
  
  car.addEventListener("mouseup", () => {
    car.style.cursor = "grab";
    pressed = false;
  });
  
  car.addEventListener("touchend", () => {
    car.style.cursor = "grab";
    pressed = false;
  });
  
  car.addEventListener("mousemove", (e) => {
    if (!pressed) return;
    
    e.preventDefault();
    x = e.offsetX;
    innerSlider.style.left = `${x - startX}px`;
    checkBoundary();

  });
  
  car.addEventListener("touchmove", (e) => {
    if (!pressed) return;
    
    e.preventDefault();
    x = e.offsetX;
    innerSlider.style.left = `${x - startX}px`;
    checkBoundary();

  });
  
  const checkBoundary = () => {
    let outer = car.getBoundingClientRect();
    let inner = innerSlider.getBoundingClientRect();

    if (parseInt(innerSlider.style.left) > 0) {
        innerSlider.style.left = "0px";
    }

    if (inner.right < outer.right) {
        innerSlider.style.left = `-${inner.width - outer.width}px`;
    }
  };
}