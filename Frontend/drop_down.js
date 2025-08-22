const multiSelect = document.getElementById('multiSelect');
const dropdown = document.getElementById('dropdown');
const selectedItems = document.getElementById('selectedItems');
const searchInput = document.getElementById('searchSymptoms');
const predictBtn = document.getElementById('predictBtn');
const selectedValues = new Set();

multiSelect.addEventListener('click', (e) => {
  // Prevent closing dropdown when clicking input
  if (e.target === searchInput) return;
  multiSelect.classList.toggle('active');
  searchInput.focus();
});

// Click to select
dropdown.addEventListener('click', (e) => {
  const option = e.target.closest('.dropdown-option');
  if (!option) return;

  const value = option.getAttribute('data-value');
  const label = option.textContent;

  if (!value || selectedValues.has(value)) return;

  selectedValues.add(value);

  const placeholder = selectedItems.querySelector('.placeholder');
  if (placeholder) placeholder.remove();

  const tag = document.createElement('span');
  tag.innerHTML = `${label} <i data-remove="${value}">&times;</i>`;
  selectedItems.appendChild(tag);
});

// Remove tag
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

// Close dropdown when clicking outside (but not inside input)
document.addEventListener('click', (e) => {
  if (!multiSelect.contains(e.target)) {
    multiSelect.classList.remove('active');
  }
});

// Search filter
searchInput.addEventListener('input', function () {
  const searchTerm = this.value.toLowerCase();
  const options = dropdown.querySelectorAll('.dropdown-option');
  options.forEach(option => {
    const text = option.textContent.toLowerCase();
    option.style.display = text.includes(searchTerm) ? 'block' : 'none';
  });
});

predictBtn.addEventListener('click', () => {
  document.getElementById('hiddenSymptoms').value = Array.from(selectedValues).join(',');
  document.getElementById('hiddenAge').value = document.getElementById('age').value;
  document.getElementById('hiddenGender').value = document.getElementById('gender').value;

  document.getElementById('predictionForm').submit();
});

