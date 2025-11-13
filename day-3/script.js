const accordions = document.querySelectorAll('.accordion');

accordions.forEach(acc => {
  const header = acc.querySelector('.accordion-header');

  header.addEventListener('click', () => {
    accordions.forEach(item => {
      if (item !== acc) item.classList.remove('active');
    });
    acc.classList.toggle('active');
  });
});
