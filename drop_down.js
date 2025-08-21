const multiSelect = document.getElementById('multiSelect');
const dropdown = document.getElementById('dropdown');
const selectedItems = document.getElementById('selectedItems');
const predictBtn = document.getElementById('predictBtn');

const selectedValues = new Set();

multiSelect.addEventListener('click', () => {
  multiSelect.classList.toggle('active');
});

dropdown.addEventListener('click', (e) => {
  const value = e.target.getAttribute('data-value');
  const label = e.target.textContent;

  if (!value || selectedValues.has(value)) return;

  selectedValues.add(value);

  const placeholder = selectedItems.querySelector('.placeholder');
  if (placeholder) placeholder.remove();

  const tag = document.createElement('span');
  tag.innerHTML = `${label} <i data-remove="${value}">&times;</i>`;
  selectedItems.appendChild(tag);
});

selectedItems.addEventListener('click', (e) => {
  if (e.target.dataset.remove) {
    const valueToRemove = e.target.dataset.remove;
    selectedValues.delete(valueToRemove);
    e.target.parentElement.remove();

    if (selectedValues.size === 0) {
      const placeholder = document.createElement('span');
      placeholder.className = 'placeholder';
      placeholder.textContent = 'Select options...';
      selectedItems.appendChild(placeholder);
    }
  }
});

document.addEventListener('click', (e) => {
  if (!multiSelect.contains(e.target)) {
    multiSelect.classList.remove('active');
  }
});

predictBtn.addEventListener('click', () => {
  alert('Selected: ' + Array.from(selectedValues).join(', '));
});
