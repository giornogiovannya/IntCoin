let isDown = false;
let startX;
let scrollLeft;
const items = document.querySelectorAll('.items');

for (let item of items){
  const end = () => {
	isDown = false;
  item.classList.remove('active');
}

const start = (e) => {
  isDown = true;
  item.classList.add('active');
  startX = e.pageX || e.touches[0].pageX - item.offsetLeft;
  scrollLeft = item.scrollLeft;
}

const move = (e) => {
	if(!isDown) return;

  e.preventDefault();
  const x = e.pageX || e.touches[0].pageX - sliders.offsetLeft;
  const dist = (x - startX);
  item.scrollLeft = scrollLeft - dist;
}

(() => {
	item.addEventListener('mousedown', start);
	document.addEventListener('touchstart', start);

	item.addEventListener('mousemove', move);
	document.addEventListener('touchmove', move);

	item.addEventListener('mouseleave', end);
	item.addEventListener('mouseup', end);
	document.addEventListener('touchend', end);
})();
}