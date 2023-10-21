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
  const x = e.pageX || e.touches[0].pageX - item.offsetLeft;
  const dist = (x - startX);
  item.scrollLeft = scrollLeft - dist;
}

(() => {
	item.addEventListener('mousedown', start);
	item.addEventListener('touchstart', start);

	item.addEventListener('mousemove', move);
	item.addEventListener('touchmove', move);

	item.addEventListener('mouseleave', end);
	item.addEventListener('mouseup', end);
	item.addEventListener('touchend', end);
})();
}