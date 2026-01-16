// Main JavaScript file for School Management System

document.addEventListener('DOMContentLoaded', function () {
    // Initialize components
    initDropdowns();
    initAlerts();
    initFormValidation();
    initDeleteConfirmation();
    initAttendanceButtons();
    initPasswordToggle();
    initRegistrationValidation();
});

// Dropdown functionality
function initDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', function (e) {
            e.stopPropagation();
            this.classList.toggle('active');
        });
    });

    document.addEventListener('click', function () {
        dropdowns.forEach(dropdown => {
            dropdown.classList.remove('active');
        });
    });
}

// Auto-dismiss alerts
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
}

// Form validation
function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                    showFieldError(field, 'This field is required');
                } else {
                    field.classList.remove('error');
                    removeFieldError(field);
                }
            });

            // Email validation
            const emailFields = form.querySelectorAll('input[type="email"]');
            emailFields.forEach(field => {
                if (field.value && !isValidEmail(field.value)) {
                    isValid = false;
                    field.classList.add('error');
                    showFieldError(field, 'Please enter a valid email');
                }
            });

            if (!isValid) {
                e.preventDefault();
            }
        });
    });
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showFieldError(field, message) {
    removeFieldError(field);
    const error = document.createElement('span');
    error.className = 'field-error';
    error.textContent = message;
    error.style.cssText = 'color: #ef4444; font-size: 0.75rem; margin-top: 0.25rem; display: block;';
    field.parentNode.appendChild(error);
}

function removeFieldError(field) {
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
}

// Delete confirmation
function initDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll('[data-delete]');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
}

// Attendance buttons
function initAttendanceButtons() {
    const statusBtns = document.querySelectorAll('.status-btn');

    statusBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const parent = this.closest('.attendance-status');
            const input = parent.querySelector('input[type="hidden"]') ||
                parent.closest('.attendance-item').querySelector('input[type="hidden"]');

            parent.querySelectorAll('.status-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            if (input) {
                input.value = this.dataset.status;
            }
        });
    });
}

// Mobile menu toggle
function toggleMobileMenu() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('mobile-active');
    }
}

// Loading state for buttons
function setLoading(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        button.dataset.originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    } else {
        button.disabled = false;
        button.innerHTML = button.dataset.originalText;
    }
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-IN', options);
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

// Print functionality
function printSection(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
        <head>
            <title>Print</title>
            <link rel="stylesheet" href="/static/css/style.css">
            <style>
                body { padding: 2rem; }
                .no-print { display: none !important; }
            </style>
        </head>
        <body>
            ${element.innerHTML}
        </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

// Search functionality
function initSearch(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);

    if (!input || !table) return;

    input.addEventListener('input', function () {
        const searchTerm = this.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
}

// Password toggle functionality
function initPasswordToggle() {
    const toggleIcons = document.querySelectorAll('.toggle-password');

    toggleIcons.forEach(icon => {
        icon.addEventListener('click', function () {
            const targetId = this.dataset.target;
            const passwordInput = document.getElementById(targetId);

            if (passwordInput) {
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    this.classList.remove('fa-eye');
                    this.classList.add('fa-eye-slash');
                } else {
                    passwordInput.type = 'password';
                    this.classList.remove('fa-eye-slash');
                    this.classList.add('fa-eye');
                }
            }
        });
    });
}

// Registration form validation
function initRegistrationValidation() {
    const registerForm = document.querySelector('.register-form');

    if (!registerForm) return;

    registerForm.addEventListener('submit', function (e) {
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm_password');

        if (password && confirmPassword) {
            if (password.value !== confirmPassword.value) {
                e.preventDefault();
                showFieldError(confirmPassword, 'Passwords do not match');
                confirmPassword.classList.add('error');
                return false;
            }

            if (password.value.length < 6) {
                e.preventDefault();
                showFieldError(password, 'Password must be at least 6 characters long');
                password.classList.add('error');
                return false;
            }
        }
    });

    // Real-time password match validation
    const confirmPassword = document.getElementById('confirm_password');
    if (confirmPassword) {
        confirmPassword.addEventListener('input', function () {
            const password = document.getElementById('password');
            if (password && this.value) {
                if (password.value !== this.value) {
                    this.classList.add('error');
                    showFieldError(this, 'Passwords do not match');
                } else {
                    this.classList.remove('error');
                    removeFieldError(this);
                }
            }
        });
    }
}
