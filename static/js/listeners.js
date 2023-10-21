// const input = document.querySelector(".search");
//
// let filter = "";
// let filterValue = ""
//
// function outList(goods) {
//   const list = document.querySelector(".goods_list");
//
//   let html = "";
//
//   for (let goodsItem of goods) {
//     html += `<li class="goods_item">
//                       <span>${goodsItem.name}</span>
//                       <span>${goodsItem.description}</span>
//                       <span>${goodsItem.price}</span>
//                     </li>`;
//   }
//
//   // list.innerHTML = html;
// }
//
// document.querySelector(".all").addEventListener("click", start);
//
// document.querySelector(".clothes").addEventListener("click", async () => {
//   const res = (await axios.get(`${host}/goods?filter=type&value=Одежда`)).data;
//   filter = "type";
//   filterValue = "Одежда";
//   outList(res);
// });
//
// document.querySelector(".travels").addEventListener("click", async () => {
//   const res = (await axios.get(`${host}/goods?filter=type&value=Путешествия`))
//     .data;
//   filter = "type";
//   filterValue = "Путешествия";
//   outList(res);
// });
//
// document.querySelector(".search").addEventListener("input", async (e) => {
//   const value = e.target.value;
//   let res;
//   if (filterValue !== "" && filter !== ""){
//     res = (await axios.get(`${host}/goods?filter=${filter}&value=${filterValue}&search=${value}`)).data;
//   }
//   else {
//     res = (await axios.get(`${host}/goods?search=${value}`)).data;
//   }
//   outList(res);
// });
//
// // document.querySelector(".menu").addEventListener("click", (e) => {
// //   const shop = document.querySelector(".menu .disable");
// //   const tsks = document.querySelector(".menu .active");
// //
// //
// // })
