// Enhanced Toast notification system
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    
    // Create toast container if it doesn't exist
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span class="toast-text">${message}</span>
        <button class="toast-close" aria-label="Close notification" type="button">&times;</button>
    `;
    
    // Add to container
    document.getElementById('toast-container').appendChild(toast);
    
    // Trigger animation
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);
    
    // Auto remove after 6 seconds
    const autoRemove = setTimeout(() => {
        removeToast(toast);
    }, 6000);
    
    // Close button functionality
    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => {
        clearTimeout(autoRemove);
        removeToast(toast);
    });
    
    // Remove toast function
    function removeToast(toastElement) {
        toastElement.classList.add('removing');
        setTimeout(() => {
            if (toastElement.parentNode) {
                toastElement.parentNode.removeChild(toastElement);
            }
        }, 400);
    }
    
    // Add hover pause functionality
    toast.addEventListener('mouseenter', () => {
        clearTimeout(autoRemove);
    });
    
    toast.addEventListener('mouseleave', () => {
        setTimeout(() => {
            removeToast(toast);
        }, 6000);
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
            // Debug: Log the actual response structure
            console.log('Error response data:', data);
            
            // Handle Django REST Framework validation errors
            let errorMessage = 'Something went wrong';
            
            if (data.error) {
                // Direct error message
                errorMessage = data.error;
            } else if (typeof data === 'object') {
                // Django REST Framework validation errors
                const errorMessages = [];
                for (const field in data) {
                    if (Array.isArray(data[field])) {
                        // Extract the actual error message from ErrorDetail objects
                        data[field].forEach(error => {
                            if (typeof error === 'string') {
                                errorMessages.push(error);
                            } else if (error && error.string) {
                                // Handle ErrorDetail objects
                                errorMessages.push(error.string);
                            } else if (error && typeof error === 'object') {
                                // Fallback for other error object types
                                errorMessages.push(JSON.stringify(error));
                            }
                        });
                    } else if (typeof data[field] === 'string') {
                        errorMessages.push(data[field]);
                    }
                }
                if (errorMessages.length > 0) {
                    errorMessage = errorMessages.join('. ');
                }
            }
            
            throw new Error(errorMessage);
        }
        
        return data;
    } catch (error) {
        // Debug: Log the error structure
        console.log('Caught error:', error);
        console.log('Error message:', error.message);
        
        // Don't show toast here, let the calling function handle it
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
                        <strong>Price:</strong> ₹${option.price}<br>
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
            window.location.href = '/bookings/';
        }, 2000);
    } catch (error) {
        console.error('Booking failed:', error);
        
        // Handle different error types
        let errorMessage = 'Booking failed. Please try again.';
        
        if (error.message) {
            // Check if it's a Django ErrorDetail string
            if (error.message.includes('ErrorDetail')) {
                // Extract the actual message from ErrorDetail
                const match = error.message.match(/string='([^']+)'/);
                if (match) {
                    errorMessage = match[1];
                } else {
                    errorMessage = error.message;
                }
            } else {
                errorMessage = error.message;
            }
        }
        
        showToast(errorMessage, 'error');
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
        // Show the specific error message from the backend
        if (error.message) {
            showToast(error.message, 'error');
        } else {
            showToast('Cancellation failed. Please try again.', 'error');
        }
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

// Booking Details Page Functions
function initializeBookingDetails() {
    // Get booking ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const bookingId = urlParams.get('id');

    if (bookingId) {
        loadBookingDetails(bookingId);
    } else {
        showError('No booking ID provided');
    }
}

// Load booking details
async function loadBookingDetails(bookingId) {
    try {
        showLoading(true);
        const data = await makeRequest(`/api/bookings/${bookingId}/`);
        displayBookingDetails(data);
    } catch (error) {
        console.error('Failed to load booking details:', error);
        showError('Failed to load booking details');
    } finally {
        showLoading(false);
    }
}

// Display booking details
function displayBookingDetails(booking) {
    const detailsContainer = document.getElementById('booking-details');
    const errorContainer = document.getElementById('error-message');
    
    if (!detailsContainer || !errorContainer) return;
    
    detailsContainer.style.display = 'block';
    errorContainer.style.display = 'none';
    
    // Update status banner
    updateStatusBanner(booking.status);
    
    // Update travel information
    updateTravelInfo(booking.travel_option);
    
    // Update booking summary
    updateBookingSummary(booking);
    
    // Update passenger details
    displayPassengers(booking.passenger_details);
    
    // Update actions
    displayActions(booking);
    
    // Start countdown if booking is confirmed
    if (booking.status === 'confirmed') {
        startCountdown(booking.travel_option.departure_date, booking.travel_option.departure_time);
    }
}

// Update status banner
function updateStatusBanner(status) {
    const banner = document.getElementById('status-banner');
    if (!banner) return;
    
    let alertClass = 'alert-info';
    let icon = 'fas fa-info-circle';
    
    switch(status) {
        case 'confirmed':
            alertClass = 'alert-success';
            icon = 'fas fa-check-circle';
            break;
        case 'pending':
            alertClass = 'alert-warning';
            icon = 'fas fa-clock';
            break;
        case 'cancelled':
            alertClass = 'alert-danger';
            icon = 'fas fa-times-circle';
            break;
    }
    
    banner.className = `alert ${alertClass}`;
    banner.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="${icon} me-2"></i>
            <div>
                <strong>Booking Status:</strong> 
                <span class="badge bg-${getStatusColor(status)} ms-2">${status.toUpperCase()}</span>
            </div>
        </div>
    `;
}

