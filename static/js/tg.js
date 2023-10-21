const user_id = WebApp.initDataUnsafe.user.id;

document.querySelector("button").addEventListener("click", () => {
  document.querySelector(".tg_id").innerHTML = user_id;
  // WebApp.close();
});
