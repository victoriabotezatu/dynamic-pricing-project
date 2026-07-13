const navButtons = document.querySelectorAll(".nav-btn");
const views = document.querySelectorAll(".view");

navButtons.forEach(function (button) {
  button.addEventListener("click", function () {
    const target = button.dataset.target;

    navButtons.forEach(function (btn) {
      btn.classList.remove("active");
    });

    views.forEach(function (view) {
      view.classList.remove("active");
    });

    button.classList.add("active");
    document.getElementById(target).classList.add("active");
  });
});
