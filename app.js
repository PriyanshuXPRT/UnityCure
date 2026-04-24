// ===== INIT LUCIDE ICONS =====
document.addEventListener('DOMContentLoaded', () => {
  lucide.createIcons();
  initNavigation();
  initLoginForm();
  initSignupForm();
  initPasswordToggles();
  initPasswordStrength();
});

// ===== HELPERS =====
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

function showError(groupId, errorId, message) {
  const group = document.getElementById(groupId);
  const error = document.getElementById(errorId);
  const wrapper = group?.querySelector('.input-wrapper');
  if (wrapper) wrapper.classList.add('error');
  if (error) error.textContent = message;
}

function clearError(groupId, errorId) {
  const group = document.getElementById(groupId);
  const error = document.getElementById(errorId);
  const wrapper = group?.querySelector('.input-wrapper');
  if (wrapper) wrapper.classList.remove('error');
  if (error) error.textContent = '';
}

function clearAllErrors(prefix, fields) {
  fields.forEach(f => clearError(`${prefix}-${f}-group`, `${prefix}-${f}-error`));
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// ===== TOAST =====
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;

  const iconName = type === 'success' ? 'check-circle-2' : 'alert-circle';
  const iconColor = type === 'success' ? 'var(--success)' : 'var(--danger)';

  toast.innerHTML = `<i data-lucide="${iconName}" style="color:${iconColor};width:20px;height:20px;"></i><span>${message}</span>`;
  container.appendChild(toast);
  lucide.createIcons({ nodes: [toast] });

  setTimeout(() => {
    toast.classList.add('toast-exit');
    toast.addEventListener('animationend', () => toast.remove());
  }, 3500);
}

// ===== PAGE NAVIGATION =====
function initNavigation() {
  $('#goto-signup').addEventListener('click', (e) => {
    e.preventDefault();
    switchPage('signup-page');
  });
  $('#goto-login').addEventListener('click', (e) => {
    e.preventDefault();
    switchPage('login-page');
  });
}

function switchPage(targetId) {
  $$('.page').forEach(p => p.classList.remove('active'));
  const target = document.getElementById(targetId);
  target.classList.remove('active');
  // Force reflow so animation replays
  void target.offsetWidth;
  target.classList.add('active');
}

// ===== PASSWORD TOGGLE =====
function initPasswordToggles() {
  $$('.toggle-password').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.dataset.target;
      const input = document.getElementById(targetId);
      const eyeOpen = btn.querySelector('.eye-icon');
      const eyeOff = btn.querySelector('.eye-off-icon');

      if (input.type === 'password') {
        input.type = 'text';
        eyeOpen.classList.add('hidden');
        eyeOff.classList.remove('hidden');
      } else {
        input.type = 'password';
        eyeOpen.classList.remove('hidden');
        eyeOff.classList.add('hidden');
      }
    });
  });
}

// ===== PASSWORD STRENGTH =====
function initPasswordStrength() {
  const pwInput = $('#signup-password');
  if (!pwInput) return;

  pwInput.addEventListener('input', () => {
    const val = pwInput.value;
    const fill = $('#strength-fill');
    const label = $('#strength-label');
    if (!fill || !label) return;

    let score = 0;
    if (val.length >= 8) score++;
    if (/[A-Z]/.test(val)) score++;
    if (/[0-9]/.test(val)) score++;
    if (/[^A-Za-z0-9]/.test(val)) score++;

    const levels = [
      { width: '0%',   color: 'transparent',    text: '' },
      { width: '25%',  color: 'var(--danger)',   text: 'Weak' },
      { width: '50%',  color: 'var(--warning)',  text: 'Fair' },
      { width: '75%',  color: 'var(--primary)',  text: 'Good' },
      { width: '100%', color: 'var(--success)',  text: 'Strong' },
    ];

    const level = val.length === 0 ? levels[0] : levels[score] || levels[1];
    fill.style.width = level.width;
    fill.style.background = level.color;
    label.textContent = level.text;
    label.style.color = level.color;
  });
}

// ===== LOGIN FORM =====
function initLoginForm() {
  const form = $('#login-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearAllErrors('login', ['email', 'password', 'role']);

    const email = $('#login-email').value.trim();
    const password = $('#login-password').value;
    const role = $('#login-role').value;
    let valid = true;

    if (!email) {
      showError('login-email-group', 'login-email-error', 'Email is required');
      valid = false;
    } else if (!isValidEmail(email)) {
      showError('login-email-group', 'login-email-error', 'Please enter a valid email');
      valid = false;
    }

    if (!password) {
      showError('login-password-group', 'login-password-error', 'Password is required');
      valid = false;
    } else if (password.length < 6) {
      showError('login-password-group', 'login-password-error', 'Password must be at least 6 characters');
      valid = false;
    }

    if (!role) {
      showError('login-role-group', 'login-role-error', 'Please select your role');
      valid = false;
    }

    if (valid) {
      const btn = $('#login-submit-btn');
      btn.querySelector('.btn-text').classList.add('hidden');
      btn.querySelector('.btn-loader').classList.remove('hidden');
      btn.disabled = true;

      try {
        const response = await fetch('http://127.0.0.1:8000/api/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
          // Check if the user's role matches their selected role in the UI
          if (data.user.role !== role) {
             showError('login-role-group', 'login-role-error', `You are registered as a ${data.user.role}, not a ${role}.`);
             showToast('Role mismatch. Please select the correct role.', 'error');
          } else {
             showToast(`Welcome back! Signed in as ${role}.`, 'success');
             
             // Save user info for dashboard
             localStorage.setItem('unitycare_user', JSON.stringify(data.user));
             
             // Redirect based on role
             setTimeout(() => {
                 if (role === 'patient') {
                     window.location.href = 'patient-dashboard.html';
                 } else if (role === 'doctor') {
                     window.location.href = 'doctor-dashboard.html';
                 }
             }, 800);
          }
        } else {
           // Display error from API
           let errorMsg = 'Login failed.';
           if (data.non_field_errors) {
              errorMsg = data.non_field_errors[0];
           } else if (data.email) {
              errorMsg = data.email[0];
           }
           showToast(errorMsg, 'error');
        }
      } catch (error) {
        console.error('Login error:', error);
        showToast('Network error. Please try again later.', 'error');
      } finally {
        btn.querySelector('.btn-text').classList.remove('hidden');
        btn.querySelector('.btn-loader').classList.add('hidden');
        btn.disabled = false;
      }
    }
  });

  // Live clear errors on input
  $('#login-email').addEventListener('input', () => clearError('login-email-group', 'login-email-error'));
  $('#login-password').addEventListener('input', () => clearError('login-password-group', 'login-password-error'));
  $('#login-role').addEventListener('change', () => clearError('login-role-group', 'login-role-error'));
}

