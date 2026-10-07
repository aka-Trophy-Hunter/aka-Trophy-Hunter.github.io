document.getElementById('year').textContent = new Date().getFullYear();

// News "show all" toggle — hides items beyond the first 3 until clicked.
const newsItems = document.querySelectorAll('.news-list li');
const toggleBtn = document.getElementById('toggle-news');
if (toggleBtn) {
  newsItems.forEach((li, i) => { if (i >= 3) li.style.display = 'none'; });
  if (newsItems.length <= 3) toggleBtn.style.display = 'none';
  toggleBtn.addEventListener('click', () => {
    newsItems.forEach(li => li.style.display = '');
    toggleBtn.style.display = 'none';
  });
}

// Publication filter buttons
const filterBtns = document.querySelectorAll('.filter-btn');
const pubCards = document.querySelectorAll('.pub-card');
filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    pubCards.forEach(card => {
      const tags = card.dataset.tags.split(' ');
      card.classList.toggle('hidden', filter !== 'all' && !tags.includes(filter));
    });
  });
});