// Update travel information
function updateTravelInfo(travelOption) {
    const sourceCity = document.getElementById('source-city');
    const destinationCity = document.getElementById('destination-city');
    const departureDateTime = document.getElementById('departure-datetime');
    const arrivalDateTime = document.getElementById('arrival-datetime');
    const travelType = document.getElementById('travel-type');
    const operatorName = document.getElementById('operator-name');
    const travelDuration = document.getElementById('travel-duration');
    
    if (sourceCity) sourceCity.textContent = travelOption.source;
    if (destinationCity) destinationCity.textContent = travelOption.destination;
    if (departureDateTime) departureDateTime.textContent = formatDateTime(travelOption.departure_date, travelOption.departure_time);
    if (arrivalDateTime) arrivalDateTime.textContent = formatDateTime(travelOption.arrival_date, travelOption.arrival_time);
    if (travelType) travelType.textContent = travelOption.type.toUpperCase();
    if (operatorName) operatorName.textContent = travelOption.operator_name;
    if (travelDuration) travelDuration.textContent = formatDuration(travelOption.duration);
}

// Update booking summary
function updateBookingSummary(booking) {
    const bookingReference = document.getElementById('booking-reference');
    const bookingDate = document.getElementById('booking-date');
    const passengerCount = document.getElementById('passenger-count');
    const pricePerTicket = document.getElementById('price-per-ticket');
    const totalPrice = document.getElementById('total-price');
    
    if (bookingReference) bookingReference.textContent = booking.reference_number;
    if (bookingDate) bookingDate.textContent = formatDate(booking.booking_date);
    if (passengerCount) passengerCount.textContent = booking.number_of_seats;
    if (pricePerTicket) pricePerTicket.textContent = formatPriceINR(booking.travel_option.price);
    if (totalPrice) totalPrice.textContent = formatPriceINR(booking.total_price);
}

