const items = document.querySelectorAll('.items');

// document.querySelector(".user_id").innerHTML = user_id

let isDown = false;
let startX;
let scrollLeft;
let shopActive = true;
let table;
let filter;
if (document.location.search === "" || document.location.search === "?activate=shop") {
  table = "goods";
  filter = "goods_category"
}
else if (document.location.search === "?activate=tasks") {
  table = "tasks";
  filter = "task_category"
}

for (let item of items){
  const category = item.classList[1];
  const end = () => {
	  isDown = false;
    item.classList.remove('active');
  }
  
  document.querySelector(".search").addEventListener("input", async (e) => {
    const value = e.target.value;
    const res = (await axios.get(`${host}/${table}?filter=${filter}&value=${category}&search=${value}`)).data;
    console.log(res);
    outList(res);
  });

  function outList(data, item) {
    let html = "";

    for (let dataItem of data) {
      html += `<li class="item">
                      <span>${dataItem.goods_title || dataItem.task_title}</span>
                      <span>${dataItem.goods_description || dataItem.task_description}</span>
                      <span>${dataItem.goods_cost || dataItem.task_cost}</span>
                    </li>`;
    }

    item.innerHTML = html;
  }
  
  
  const req = async (item) => {
    const res = (await axios.get(`${host}/${table}?filter=${filter}&value=${category}`)).data;
    outList(res, item);
  }

  req(item)

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

const shop = document.querySelector(".shop")
const tasks = document.querySelector(".tasks")