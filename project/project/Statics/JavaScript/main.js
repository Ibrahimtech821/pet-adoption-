// ========================================
// Mobile Menu Toggle
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenuBtn.classList.toggle('active');
            mobileMenu.classList.toggle('active');
        });
    }
});

// ========================================
// Adoption Modal Functions
// ========================================
function openAdoptionModal(petName) {
    const modal = document.getElementById('adoptionModal');
    const modalTitle = document.getElementById('modalTitle');
    const adoptionForm = document.getElementById('adoptionForm');
    const successMessage = document.getElementById('successMessage');
    
    if (modal) {
        modalTitle.textContent = `Adoption Application for ${petName}`;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Reset form and show it
        if (adoptionForm) {
            adoptionForm.reset();
            adoptionForm.style.display = 'block';
        }
        if (successMessage) {
            successMessage.style.display = 'none';
        }
    }
}

function closeAdoptionModal() {
    const modal = document.getElementById('adoptionModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Close modal on background click
document.addEventListener('click', function(e) {
    const modal = document.getElementById('adoptionModal');
    if (modal && e.target === modal) {
        closeAdoptionModal();
    }
});

// Close modal on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeAdoptionModal();
    }
});

// ========================================
// Form Validation
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const adoptionForm = document.getElementById('adoptionForm');
    
    if (adoptionForm) {
        adoptionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Clear previous errors
            clearFormErrors();
            
            // Get form values
            const fullName = document.getElementById('fullName').value.trim();
            const email = document.getElementById('email').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const address = document.getElementById('address').value.trim();
            const experience = document.getElementById('experience').value;
            
            let isValid = true;
            
            // Validate full name
            if (!fullName) {
                showError('fullName', 'Full name is required');
                isValid = false;
            }
            
            // Validate email
            if (!email) {
                showError('email', 'Email is required');
                isValid = false;
            } else if (!isValidEmail(email)) {
                showError('email', 'Please enter a valid email');
                isValid = false;
            }
            
            // Validate phone
            if (!phone) {
                showError('phone', 'Phone number is required');
                isValid = false;
            }
            
            // Validate address
            if (!address) {
                showError('address', 'Address is required');
                isValid = false;
            }
            
            // Validate experience
            if (!experience) {
                showError('experience', 'Please select your pet experience');
                isValid = false;
            }
            
            // If form is valid, submit it
            if (isValid) {
                submitAdoptionForm();
            }
        });
    }
});

function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorSpan = document.getElementById(fieldId + 'Error');
    
    if (field) {
        field.classList.add('error');
    }
    if (errorSpan) {
        errorSpan.textContent = message;
    }
}

function clearFormErrors() {
    const errorInputs = document.querySelectorAll('.form-input.error, .form-select.error');
    const errorMessages = document.querySelectorAll('.form-error');
    
    errorInputs.forEach(input => {
        input.classList.remove('error');
    });
    
    errorMessages.forEach(message => {
        message.textContent = '';
    });
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function submitAdoptionForm() {
    const adoptionForm = document.getElementById('adoptionForm');
    const successMessage = document.getElementById('successMessage');
    const petNameSuccess = document.getElementById('petNameSuccess');
    const modalTitle = document.getElementById('modalTitle');
    
    // Get pet name from modal title
    const petName = modalTitle.textContent.replace('Adoption Application for ', '');
    
    // In a real application, you would send the form data to the server here
    // For now, we'll just show the success message
    
    // Hide form and show success message
    if (adoptionForm) {
        adoptionForm.style.display = 'none';
    }
    if (successMessage) {
        successMessage.style.display = 'block';
    }
    if (petNameSuccess) {
        petNameSuccess.textContent = petName;
    }
    
    // Close modal after 2 seconds
    setTimeout(function() {
        closeAdoptionModal();
    }, 2000);
}

// ========================================
// Favorite Button Toggle
// ========================================
document.addEventListener('click', function(e) {
    if (e.target.closest('.favorite-btn') || e.target.closest('.favorite-btn-large')) {
        e.preventDefault();
        const btn = e.target.closest('.favorite-btn') || e.target.closest('.favorite-btn-large');
        const svg = btn.querySelector('svg');
        
        if (svg) {
            // Toggle fill
            if (svg.style.fill === 'currentColor' || svg.style.fill === '') {
                svg.style.fill = '#ef4444';
                svg.style.color = '#ef4444';
            } else {
                svg.style.fill = '';
                svg.style.color = '';
            }
        }
    }
});

// ========================================
// Contact Form Submit
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('.contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const name = document.getElementById('contactName').value.trim();
            const email = document.getElementById('contactEmail').value.trim();
            const message = document.getElementById('contactMessage').value.trim();
            
            // Basic validation
            if (name && email && message && isValidEmail(email)) {
                // In a real application, you would send this to the server
                alert('Thank you for your message! We will get back to you soon.');
                contactForm.reset();
            } else {
                alert('Please fill in all fields with valid information.');
            }
        });
    }
});

// ========================================
// Smooth Scroll for Anchor Links
// ========================================
document.addEventListener('click', function(e) {
    if (e.target.tagName === 'A' && e.target.getAttribute('href') && e.target.getAttribute('href').startsWith('#')) {
        e.preventDefault();
        const targetId = e.target.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});
