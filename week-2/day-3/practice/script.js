let counter = 0;
const appName = "JS DOM Demo";

const greetUser = (name = "Guest") => {
  console.log(`Welcome to ${appName}, ${name}!`);
};

greetUser("Vidhi");

const numbers = [1, 2, 3, 4, 5, 6];

const doubled = numbers.map(n => n * 2);
console.log("Doubled:", doubled);

const evens = numbers.filter(n => n % 2 === 0);
console.log("Even numbers:", evens);

const sum = numbers.reduce((acc, n) => acc + n, 0);
console.log("Sum:", sum);

const user = {
  name: "Vidhi",
  role: "Developer",
  skills: ["HTML", "CSS", "JavaScript"]
};

console.log(`${user.name} is a ${user.role} skilled in ${user.skills.join(", ")}`);


const menuBtn = document.querySelector("#menu-btn");
const navLinks = document.querySelector("#nav-links");

if (menuBtn && navLinks) {
  menuBtn.addEventListener("click", () => {
    navLinks.classList.toggle("visible");
    console.log("Navbar toggled");
  });
}

// Dropdown
const dropdownBtn = document.querySelector("#dropdown-btn");
const dropdownMenu = document.querySelector("#dropdown-menu");

if (dropdownBtn && dropdownMenu) {
  dropdownBtn.addEventListener("click", () => {
    dropdownMenu.classList.toggle("open");
    console.log("Dropdown toggled");
  });
}

// Modal
const openModalBtn = document.querySelector("#open-modal");
const closeModalBtn = document.querySelector("#close-modal");
const modal = document.querySelector("#modal");

if (openModalBtn && modal && closeModalBtn) {
  openModalBtn.addEventListener("click", () => {
    modal.style.display = "block";
  });

  closeModalBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });
}

// 4. Event Listeners (counter + key events)

const countDisplay = document.querySelector("#count");
const incBtn = document.querySelector("#increment");
const decBtn = document.querySelector("#decrement");

if (countDisplay && incBtn && decBtn) {
  incBtn.addEventListener("click", () => {
    counter++;
    countDisplay.textContent = counter;
  });

  decBtn.addEventListener("click", () => {
    counter--;
    countDisplay.textContent = counter;
  });
}

document.addEventListener("keydown", (event) => {
  console.log(`Key pressed: ${event.key}`);
});

