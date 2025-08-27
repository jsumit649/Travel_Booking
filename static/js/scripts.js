// Toast notification system
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type} show`;
    toast.innerHTML = `
        <span class="toast-text">${message}</span>
        <button class="toast-close" aria-label="Close notification" type="button">&times;</button>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
    
    // Close button functionality
    toast.querySelector('.toast-close').addEventListener('click', () => {
        toast.remove();
    });
}

// Form validation
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// AJAX helper function
async function makeRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Something went wrong');
        }
        
        return data;
    } catch (error) {
        showToast(error.message, 'error');
        throw error;
    }
}

// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Search functionality
function initializeSearch() {
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(searchForm);
            const params = new URLSearchParams();
            
            for (let [key, value] of formData.entries()) {
                if (value) params.append(key, value);
            }
            
            try {
                const data = await makeRequest(`/api/travel-search/?${params}`);
                displaySearchResults(data.results || data);
            } catch (error) {
                console.error('Search failed:', error);
            }
        });
    }
}

// Display search results
function displaySearchResults(results) {
    const resultsContainer = document.getElementById('search-results');
    if (!resultsContainer) return;
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p class="text-center">No travel options found.</p>';
        return;
    }
    
    const html = results.map(option => `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">${option.type.toUpperCase()} - ${option.operator_name}</h5>
                    <p class="card-text">
                        <strong>From:</strong> ${option.source}<br>
                        <strong>To:</strong> ${option.destination}<br>
                        <strong>Date:</strong> ${option.departure_date}<br>
                        <strong>Time:</strong> ${option.departure_time}<br>
                        <strong>Price:</strong> $${option.price}<br>
                        <strong>Available Seats:</strong> ${option.available_seats}
                    </p>
                    <button class="btn btn-primary" onclick="bookTravel(${option.travel_id})">
                        Book Now
                    </button>
                </div>
            </div>
        </div>
    `).join('');
    
    resultsContainer.innerHTML = html;
}

// Booking functionality
async function bookTravel(travelId) {
    if (!confirm('Are you sure you want to book this travel option?')) {
        return;
    }
    
    const numberOfSeats = prompt('Enter number of seats:');
    if (!numberOfSeats || isNaN(numberOfSeats)) {
        showToast('Please enter a valid number of seats', 'error');
        return;
    }
    
    const passengerDetails = [];
    for (let i = 0; i < numberOfSeats; i++) {
        const name = prompt(`Enter passenger ${i + 1} name:`);
        const age = prompt(`Enter passenger ${i + 1} age:`);
        if (!name || !age) {
            showToast('Please provide all passenger details', 'error');
            return;
        }
        passengerDetails.push({ name, age });
    }
    
    try {
        const data = await makeRequest('/api/bookings/', {
            method: 'POST',
            body: JSON.stringify({
                travel_option: travelId,
                number_of_seats: parseInt(numberOfSeats),
                passenger_details: passengerDetails
            })
        });
        
        showToast('Booking created successfully!', 'success');
        setTimeout(() => {
            window.location.href = '/api/bookings/';
        }, 2000);
    } catch (error) {
        console.error('Booking failed:', error);
    }
}

// Cancel booking
async function cancelBooking(bookingId) {
    if (!confirm('Are you sure you want to cancel this booking?')) {
        return;
    }
    
    try {
        await makeRequest(`/api/bookings/${bookingId}/cancel/`, {
            method: 'POST'
        });
        
        showToast('Booking cancelled successfully!', 'success');
        setTimeout(() => {
            window.location.reload();
        }, 2000);
    } catch (error) {
        console.error('Cancellation failed:', error);
    }
}

// Navbar scroll effect
function initializeNavbar() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Add smooth scrolling to navbar links
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Password toggle functionality
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(inputId + '-icon');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Password strength checker
function checkPasswordStrength(password) {
    const strengthDiv = document.getElementById('password-strength');
    if (!strengthDiv) return;
    
    let strength = 0;
    let feedback = '';
    
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    switch (strength) {
        case 0:
        case 1:
            feedback = 'Very Weak';
            strengthDiv.className = 'password-strength weak';
            break;
        case 2:
            feedback = 'Weak';
            strengthDiv.className = 'password-strength weak';
            break;
        case 3:
            feedback = 'Medium';
            strengthDiv.className = 'password-strength medium';
            break;
        case 4:
            feedback = 'Strong';
            strengthDiv.className = 'password-strength strong';
            break;
        case 5:
            feedback = 'Very Strong';
            strengthDiv.className = 'password-strength strong';
            break;
    }
    
    strengthDiv.textContent = feedback;
}

// Password confirmation checker
function checkPasswordMatch() {
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    
    if (password1 && password2) {
        if (password2.value && password1.value !== password2.value) {
            password2.setCustomValidity('Passwords do not match');
        } else {
            password2.setCustomValidity('');
        }
    }
}

// Initialize authentication forms
function initializeAuthForms() {
    // Password strength checker
    const password1 = document.getElementById('password1');
    if (password1) {
        password1.addEventListener('input', function() {
            checkPasswordStrength(this.value);
        });
    }
    
    // Password confirmation checker
    const password2 = document.getElementById('password2');
    if (password2) {
        password2.addEventListener('input', checkPasswordMatch);
    }
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeAuthForms();
    initializeNavbar();
    initializeSearch();
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!validateForm(form)) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});
