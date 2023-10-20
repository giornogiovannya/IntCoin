// async function start() {
//   const res = await axios.get("http://127.0.0.1:5000/goods");
//   console.log(res);
// }

// start();

const user_id = WebApp.initDataUnsafe.user.id;

console.log(user_id);

document.querySelector("button").addEventListener("click", () => {
  console.log(user_id);
  WebApp.sendData(JSON.stringify({ text: user_id }));
});
