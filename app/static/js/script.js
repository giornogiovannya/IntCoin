// async function start() {
//   const res = await axios.get("http://127.0.0.1:5000/goods");
//   console.log(res);
// }

// start();

document.querySelector("button").addEventListener("click", () => {
  WebApp.sendData(JSON.stringify({ text: "hello, world" }));
});
