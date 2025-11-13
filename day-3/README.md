```markdown
# 🧠 Day 3 – JavaScript ES6 + DOM Manipulation

## 🔹 Learning Outcomes
By the end of this task, you will:
- Understand **modern JavaScript (ES6)** features such as `let`, `const`, and **arrow functions**.
- Use **array/object methods** (`map`, `filter`, `reduce`) for data processing.
- Manipulate the **DOM (Document Object Model)** without using frameworks.
- Handle **user interactions** with event listeners.
- Build and control UI components like:
  - **Navbar toggle**
  - **Dropdown menu**
  - **Modal pop-up**
  - **Counter buttons**
  - **Keyboard event logging**
- Create an **interactive FAQ Accordion** using pure JavaScript.

---

## 🧩 Topics & Activities

| Topic | Activity |
|-------|-----------|
| Variables & Functions | Use `let`, `const`, and arrow functions |
| Arrays & Objects | Practice with `map()`, `filter()`, and `reduce()` |
| DOM Manipulation | Toggle navbar, dropdown, and modal using JS |
| Event Listeners | Implement click and keyboard events |
| Mini Project | Build a **FAQ Accordion** with JS expand/collapse feature |

---

## 🧪 Exercise: FAQ Accordion

**Goal:** Build an interactive FAQ accordion using **HTML**, **CSS**, and **JavaScript**.  
Each question should expand on click to reveal the answer, and collapse when another is opened.

### 🧱 Features:
- Smooth open/close animation.
- Only one accordion opens at a time.
- Fully responsive design.
- No frameworks — only **vanilla JS**.

### 🖼️ Reference Design:
![FAQ Accordion Example](https://codeconvey.com/wp-content/uploads/2020/02/responsive-accordion-pure-css.png.webp)

---

## 🧰 Files Included
```

│
├── index.html      # Main HTML structure for accordion
├── style.css       # Styling for accordion and layout
├── script.js       # JavaScript logic for interactivity
└── README.md       # Project documentation


```

![alt text](<Screenshot from 2025-11-13 16-45-44.png>)


---

## ⚙️ How It Works
1. Click on any FAQ header → toggles its visibility.
2. When a header is opened, all other accordions close.
3. Uses simple **`classList.toggle()`** and **event listeners** to manage UI state.

---

## 📚 Concepts Demonstrated
- **ES6 Syntax:** `let`, `const`, arrow functions
- **DOM Selection:** `querySelector`, `querySelectorAll`
- **Class Manipulation:** `classList.toggle()`
- **Event Handling:** `addEventListener()`
- **Array Methods:** `map`, `filter`, `reduce`
- **Objects & Template Literals**
- **Keyboard Events:** Listening to user key presses
- **Dynamic Styling:** Show/hide content with CSS transitions

---
