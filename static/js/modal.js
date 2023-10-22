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
