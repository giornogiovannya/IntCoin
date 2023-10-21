const carousel = document.querySelectorAll(".carousel");

for(let car of carousel){
  const firstBlock = car.querySelectorAll(".goods_item")[0];

  const category = car.classList[1]
  
  let isDragStart = false;
  let isDragging = false
  let prevPageX;
  let prevScrollLeft;
  let positionDiff;
  
  function outList(goods) {
    const list = car;
  
    let html = "";
  
    for (let goodsItem of goods) {
      html += `<div class="goods_item">
                        <p>${goodsItem.name}</p>
                        <p>${goodsItem.description}</p>
                        <p>${goodsItem.price}</p>
                      </div>`;
    }
    list.innerHTML = html;
  }
  
  async function start() {
    const res = (await axios.get(`${host}/goods?filter=type&value=${category}`)).data;
    outList(res);
  }
  
  window.addEventListener("load", start);
  
  const autoSlide = () => {
      if(car.scrollLeft - (car.scrollWidth - car.clientWidth) > -1 || car.scrollLeft <= 0) return;
      positionDiff = Math.abs(positionDiff); // making positionDiff value to positive
      let firstImgWidth = firstBlock.clientWidth + 14;
      let valDifference = firstImgWidth - positionDiff;
      if(car.scrollLeft > prevScrollLeft) { // if user is scrolling to the right
          return car.scrollLeft += positionDiff > firstImgWidth / 3 ? valDifference : -positionDiff;
      }
      car.scrollLeft -= positionDiff > firstImgWidth / 3 ? valDifference : -positionDiff;
  }
  const dragStart = (e) => {
      isDragStart = true;
      prevPageX = e.pageX || e.touches[0].pageX;
      prevScrollLeft = car.scrollLeft;
  }
  const dragging = (e) => {
      if(!isDragStart) return;
      e.preventDefault();
      isDragging = true;
      car.classList.add("dragging");
      positionDiff = (e.pageX || e.touches[0].pageX) - prevPageX;
      car.scrollLeft = prevScrollLeft - positionDiff;
  }
  const dragStop = () => {
      isDragStart = false;
      car.classList.remove("dragging");
      if(!isDragging) return;
      isDragging = false;
      autoSlide();
  }
  car.addEventListener("mousedown", dragStart);
  car.addEventListener("touchstart", dragStart);
  document.addEventListener("mousemove", dragging);
  car.addEventListener("touchmove", dragging);
  document.addEventListener("mouseup", dragStop);
  car.addEventListener("touchend", dragStop);
}