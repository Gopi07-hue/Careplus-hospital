/**
 * CarePlus Hospital - Interactive Frontend Engine
 * Modern, responsive hospital web application
 */

document.addEventListener('DOMContentLoaded', () => {

  // ==========================================================================
  // 1. THEME SWITCHER (Dark Mode & Light Mode)
  // ==========================================================================
  const darkToggleBtn = document.getElementById('darkToggleBtn');
  const currentTheme = localStorage.getItem('careplus_theme') || 'light';

  if (currentTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    if (darkToggleBtn) darkToggleBtn.innerHTML = '<i class="fa-solid fa-sun"></i> Light';
  }

  if (darkToggleBtn) {
    darkToggleBtn.addEventListener('click', () => {
      const theme = document.documentElement.getAttribute('data-theme');
      if (theme === 'dark') {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('careplus_theme', 'light');
        darkToggleBtn.innerHTML = '<i class="fa-solid fa-moon"></i> Dark';
      } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('careplus_theme', 'dark');
        darkToggleBtn.innerHTML = '<i class="fa-solid fa-sun"></i> Light';
      }
    });
  }

  // ==========================================================================
  // 2. MOBILE NAVIGATION MENU
  // ==========================================================================
  const mobileNavToggle = document.getElementById('mobileNavToggle');
  const navMenu = document.getElementById('navMenu');

  if (mobileNavToggle && navMenu) {
    mobileNavToggle.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      const icon = mobileNavToggle.querySelector('i');
      if (icon) {
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-xmark');
      }
    });

    // Close mobile menu on link click
    navMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        const icon = mobileNavToggle.querySelector('i');
        if (icon) {
          icon.classList.add('fa-bars');
          icon.classList.remove('fa-xmark');
        }
      });
    });
  }

  // ==========================================================================
  // 3. ANIMATED STATISTICS COUNTER
  // ==========================================================================
  const counters = document.querySelectorAll('.counter-val');
  let animated = false;

  const countUp = () => {
    counters.forEach(counter => {
      const target = +counter.getAttribute('data-target');
      const duration = 2000;
      const step = Math.ceil(target / (duration / 25));
      let current = 0;

      const timer = setInterval(() => {
        current += step;
        if (current >= target) {
          counter.textContent = target.toLocaleString();
          clearInterval(timer);
        } else {
          counter.textContent = current.toLocaleString();
        }
      }, 25);
    });
  };

  const statsSection = document.getElementById('statistics');
  if (statsSection) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !animated) {
          animated = true;
          countUp();
        }
      });
    }, { threshold: 0.3 });

    observer.observe(statsSection);
  }

  // ==========================================================================
  // 4. LIVE HOSPITAL CLOCK
  // ==========================================================================
  const liveClockEl = document.getElementById('liveClock');
  const updateClock = () => {
    if (liveClockEl) {
      const now = new Date();
      liveClockEl.textContent = now.toLocaleTimeString('en-US', { hour12: false });
    }
  };
  setInterval(updateClock, 1000);
  updateClock();

  // ==========================================================================
  // 5. HEALTH CALCULATOR (BMI & Heart Rate)
  // ==========================================================================
  const btnCalcBMI = document.getElementById('btnCalcBMI');
  if (btnCalcBMI) {
    btnCalcBMI.addEventListener('click', () => {
      const weight = parseFloat(document.getElementById('bmiWeight').value);
      const height = parseFloat(document.getElementById('bmiHeight').value);
      const resultBox = document.getElementById('bmiResult');

      if (!weight || !height || weight <= 0 || height <= 0) {
        resultBox.innerHTML = '<span style="color:#ef4444;">Please enter valid weight and height.</span>';
        return;
      }

      const heightInMeters = height / 100;
      const bmi = (weight / (heightInMeters * heightInMeters)).toFixed(1);

      let status = '';
      let color = '';

      if (bmi < 18.5) {
        status = 'Underweight';
        color = '#3b82f6';
      } else if (bmi >= 18.5 && bmi <= 24.9) {
        status = 'Normal Weight (Healthy)';
        color = '#10b981';
      } else if (bmi >= 25 && bmi <= 29.9) {
        status = 'Overweight';
        color = '#f59e0b';
      } else {
        status = 'Obese';
        color = '#ef4444';
      }

      resultBox.innerHTML = `
        <div style="font-size:1.3rem; margin-bottom:4px;">BMI: <strong style="color:${color};">${bmi}</strong></div>
        <div style="color:${color}; font-size:0.95rem;">Category: <strong>${status}</strong></div>
      `;
    });
  }

  const btnCheckPulse = document.getElementById('btnCheckPulse');
  if (btnCheckPulse) {
    btnCheckPulse.addEventListener('click', () => {
      const pulse = parseInt(document.getElementById('heartPulse').value);
      const resultBox = document.getElementById('heartResult');

      if (!pulse || pulse <= 0) {
        resultBox.innerHTML = '<span style="color:#ef4444;">Please enter a valid pulse rate.</span>';
        return;
      }

      let status = '';
      let color = '';

      if (pulse < 60) {
        status = 'Resting Bradycardia (Low)';
        color = '#3b82f6';
      } else if (pulse >= 60 && pulse <= 100) {
        status = 'Normal Heart Rate (60-100 bpm)';
        color = '#10b981';
      } else {
        status = 'Tachycardia (Elevated / High)';
        color = '#ef4444';
      }

      resultBox.innerHTML = `
        <div style="font-size:1.3rem; margin-bottom:4px;">Pulse: <strong style="color:${color};">${pulse} BPM</strong></div>
        <div style="color:${color}; font-size:0.95rem;">Status: <strong>${status}</strong></div>
      `;
    });
  }

  // ==========================================================================
  // 6. HEALTH TIPS CAROUSEL
  // ==========================================================================
  const tips = [
    {
      icon: 'fa-droplet',
      title: 'Stay Hydrated Daily',
      text: 'Drinking 2.5 to 3 liters of water each day improves kidney function, aids cellular digestion, and keeps energy levels steady.'
    },
    {
      icon: 'fa-heart-pulse',
      title: 'Protect Your Heart Health',
      text: 'Just 30 minutes of brisk walking or moderate aerobic exercise reduces the risk of cardiovascular disease by up to 35%.'
    },
    {
      icon: 'fa-moon',
      title: 'Prioritize Restful Sleep',
      text: 'Aim for 7 to 8 hours of quality sleep. Deep restorative sleep enhances the immune system and regulates blood pressure.'
    },
    {
      icon: 'fa-apple-whole',
      title: 'Balanced Nutrition',
      text: 'Fill half your plate with colorful vegetables and fruits to supply essential antioxidants and natural fiber for gut health.'
    },
    {
      icon: 'fa-brain',
      title: 'Mental Wellbeing & Mindfulness',
      text: 'Take 5-minute breathing pauses during busy workdays to reduce cortisol levels and maintain focus and emotional balance.'
    }
  ];

  let currentTipIndex = 0;
  const tipSlideEl = document.getElementById('tipSlide');
  const tipDotsContainer = document.getElementById('tipDots');

  const renderTip = (index) => {
    if (!tipSlideEl) return;
    const item = tips[index];
    tipSlideEl.style.opacity = '0';
    setTimeout(() => {
      tipSlideEl.innerHTML = `
        <i class="fa-solid ${item.icon} tip-icon"></i>
        <h3 class="tip-title">${item.title}</h3>
        <p class="tip-text">${item.text}</p>
      `;
      tipSlideEl.style.opacity = '1';

      if (tipDotsContainer) {
        const dots = tipDotsContainer.querySelectorAll('.tip-dot');
        dots.forEach((dot, idx) => {
          dot.classList.toggle('active', idx === index);
        });
      }
    }, 200);
  };

  if (tipDotsContainer) {
    tipDotsContainer.innerHTML = '';
    tips.forEach((_, idx) => {
      const dot = document.createElement('div');
      dot.className = `tip-dot ${idx === 0 ? 'active' : ''}`;
      dot.addEventListener('click', () => {
        currentTipIndex = idx;
        renderTip(currentTipIndex);
      });
      tipDotsContainer.appendChild(dot);
    });
  }

  // Auto rotate tips
  setInterval(() => {
    currentTipIndex = (currentTipIndex + 1) % tips.length;
    renderTip(currentTipIndex);
  }, 4500);

  // ==========================================================================
  // 7. BOOK AMBULANCE FORM (AJAX)
  // ==========================================================================
  const ambulanceForm = document.getElementById('ambulanceForm');
  if (ambulanceForm) {
    ambulanceForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const patientName = document.getElementById('ambPatientName').value.trim();
      const phone = document.getElementById('ambPhone').value.trim();
      const location = document.getElementById('ambLocation').value.trim();
      const emergencyType = document.getElementById('ambType') ? document.getElementById('ambType').value : 'General Emergency';

      if (!patientName || !phone || !location) {
        alert('Please fill out all ambulance request fields.');
        return;
      }

      try {
        const response = await fetch('/api/book-ambulance', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            patient_name: patientName,
            phone: phone,
            location: location,
            emergency_type: emergencyType
          })
        });

        const data = await response.json();
        if (data.success) {
          showModal(`
            <div style="color:#ef4444; font-size:3.5rem; margin-bottom:15px;"><i class="fa-solid fa-truck-medical"></i></div>
            <h3 style="font-size:1.5rem; color:var(--heading-color); margin-bottom:10px;">Ambulance Request Dispatched</h3>
            <p style="margin-bottom:15px; color:var(--text-color);">Request ID: <strong>${data.request_id}</strong></p>
            <div style="background:rgba(239,68,68,0.1); border-radius:12px; padding:15px; margin-bottom:20px; text-align:left; font-size:0.92rem;">
              <p>📍 <strong>Pickup:</strong> ${location}</p>
              <p>⏱️ <strong>Estimated Arrival:</strong> ${data.eta}</p>
              <p>📞 <strong>Driver Contact:</strong> +91 98765 43210</p>
            </div>
            <p style="font-size:0.8rem; color:#64748b; font-style:italic;">Note: This is a demonstration booking confirmation. For real emergencies, dial local 108 or hospital emergency immediately.</p>
          `);
          ambulanceForm.reset();
        } else {
          alert(data.message || 'Error booking ambulance.');
        }
      } catch (err) {
        console.error(err);
        alert('Failed to connect to ambulance dispatch server.');
      }
    });
  }

  // ==========================================================================
  // 8. APPOINTMENT BOOKING FORM (AJAX)
  // ==========================================================================
  const appointmentForm = document.getElementById('appointmentForm');
  if (appointmentForm) {
    appointmentForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const patientName = document.getElementById('aptName').value.trim();
      const age = document.getElementById('aptAge').value.trim();
      const phone = document.getElementById('aptPhone').value.trim();
      const email = document.getElementById('aptEmail').value.trim();
      const department = document.getElementById('aptDept').value;
      const doctorName = document.getElementById('aptDoctor').value;
      const date = document.getElementById('aptDate').value;
      const time = document.getElementById('aptTime').value;
      const symptoms = document.getElementById('aptSymptoms').value.trim();

      if (!patientName || !phone || !department || !date || !time) {
        alert('Please fill in all mandatory appointment fields.');
        return;
      }

      try {
        const response = await fetch('/api/book-appointment', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            patient_name: patientName,
            age: age,
            phone: phone,
            email: email,
            department: department,
            doctor_name: doctorName,
            appointment_date: date,
            preferred_time: time,
            symptoms: symptoms
          })
        });

        const data = await response.json();
        if (data.success) {
          showModal(`
            <div style="color:#10b981; font-size:3.5rem; margin-bottom:15px;"><i class="fa-solid fa-circle-check"></i></div>
            <h3 style="font-size:1.5rem; color:var(--heading-color); margin-bottom:10px;">Appointment Confirmed!</h3>
            <p style="margin-bottom:15px; color:var(--text-color);">Reference ID: <strong>${data.booking_id}</strong></p>
            <div style="background:rgba(16,185,129,0.1); border-radius:12px; padding:15px; margin-bottom:20px; text-align:left; font-size:0.92rem;">
              <p>👤 <strong>Patient:</strong> ${patientName}</p>
              <p>🏥 <strong>Department:</strong> ${department}</p>
              <p>🩺 <strong>Doctor:</strong> ${doctorName || 'Assigned Consultant'}</p>
              <p>📅 <strong>Schedule:</strong> ${date} at ${time}</p>
            </div>
            <p style="font-size:0.85rem; color:var(--text-color);">A confirmation SMS has been prepared for ${phone}. Please arrive 15 minutes before your time slot.</p>
          `);
          appointmentForm.reset();
        } else {
          alert(data.message || 'Error booking appointment.');
        }
      } catch (err) {
        console.error(err);
        alert('Failed to connect to appointment booking server.');
      }
    });
  }

  // ==========================================================================
  // 9. QUICK ACCESS CARDS INTERACTION
  // ==========================================================================
  document.querySelectorAll('.quick-card').forEach(card => {
    card.addEventListener('click', () => {
      const action = card.getAttribute('data-action');
      if (action === 'appointment') {
        const target = document.getElementById('appointment');
        if (target) target.scrollIntoView({ behavior: 'smooth' });
      } else if (action === 'emergency') {
        const target = document.getElementById('ambulance');
        if (target) target.scrollIntoView({ behavior: 'smooth' });
      } else if (action === 'lab') {
        showModal(`
          <div style="color:var(--primary); font-size:3rem; margin-bottom:15px;"><i class="fa-solid fa-flask-vial"></i></div>
          <h3 style="font-size:1.4rem; color:var(--heading-color); margin-bottom:10px;">Online Lab Reports Portal</h3>
          <p style="margin-bottom:15px; color:var(--text-color);">Enter your Patient ID or Mobile Number to access your verified pathology and radiology reports securely.</p>
          <div style="margin-bottom:15px;">
            <input type="text" placeholder="Enter Patient ID (e.g. CP-1002)" class="form-control" style="margin-bottom:10px;">
            <button class="btn btn-primary" style="width:100%;" onclick="alert('Demo: Report CP-1002 is verified and ready for download.')">Search Report</button>
          </div>
        `);
      } else if (action === 'pharmacy') {
        showModal(`
          <div style="color:var(--primary); font-size:3rem; margin-bottom:15px;"><i class="fa-solid fa-capsules"></i></div>
          <h3 style="font-size:1.4rem; color:var(--heading-color); margin-bottom:10px;">CarePlus 24/7 Online Pharmacy</h3>
          <p style="margin-bottom:15px; color:var(--text-color);">Order prescription medicines, surgical items, and wellness products with doorstep delivery within 60 minutes.</p>
          <p style="font-weight:600; color:var(--primary);">Pharmacy Hotline: +91 98765 43210 (Ext 3)</p>
        `);
      } else if (action === 'records') {
        showModal(`
          <div style="color:var(--primary); font-size:3rem; margin-bottom:15px;"><i class="fa-solid fa-file-medical"></i></div>
          <h3 style="font-size:1.4rem; color:var(--heading-color); margin-bottom:10px;">Electronic Health Records</h3>
          <p style="margin-bottom:15px; color:var(--text-color);">CarePlus maintains 100% digital, HIPAA-compliant patient medical history accessible through your registered mobile OTP.</p>
        `);
      } else if (action === 'insurance') {
        showModal(`
          <div style="color:var(--primary); font-size:3rem; margin-bottom:15px;"><i class="fa-solid fa-shield-halved"></i></div>
          <h3 style="font-size:1.4rem; color:var(--heading-color); margin-bottom:10px;">Cashless Health Insurance Desk</h3>
          <p style="margin-bottom:15px; color:var(--text-color);">We partner with over 45+ premier insurance companies and TPAs including Star Health, HDFC ERGO, ICICI Lombard, Max Bupa, and government schemes.</p>
          <p style="font-weight:600; color:var(--primary);">TPA Helpdesk: Ground Floor, Counter 6</p>
        `);
      }
    });
  });

  // ==========================================================================
  // 10. FLOATING CHATBOT WIDGET
  // ==========================================================================
  const floatingBotBtn = document.getElementById('floatingBotBtn');
  const chatbotBox = document.getElementById('chatbotBox');
  const closeChatBtn = document.getElementById('closeChatBtn');
  const chatSendBtn = document.getElementById('chatSendBtn');
  const chatInput = document.getElementById('chatInput');
  const chatMessages = document.getElementById('chatMessages');

  if (floatingBotBtn && chatbotBox) {
    floatingBotBtn.addEventListener('click', () => {
      chatbotBox.classList.toggle('active');
    });

    if (closeChatBtn) {
      closeChatBtn.addEventListener('click', () => {
        chatbotBox.classList.remove('active');
      });
    }

    const appendMessage = (text, sender) => {
      const bubble = document.createElement('div');
      bubble.className = `chat-bubble ${sender}`;
      bubble.textContent = text;
      chatMessages.appendChild(bubble);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const sendChatMessage = async (msgText) => {
      const text = msgText || (chatInput ? chatInput.value.trim() : '');
      if (!text) return;

      appendMessage(text, 'user');
      if (chatInput) chatInput.value = '';

      try {
        const res = await fetch('/api/chatbot', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        appendMessage(data.reply || 'Thank you for reaching out to CarePlus Hospital.', 'bot');
      } catch (e) {
        appendMessage('Thank you. Please call our 24x7 desk at +91 9876543210 for immediate support.', 'bot');
      }
    };

    if (chatSendBtn) {
      chatSendBtn.addEventListener('click', () => sendChatMessage());
    }

    if (chatInput) {
      chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
      });
    }

    // Chat quick tags
    document.querySelectorAll('.chat-tag').forEach(tag => {
      tag.addEventListener('click', () => {
        sendChatMessage(tag.getAttribute('data-msg'));
      });
    });
  }

  // ==========================================================================
  // 11. GALLERY LIGHTBOX MODAL
  // ==========================================================================
  document.querySelectorAll('.gallery-item').forEach(item => {
    item.addEventListener('click', () => {
      const img = item.querySelector('img');
      const title = item.querySelector('h4') ? item.querySelector('h4').textContent : 'CarePlus Hospital Facility';
      if (img) {
        showModal(`
          <h3 style="font-size:1.3rem; color:var(--heading-color); margin-bottom:15px;">${title}</h3>
          <div style="border-radius:16px; overflow:hidden; max-height:450px; margin-bottom:15px;">
            <img src="${img.src}" alt="${title}" style="width:100%; height:auto; object-fit:cover;">
          </div>
          <p style="font-size:0.9rem; color:var(--text-color);">Modern, sterilized infrastructure meeting global healthcare and NABH standards.</p>
        `);
      }
    });
  });

  // ==========================================================================
  // 12. BACK TO TOP BUTTON
  // ==========================================================================
  const backToTopBtn = document.getElementById('backToTopBtn');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 350) {
      if (backToTopBtn) backToTopBtn.classList.add('active');
    } else {
      if (backToTopBtn) backToTopBtn.classList.remove('active');
    }
  });

  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ==========================================================================
  // 13. GLOBAL MODAL HELPER
  // ==========================================================================
  const modalOverlay = document.getElementById('globalModal');
  const modalBody = document.getElementById('modalBody');
  const modalCloseBtn = document.getElementById('modalCloseBtn');

  window.showModal = (htmlContent) => {
    if (modalBody && modalOverlay) {
      modalBody.innerHTML = htmlContent;
      modalOverlay.classList.add('active');
    }
  };

  if (modalCloseBtn && modalOverlay) {
    modalCloseBtn.addEventListener('click', () => {
      modalOverlay.classList.remove('active');
    });

    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) {
        modalOverlay.classList.remove('active');
      }
    });
  }

});
