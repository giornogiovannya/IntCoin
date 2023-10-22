const modal = document.querySelector(".modal");
const confimation = document.querySelector(".confirmation")
const modalWindow = document.querySelector(".window");
const hashDict = {}

let cost = 0;
let hash = "";
let size = ""
let balance = 0;
let costGoods = 0;

const getUser = async () => {
  const user = (await axios.get(`${host}/users?user_id=${user_id}`)).data;
  
  document.querySelector(".coins").innerHTML = user.intcoins
  document.querySelector(".avatar").src = "static/uploads/" + user.avatar;
  balance = user.intcoins
}

getUser()

const items = document.querySelectorAll('.items');

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
    outList(res);
  });

  const outList = (data, item) => {
    if (data.length === 0) return
    let html = "";

    if (table === "goods") {
      for (let dataItem of data) {
        if (hashDict[dataItem.goods_hash]) {
          hashDict[dataItem.goods_hash].push(dataItem)
        }
        else {
          hashDict[dataItem.goods_hash] = [dataItem]
        }
      }
      
      for (let hash in hashDict){
        let id;
        let title;
        let description;
        let cost = 0;
        for (let dataItem of hashDict[hash]){
          title = dataItem.goods_title
          description = dataItem.goods_description
          id = dataItem.goods_id
          cost = dataItem.goods_cost
        }
        html += `<li class="item" onclick="openModal('${table}', '${hash}')" data_id="${hash}">
                         <span>${title}</span>
                         <span>${description}</span>
                         <span>${cost}</span>
                       </li>`;
      }
      item.innerHTML = html
    }
    else if (table === "tasks") {
      for (let dataItem of data) {
        html += `<li class="item" onclick="openModal('${table}', '${dataItem.task_id}')" data_id="${dataItem.task_id}">
                      <span>${dataItem.task_title}</span>
                      <span>${dataItem.task_description}</span>
                      <span>${dataItem.task_cost}</span>
                    </li>`;
      }
      item.innerHTML = html
    }
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

const openModal = async (table, id) => {
  hash = id;
  modal.style.display = "block";
  confimation.style.display = "none"
  
  filter = "";
  if (table === "goods"){
    
    const buyBtn = document.querySelector(".buy");
    const s = document.querySelector(".sizes");
    
    while (s.lastChild){
      s.removeChild(s.lastChild)
    }
    
    document.querySelector(".count").style.display = "none"
    
    const res = (await axios.get(`${host}/${table}?filter=goods_hash&value=${id}`)).data
    let title = "";
    let description = "";
    let sizes = {};
    
    for (let dataItem of hashDict[id]) {
      if (sizes[dataItem.goods_merch_size])
        sizes[dataItem.goods_merch_size] += dataItem.goods_count
      else
        sizes[dataItem.goods_merch_size] = dataItem.goods_count;
      title = dataItem.goods_title
      description = dataItem.goods_description
      id = dataItem.goods_id
      cost = dataItem.goods_cost
    }
    
    if (balance - cost <= 0) {
      buyBtn.disabled = true;
      buyBtn.classList.add("disabled")
      buyBtn.innerText = `Вам не хватает ${cost-balance}`
      buyBtn.innerHTML += `<svg width="26" height="26" xmlns="http://www.w3.org/2000/svg" style="background-color:transparent">
  <circle cx="13" cy="13" r="10" fill="black" />
  <text x="9" y="17" font-family="Arial" font-size="12" fill="white">|</text>
  <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 30 30" fill="none" x="12" y="7">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M3.285 2.55726L1.54509 3.28538 0 4.01351 0 0 1.54509 0.728126 3.285 2.55726Z" fill="#45AE31"/>
  </svg>
</svg>`
    }
    
    document.querySelector(".window").style.display = "flex";
  
    document.querySelector(".title").innerHTML = title
    document.querySelector(".description").innerHTML = description
    document.querySelector(".cost").innerHTML = cost
    
    for (size in sizes){
      const li = document.createElement("li")
      const btn = document.createElement("button");
      const p = document.createElement("p");
      
      if (res[0].goods_category === "merch"){
        li.classList = "size";
        btn.classList = btn;
        btn.innerText = size;
        
        btn.classList = "btn btn-size"
        btn.id = sizes[size];
        btn.setAttribute("data-size", size)
        
        if (sizes[size] === 0) {
          btn.disabled = true
          btn.classList.add("disabled")
        }
        
        p.innerText = 'В наличии: ';
        li.append(btn);
        
        document.querySelector(".sizes").append(li)
      }
    }
    
    const btns = document.querySelectorAll(".btn-size")
    
    btns.forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.id
        size = btn.getAttribute("data-size")
        console.log(btn);
        
        console.log(btn.getAttribute("data-size"));
        
        if (btn.disabled){
          document.querySelector(".count").style.display = "none"
        }
        
        document.querySelector(".count").style.display = "block"
        document.querySelector(".count").innerText = `В наличии: ${id}`
      })
    })
    
    buyBtn.addEventListener("click", () => {
      modal.style.display = "none"
      confimation.style.display = "block"
      confimation.style.opacity = 1;
      costGoods = cost;
      document.querySelector(".body .info").innerText = `Вы уверены что хотите купить ${title} за ${cost}?`
    })
  }
  else if (table === "tasks"){
    const res = (await axios.get(`${host}/${table}?filter=id&value=${id}`)).data[0]
    document.querySelector(".window").style.display = "flex";
    document.querySelector(".title").innerHTML = res.task_title;
    document.querySelector(".description").innerHTML = res.task_description;
    document.querySelector(".cost").innerHTML = res.task_cost;
    
  }
}

document.querySelector(".close").addEventListener("click", () => {
  document.querySelector(".window").style.display = "none";
})

document.querySelector(".window").addEventListener("click", (e) => {
  if (e.target === document.querySelector(".window")){
    document.querySelector(".window").style.display = "none";
  }
})

document.querySelector(".cancel").addEventListener("click", () => {
  modal.style.display = "block";
  confimation.style.display = "none";
})

document.querySelector(".access").addEventListener("click", async () => {
  modalWindow.style.display = "none";
  modal.style.display = "block";
  confimation.style.display = "none";
  
  const body = {
    user_id,
    goods_hash: hash,
    cost,
    size
  }
  
  await axios.post(`${host}/buy`, body)
  await getUser()
})