// ===== SIGNUP FORM =====
function initSignupForm() {
  const form = $('#signup-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearAllErrors('signup', ['name', 'email', 'password', 'confirm', 'role', 'terms']);

    const name = $('#signup-name').value.trim();
    const email = $('#signup-email').value.trim();
    const password = $('#signup-password').value;
    const confirm = $('#signup-confirm').value;
    const role = document.querySelector('input[name="signup-role"]:checked');
    const terms = $('#signup-terms').checked;
    let valid = true;

    if (!name) {
      showError('signup-name-group', 'signup-name-error', 'Full name is required');
      valid = false;
    } else if (name.length < 2) {
      showError('signup-name-group', 'signup-name-error', 'Name must be at least 2 characters');
      valid = false;
    }

    if (!email) {
      showError('signup-email-group', 'signup-email-error', 'Email is required');
      valid = false;
    } else if (!isValidEmail(email)) {
      showError('signup-email-group', 'signup-email-error', 'Please enter a valid email');
      valid = false;
    }

    if (!password) {
      showError('signup-password-group', 'signup-password-error', 'Password is required');
      valid = false;
    } else if (password.length < 8) {
      showError('signup-password-group', 'signup-password-error', 'Password must be at least 8 characters');
      valid = false;
    }

    if (!confirm) {
      showError('signup-confirm-group', 'signup-confirm-error', 'Please confirm your password');
      valid = false;
    } else if (password !== confirm) {
      showError('signup-confirm-group', 'signup-confirm-error', 'Passwords do not match');
      valid = false;
    }

    if (!role) {
      showError('signup-role-group', 'signup-role-error', 'Please select a role');
      valid = false;
    }

    if (!terms) {
      showError('signup-terms-group', 'signup-terms-error', 'You must agree to the terms');
      valid = false;
    }

    if (valid) {
      const btn = $('#signup-submit-btn');
      btn.querySelector('.btn-text').classList.add('hidden');
      btn.querySelector('.btn-loader').classList.remove('hidden');
      btn.disabled = true;

      try {
        const response = await fetch('http://127.0.0.1:8000/api/signup/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ name, email, password, role: role.value })
        });

        const data = await response.json();

        if (response.ok) {
          showToast(`Account created! Welcome, ${name}.`, 'success');
          form.reset();
          // Reset strength bar
          const fill = $('#strength-fill');
          const label = $('#strength-label');
          if (fill) fill.style.width = '0%';
          if (label) label.textContent = '';
          
          // Switch to login page after a brief delay
          setTimeout(() => {
            switchPage('login-page');
            $('#login-email').value = email;
            $('#login-role').value = role.value;
          }, 1500);
        } else {
           // Display error from API
           let errorMsg = 'Signup failed.';
           if (data.email) {
              errorMsg = `Email error: ${data.email[0]}`;
              showError('signup-email-group', 'signup-email-error', data.email[0]);
           } else if (data.non_field_errors) {
              errorMsg = data.non_field_errors[0];
           }
           showToast(errorMsg, 'error');
        }
      } catch (error) {
        console.error('Signup error:', error);
        showToast('Network error. Please try again later.', 'error');
      } finally {
        btn.querySelector('.btn-text').classList.remove('hidden');
        btn.querySelector('.btn-loader').classList.add('hidden');
        btn.disabled = false;
      }
    }
  });

  // Live clear errors on input
  $('#signup-name').addEventListener('input', () => clearError('signup-name-group', 'signup-name-error'));
  $('#signup-email').addEventListener('input', () => clearError('signup-email-group', 'signup-email-error'));
  $('#signup-password').addEventListener('input', () => clearError('signup-password-group', 'signup-password-error'));
  $('#signup-confirm').addEventListener('input', () => clearError('signup-confirm-group', 'signup-confirm-error'));
  $$('input[name="signup-role"]').forEach(r => r.addEventListener('change', () => clearError('signup-role-group', 'signup-role-error')));
  $('#signup-terms').addEventListener('change', () => clearError('signup-terms-group', 'signup-terms-error'));
}
