/**
 * Nhealth - Healthcare at Home
 * Main Frontend Interactions & API Handlers
 */

document.addEventListener('DOMContentLoaded', () => {
    initIntroVideo();
    initNavbarScroll();
    initStatsCounter();
    initMobileNav();
    initSearch();
    initMapInteractions();
    initDateInput();
});

/* ==========================================================================
   1. NAVBAR SCROLL EFFECT & SMOOTH SCROLLING
   ========================================================================== */
function initNavbarScroll() {
    const header = document.getElementById('mainHeader');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 30) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

/* Set default date for booking picker */
function initDateInput() {
    const dateInput = document.getElementById('bookDate');
    if (dateInput) {
        const today = new Date();
        today.setDate(today.getDate() + 1); // default tomorrow
        dateInput.value = today.toISOString().split('T')[0];
        dateInput.min = new Date().toISOString().split('T')[0];
    }
}


/* ==========================================================================
   2. MOBILE NAVIGATION DRAWER
   ========================================================================== */
function initMobileNav() {
    const mobileToggle = document.getElementById('mobileMenuToggle');
    const mobileDrawer = document.getElementById('mobileDrawer');
    const mobileBackdrop = document.getElementById('mobileBackdrop');
    const closeDrawerBtn = document.getElementById('closeDrawerBtn');

    if (mobileToggle && mobileDrawer && mobileBackdrop) {
        mobileToggle.addEventListener('click', () => {
            mobileDrawer.classList.add('active');
            mobileBackdrop.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

        const closeNav = () => {
            mobileDrawer.classList.remove('active');
            mobileBackdrop.classList.remove('active');
            document.body.style.overflow = '';
        };

        if (closeDrawerBtn) closeDrawerBtn.addEventListener('click', closeNav);
        mobileBackdrop.addEventListener('click', closeNav);
    }
}

function openMobileDrawer() {
    const mobileDrawer = document.getElementById('mobileDrawer');
    const mobileBackdrop = document.getElementById('mobileBackdrop');
    if (mobileDrawer) mobileDrawer.classList.add('active');
    if (mobileBackdrop) mobileBackdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeMobileDrawer() {
    const mobileDrawer = document.getElementById('mobileDrawer');
    const mobileBackdrop = document.getElementById('mobileBackdrop');
    if (mobileDrawer) mobileDrawer.classList.remove('active');
    if (mobileBackdrop) mobileBackdrop.classList.remove('active');
    document.body.style.overflow = '';
}

function toggleMobileSubmenu(e) {
    e.preventDefault();
    const submenu = document.getElementById('mobileSubmenu');
    if (submenu) {
        submenu.classList.toggle('open');
    }
}


/* ==========================================================================
   3. ANDHRA PRADESH MAP INTERACTIVITY & TOOLTIP
   ========================================================================== */
function initMapInteractions() {
    const apShape = document.getElementById('andhraPradeshShape');
    const apTooltip = document.getElementById('apTooltip');

    if (apShape && apTooltip) {
        apShape.addEventListener('mouseenter', () => {
            apTooltip.classList.add('show');
        });

        apShape.addEventListener('mouseleave', () => {
            setTimeout(() => {
                if (!apTooltip.matches(':hover')) {
                    apTooltip.classList.remove('show');
                }
            }, 300);
        });

        apTooltip.addEventListener('mouseleave', () => {
            apTooltip.classList.remove('show');
        });
    }
}

function highlightAP() {
    const apTooltip = document.getElementById('apTooltip');
    if (apTooltip) {
        apTooltip.classList.toggle('show');
    }
    showToast("📍 Nhealth operates across 15+ major cities in Andhra Pradesh!", "info");
}


/* ==========================================================================
   4. STATS COUNTER ANIMATION
   ========================================================================== */
function initStatsCounter() {
    const animateCount = (el, target, suffix = "+") => {
        let count = 0;
        const speed = Math.max(1, target / 60); // 60 steps

        const update = () => {
            count += speed;
            if (count < target) {
                el.innerText = Math.ceil(count).toLocaleString() + suffix;
                requestAnimationFrame(update);
            } else {
                el.innerText = target.toLocaleString() + suffix;
            }
        };
        update();
    };

    const sections = document.querySelectorAll('.trust-stats-section, .m-trust-stats-section');
    sections.forEach(section => {
        let sectionAnimated = false;
        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !sectionAnimated) {
                    sectionAnimated = true;
                    const statNumbers = section.querySelectorAll('.stat-number');
                    statNumbers.forEach(stat => {
                        const target = parseInt(stat.getAttribute('data-target'), 10);
                        if (!isNaN(target)) {
                            animateCount(stat, target);
                        }
                    });
                    obs.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        observer.observe(section);
    });
}


/* ==========================================================================
   5. BOOKING MODAL & AJAX FORM
   ========================================================================== */
function openBookingModal(preselectedService = null) {
    const modal = document.getElementById('bookingModalBackdrop');
    const form = document.getElementById('bookingForm');
    const successView = document.getElementById('bookingSuccessView');
    const serviceSelect = document.getElementById('bookService');

    if (modal) {
        if (form) form.style.display = 'block';
        if (successView) successView.style.display = 'none';

        if (preselectedService && serviceSelect) {
            // Find option matching title
            for (let i = 0; i < serviceSelect.options.length; i++) {
                if (serviceSelect.options[i].value.toLowerCase().includes(preselectedService.toLowerCase()) || 
                    preselectedService.toLowerCase().includes(serviceSelect.options[i].value.toLowerCase())) {
                    serviceSelect.selectedIndex = i;
                    break;
                }
            }
        }

        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeBookingModal() {
    const modal = document.getElementById('bookingModalBackdrop');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

async function handleBookingSubmit(e) {
    e.preventDefault();
    const submitBtn = document.getElementById('submitBookingBtn');
    const btnText = document.getElementById('btnText');
    const btnIcon = document.getElementById('btnIcon');

    // UI Loading state
    if (submitBtn) submitBtn.disabled = true;
    if (btnText) btnText.innerText = "Confirming...";
    if (btnIcon) btnIcon.className = "fa-solid fa-spinner fa-spin";

    const formData = {
        name: document.getElementById('bookName').value,
        phone: document.getElementById('bookPhone').value,
        service: document.getElementById('bookService').value,
        city: document.getElementById('bookCity').value,
        date: document.getElementById('bookDate').value,
        time_slot: document.getElementById('bookTime').value,
        address: document.getElementById('bookAddress').value
    };

    try {
        const response = await fetch('/api/book', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (response.ok && result.status === 'success') {
            // Show Success Ticket Screen
            document.getElementById('bookingForm').style.display = 'none';
            const successView = document.getElementById('bookingSuccessView');
            successView.style.display = 'block';

            document.getElementById('ticketId').innerText = result.booking_id;
            document.getElementById('ticketService').innerText = result.details.service;
            document.getElementById('ticketCity').innerText = result.details.city;
            document.getElementById('ticketSlot').innerText = `${result.details.date} (${result.details.slot})`;

            showToast("✅ Appointment request booked successfully!", "success");
        } else {
            showToast("❌ " + (result.message || "Failed to book appointment."), "error");
        }
    } catch (err) {
        console.error("Booking error:", err);
        showToast("❌ Network error. Please try again.", "error");
    } finally {
        if (submitBtn) submitBtn.disabled = false;
        if (btnText) btnText.innerText = "Confirm Appointment";
        if (btnIcon) btnIcon.className = "fa-solid fa-arrow-right";
    }
}


/* ==========================================================================
   6. FIRST-TIME INTRO VIDEO & VIDEO MODAL PLAYBACK
   ========================================================================== */
function initIntroVideo() {
    const introOverlay = document.getElementById('introVideoOverlay');
    const introVideo = document.getElementById('introVideoPlayer');

    // Allow ?intro=1 or ?play_intro=1 to test intro video anytime, or ?no_intro=1 to skip
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('intro') || urlParams.has('play_intro')) {
        sessionStorage.removeItem('nhealth_intro_viewed');
    } else if (urlParams.has('no_intro') || urlParams.has('skip_intro')) {
        sessionStorage.setItem('nhealth_intro_viewed', 'true');
    }

    // Detect mobile screen (width <= 991px or mobile user agent)
    const isMobile = window.innerWidth <= 991 || /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

    if (introVideo) {
        const targetSrc = isMobile ? introVideo.dataset.mobileSrc : introVideo.dataset.desktopSrc;
        if (targetSrc) {
            const currentSrc = introVideo.currentSrc || introVideo.src || '';
            if (!currentSrc.includes(targetSrc)) {
                introVideo.src = targetSrc;
                introVideo.load();
            }
        }
    }

    // Check if user has already visited in this session
    const hasSeenIntro = sessionStorage.getItem('nhealth_intro_viewed');

    if (!hasSeenIntro && introOverlay && introVideo) {
        // Show intro overlay for first-time entrance
        introOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';

        // Play video (muted ensures browser autoplay compliance)
        introVideo.play().catch(err => {
            console.log("Autoplay waiting for user interaction:", err);
        });

        // When video ends, automatically enter the website smoothly
        introVideo.addEventListener('ended', () => {
            setTimeout(closeIntroVideo, 800);
        });
    }
}

function closeIntroVideo() {
    const introOverlay = document.getElementById('introVideoOverlay');
    const introVideo = document.getElementById('introVideoPlayer');

    if (introOverlay) {
        introOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (introVideo) {
        introVideo.pause();
    }

    // Save flag so it only pops up on first entrance
    sessionStorage.setItem('nhealth_intro_viewed', 'true');
}

function toggleIntroAudio() {
    const video = document.getElementById('introVideoPlayer');
    const icon = document.getElementById('introAudioIcon');
    if (!video || !icon) return;

    if (video.muted) {
        video.muted = false;
        icon.className = "fa-solid fa-volume-high";
        showToast("🔊 Audio Unmuted", "info");
    } else {
        video.muted = true;
        icon.className = "fa-solid fa-volume-xmark";
        showToast("🔇 Audio Muted", "info");
    }
}

function toggleIntroPlay() {
    const video = document.getElementById('introVideoPlayer');
    const icon = document.getElementById('introPlayIcon');
    if (!video || !icon) return;

    if (video.paused) {
        video.play();
        icon.className = "fa-solid fa-pause";
    } else {
        video.pause();
        icon.className = "fa-solid fa-play";
    }
}

function openVideoModal() {
    const modal = document.getElementById('videoModalBackdrop');
    const video = document.getElementById('modalVideoPlayer');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        if (video) {
            const isMobile = window.innerWidth <= 991 || /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
            const targetSrc = isMobile ? video.dataset.mobileSrc : video.dataset.desktopSrc;
            if (targetSrc && (!video.src || !video.src.includes(targetSrc))) {
                video.src = targetSrc;
                video.load();
            }
            video.currentTime = 0;
            video.play().catch(e => console.log(e));
        }
    }
}

function closeVideoModal() {
    const modal = document.getElementById('videoModalBackdrop');
    const video = document.getElementById('modalVideoPlayer');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        if (video) {
            video.pause();
        }
    }
}


/* ==========================================================================
   7. LOGIN & AUTH MODAL
   ========================================================================== */
function openLoginModal() {
    const modal = document.getElementById('loginModalBackdrop');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeLoginModal() {
    const modal = document.getElementById('loginModalBackdrop');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function switchLoginTab(tab, tabBtn) {
    document.querySelectorAll('.l-tab').forEach(b => b.classList.remove('active'));
    tabBtn.classList.add('active');

    const otpForm = document.getElementById('otpLoginForm');
    const emailForm = document.getElementById('emailLoginForm');

    if (tab === 'otp') {
        otpForm.style.display = 'block';
        emailForm.style.display = 'none';
    } else {
        otpForm.style.display = 'none';
        emailForm.style.display = 'block';
    }
}

function sendMockOtp() {
    const phoneInput = document.getElementById('loginPhoneInput');
    if (!phoneInput.value || phoneInput.value.length < 10) {
        showToast("⚠️ Please enter a valid 10-digit mobile number", "error");
        return;
    }
    showToast(`📲 6-digit OTP sent to +91 ${phoneInput.value}`, "success");
    setTimeout(() => {
        closeLoginModal();
        showToast("🎉 Welcome to Nhealth Healthcare Portal!", "success");
    }, 1500);
}

function handlePartnerLogin() {
    showToast("🔐 Authenticating doctor / partner credentials...", "info");
    setTimeout(() => {
        closeLoginModal();
        showToast("👨‍⚕️ Welcome Doctor! Provider dashboard access granted.", "success");
    }, 1200);
}


/* ==========================================================================
   8. ALL SERVICES MODAL
   ========================================================================== */
function openAllServicesModal() {
    const modal = document.getElementById('allServicesModalBackdrop');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeAllServicesModal() {
    const modal = document.getElementById('allServicesModalBackdrop');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}


/* ==========================================================================
   9. SEARCH OVERLAY
   ========================================================================== */
let allServicesData = [];

function initSearch() {
    const searchBtn = document.getElementById('searchTriggerBtn');
    const searchOverlay = document.getElementById('searchOverlay');
    const searchInput = document.getElementById('liveSearchInput');

    if (searchBtn && searchOverlay) {
        searchBtn.addEventListener('click', () => {
            searchOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
            if (searchInput) {
                searchInput.focus();
                handleSearchQuery('');
            }
        });
    }

    // Fetch dynamic services catalog
    fetch('/api/services')
        .then(res => res.json())
        .then(json => {
            if (json.data) {
                allServicesData = json.data;
            }
        })
        .catch(err => console.error("Could not preload services:", err));
}

function closeSearchOverlay() {
    const searchOverlay = document.getElementById('searchOverlay');
    if (searchOverlay) {
        searchOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function handleSearchQuery(query) {
    const resultsContainer = document.getElementById('searchResultsList');
    if (!resultsContainer) return;

    const q = query.trim().toLowerCase();
    const filtered = allServicesData.filter(s => 
        s.title.toLowerCase().includes(q) || 
        s.category.toLowerCase().includes(q) ||
        s.description.toLowerCase().includes(q)
    );

    if (filtered.length === 0) {
        resultsContainer.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: #64748b;">
                <i class="fa-solid fa-magnifying-glass" style="font-size: 2rem; margin-bottom: 0.5rem; opacity: 0.5;"></i>
                <p>No services matched "${query}". Try searching "Doctor", "Blood Test", "X-Ray", or "Eldercare".</p>
            </div>
        `;
        return;
    }

    resultsContainer.innerHTML = filtered.map(item => `
        <div class="search-result-item" onclick="openBookingModal('${item.title}'); closeSearchOverlay();">
            <div class="dropdown-icon" style="background: ${item.bg_tint}; color: ${item.color};">
                <i class="fa-solid fa-${item.icon}"></i>
            </div>
            <div class="dropdown-info" style="flex: 1;">
                <span class="d-title">${item.title}</span>
                <span class="d-desc">${item.category} &bull; ${item.badge}</span>
            </div>
            <button class="btn-outline-pill" style="padding: 0.3rem 0.9rem; font-size: 0.78rem;">Book</button>
        </div>
    `).join('');
}


/* ==========================================================================
   10. TOAST NOTIFICATIONS & GLOBAL MODAL ESCAPE
   ========================================================================== */
function showToast(message, type = "success") {
    const toast = document.getElementById('toastNotification');
    const msgEl = document.getElementById('toastMsg');
    const iconEl = document.getElementById('toastIcon');

    if (!toast || !msgEl) return;

    msgEl.innerText = message;
    
    if (type === "success") {
        iconEl.className = "fa-solid fa-circle-check toast-icon";
        iconEl.style.color = "#10b981";
    } else if (type === "error") {
        iconEl.className = "fa-solid fa-circle-exclamation toast-icon";
        iconEl.style.color = "#ef4444";
    } else {
        iconEl.className = "fa-solid fa-circle-info toast-icon";
        iconEl.style.color = "#0ea5e9";
    }

    toast.classList.add('active');

    setTimeout(() => {
        toast.classList.remove('active');
    }, 3800);
}

/* ==========================================================================
   11. TELEMEDICINE VIRTUAL CLINIC & LIVE CHAT / RX
   ========================================================================== */
function switchTelemedTab(tab, tabBtn) {
    document.querySelectorAll('.t-tab-btn').forEach(b => b.classList.remove('active'));
    tabBtn.classList.add('active');

    const chatPane = document.getElementById('telemedChatPane');
    const rxPane = document.getElementById('telemedRxPane');

    if (tab === 'chat') {
        if (chatPane) chatPane.style.display = 'flex';
        if (rxPane) rxPane.style.display = 'none';
    } else {
        if (chatPane) chatPane.style.display = 'none';
        if (rxPane) rxPane.style.display = 'flex';
    }
}

function sendTelemedChatMessage(e) {
    e.preventDefault();
    const input = document.getElementById('telemedChatInput');
    const scrollContainer = document.getElementById('chatMessagesScroll');

    if (!input || !input.value.trim() || !scrollContainer) return;

    const userText = input.value.trim();
    input.value = '';

    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Append patient message
    const patientMsg = document.createElement('div');
    patientMsg.className = 'chat-bubble patient-msg';
    patientMsg.innerHTML = `
        <div class="chat-sender">You</div>
        <div class="chat-text">${userText}</div>
        <div class="chat-time">${timeStr}</div>
    `;
    scrollContainer.appendChild(patientMsg);
    scrollContainer.scrollTop = scrollContainer.scrollHeight;

    // Doctor response simulation
    setTimeout(() => {
        const docMsg = document.createElement('div');
        docMsg.className = 'chat-bubble doc-msg';
        docMsg.innerHTML = `
            <div class="chat-sender">Dr. Priya Sharma</div>
            <div class="chat-text">Noted Rahul. Telemetry readings reflect stable cardiac rhythm. I've updated your digital chart accordingly.</div>
            <div class="chat-time">${timeStr}</div>
        `;
        scrollContainer.appendChild(docMsg);
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
        showToast("💬 Dr. Priya Sharma responded to your message", "info");
    }, 1100);
}

function triggerEmergencySOS() {
    showToast("🚨 EMERGENCY SOS ACTIVE: Dispatched nearest ALS Ambulance (ETA 6 Mins). Hospital ER pre-synced!", "error");
}

function openSearchOverlay() {
    const searchOverlay = document.getElementById('searchOverlay');
    const searchInput = document.getElementById('liveSearchInput');
    if (searchOverlay) {
        searchOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        if (searchInput) {
            searchInput.focus();
            handleSearchQuery('');
        }
    }
}

/* ==========================================================================
   12. FLOATING WHATSAPP BUTTON & CHAT WIDGET
   ========================================================================== */
function toggleWhatsAppWidget() {
    const widget = document.getElementById('whatsappChatWidget');
    if (widget) {
        widget.classList.toggle('active');
    }
}

function selectWhatsAppQuickTopic(topic) {
    toggleWhatsAppWidget();
    openBookingModal(topic);
    showToast(`📲 Selected "${topic}" — Continue booking below`, "info");
}

// Close modals with Escape key or clicking outer backdrop
window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeBookingModal();
        closeVideoModal();
        closeLoginModal();
        closeAllServicesModal();
        closeSearchOverlay();
        closeMobileDrawer();
        const waWidget = document.getElementById('whatsappChatWidget');
        if (waWidget) waWidget.classList.remove('active');
    }
});

document.querySelectorAll('.custom-modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', (e) => {
        if (e.target === backdrop) {
            backdrop.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
});