// Display passengers
function displayPassengers(passengerDetails) {
    const container = document.getElementById('passengers-list');
    if (!container) return;
    
    if (!passengerDetails || !Array.isArray(passengerDetails)) {
        container.innerHTML = '<p class="text-muted">No passenger details available</p>';
        return;
    }
    
    const html = passengerDetails.map((passenger, index) => `
        <div class="passenger-item border rounded p-3 mb-3">
            <div class="d-flex justify-content-between align-items-start mb-2">
                <h6 class="mb-0">Passenger ${index + 1}</h6>
                <span class="badge bg-primary">${passenger.age || 'N/A'} years</span>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <label class="text-muted small">Name</label>
                    <p class="mb-2 fw-bold">${passenger.name || 'N/A'}</p>
                </div>
                <div class="col-md-6">
                    <label class="text-muted small">ID Number</label>
                    <p class="mb-2 fw-bold">${passenger.id_number || 'N/A'}</p>
                </div>
            </div>
            ${passenger.special_requirements ? `
                <div>
                    <label class="text-muted small">Special Requirements</label>
                    <p class="mb-0 text-info">${passenger.special_requirements}</p>
                </div>
            ` : ''}
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// Display actions
function displayActions(booking) {
    const container = document.getElementById('booking-actions');
    if (!container) return;
    
    let actionsHtml = '';
    
    if (booking.status === 'confirmed') {
        actionsHtml += `
            <button class="btn btn-danger w-100 mb-2" onclick="cancelBooking(${booking.booking_id})">
                <i class="fas fa-times me-2"></i>Cancel Booking
            </button>
        `;
    }
    
    actionsHtml += `
        <button class="btn btn-outline-primary w-100 mb-2" onclick="downloadTicket(${booking.booking_id})">
            <i class="fas fa-download me-2"></i>Download Ticket
        </button>
        <button class="btn btn-outline-secondary w-100" onclick="shareBooking()">
            <i class="fas fa-share me-2"></i>Share Booking
        </button>
    `;
    
    container.innerHTML = actionsHtml;
}

// Start countdown timer
function startCountdown(departureDate, departureTime) {
    const countdownSection = document.getElementById('countdown-section');
    const countdownTimer = document.getElementById('countdown-timer');
    
    if (!countdownSection || !countdownTimer) return;
    
    countdownSection.style.display = 'block';
    
    function updateCountdown() {
        const now = new Date();
        const departure = new Date(`${departureDate}T${departureTime}`);
        const diff = departure - now;
        
        if (diff <= 0) {
            countdownTimer.innerHTML = '<span class="text-danger">DEPARTED</span>';
            return;
        }
        
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);
        
        let countdownText = '';
        if (days > 0) countdownText += `${days}d `;
        if (hours > 0) countdownText += `${hours}h `;
        countdownText += `${minutes}m ${seconds}s`;
        
        countdownTimer.textContent = countdownText;
    }
    
    updateCountdown();
    setInterval(updateCountdown, 1000);
}

// Action functions
function downloadTicket(bookingId) {
    showToast('Download feature will be implemented soon', 'info');
}

function shareBooking() {
    if (navigator.share) {
        navigator.share({
            title: 'My Travel Booking',
            text: 'Check out my travel booking details',
            url: window.location.href
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(window.location.href)
            .then(() => showToast('Booking URL copied to clipboard', 'success'))
            .catch(() => showToast('Failed to copy URL', 'error'));
    }
}

function printBooking() {
    window.print();
}

// Show/hide functions for booking details
function showLoading(show) {
    const spinner = document.getElementById('loading-spinner');
    const details = document.getElementById('booking-details');
    const error = document.getElementById('error-message');
    
    if (!spinner || !details || !error) return;
    
    if (show) {
        spinner.style.display = 'block';
        details.style.display = 'none';
        error.style.display = 'none';
    } else {
        spinner.style.display = 'none';
    }
}

function showError(message) {
    const spinner = document.getElementById('loading-spinner');
    const details = document.getElementById('booking-details');
    const error = document.getElementById('error-message');
    
    if (!spinner || !details || !error) return;
    
    spinner.style.display = 'none';
    details.style.display = 'none';
    error.style.display = 'block';
    
    if (message) {
        const errorTitle = error.querySelector('h4');
        if (errorTitle) errorTitle.textContent = message;
    }
}

// Helper functions for booking details
function formatPriceINR(price) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(price);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatDateTime(dateString, timeString) {
    const date = new Date(`${dateString}T${timeString}`);
    return date.toLocaleString('en-IN', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatDuration(durationString) {
    if (!durationString) return 'N/A';
    
    const duration = durationString.split(':');
    const hours = parseInt(duration[0]);
    const minutes = parseInt(duration[1]);
    
    let result = '';
    if (hours > 0) result += `${hours}h `;
    if (minutes > 0) result += `${minutes}m`;
    
    return result.trim();
}

function getStatusColor(status) {
    switch(status) {
        case 'confirmed': return 'success';
        case 'pending': return 'warning';
        case 'cancelled': return 'danger';
        default: return 'secondary';
    }
}

// Initialize booking details page
function initializeBookingDetailsPage() {
    // Check if we're on the booking details page
    if (window.location.pathname.includes('booking-details')) {
        initializeBookingDetails();
    }
}

// View booking details - Navigate to booking details page
function viewBookingDetails(bookingId) {
    window.location.href = `/booking-details/?id=${bookingId}`;
}

// Footer functionality
function initializeFooter() {
    // Add scroll-to-top functionality
    const footer = document.querySelector('.main-footer');
    if (footer) {
        // Add scroll-to-top button
        const scrollToTopBtn = document.createElement('button');
        scrollToTopBtn.className = 'scroll-to-top-btn';
        scrollToTopBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
        scrollToTopBtn.setAttribute('aria-label', 'Scroll to top');
        document.body.appendChild(scrollToTopBtn);
        
        // Show/hide scroll-to-top button
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                scrollToTopBtn.classList.add('show');
            } else {
                scrollToTopBtn.classList.remove('show');
            }
        });
        
        // Scroll to top functionality
        scrollToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        // Add hover effects to footer links
        const footerLinks = document.querySelectorAll('.footer-links a');
        footerLinks.forEach(link => {
            link.addEventListener('mouseenter', function() {
                this.style.transform = 'translateX(5px)';
            });
            
            link.addEventListener('mouseleave', function() {
                this.style.transform = 'translateX(0)';
            });
        });
        
        // Add animation to social links
        const socialLinks = document.querySelectorAll('.social-link');
        socialLinks.forEach((link, index) => {
            link.style.animationDelay = `${index * 0.1}s`;
            link.classList.add('animate-social');
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeAuthForms();
    initializeNavbar();
    initializeSearch();
    initializeBookingDetailsPage();
    initializeFooter(); // Add footer initialization
    
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
