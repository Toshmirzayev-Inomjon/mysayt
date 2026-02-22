(function () {
    var root = document.documentElement;
    var body = document.body;
    body.classList.add('js-enabled');

    var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function initTheme() {
        var toggle = document.getElementById('themeToggle');
        if (!toggle) return;

        var saved = localStorage.getItem('theme');
        if (saved === 'light' || saved === 'dark') {
            root.setAttribute('data-theme', saved);
        }

        toggle.addEventListener('click', function () {
            var current = root.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
            var next = current === 'dark' ? 'light' : 'dark';
            root.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
        });
    }

    function initMobileNav() {
        var toggle = document.getElementById('navToggle');
        var nav = document.getElementById('mainNav');
        var backdrop = document.getElementById('navBackdrop');
        if (!toggle || !nav) return;

        function closeNav() {
            body.classList.remove('nav-open');
            toggle.setAttribute('aria-expanded', 'false');
        }

        function openNav() {
            body.classList.add('nav-open');
            toggle.setAttribute('aria-expanded', 'true');
        }

        toggle.addEventListener('click', function () {
            if (body.classList.contains('nav-open')) {
                closeNav();
            } else {
                openNav();
            }
        });

        if (backdrop) {
            backdrop.addEventListener('click', closeNav);
        }

        nav.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', closeNav);
        });

        window.addEventListener('resize', function () {
            if (window.innerWidth > 920) {
                closeNav();
            }
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                closeNav();
            }
        });
    }

    function hideLoader() {
        var loader = document.getElementById('pageLoader');
        if (!loader) return;
        window.addEventListener('load', function () {
            loader.classList.add('is-hidden');
        });
    }

    function initVideoExperience() {
        var videos = document.querySelectorAll('video[data-video-fallback="1"]');
        if (!videos.length) return;

        var connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        var saveData = connection && connection.saveData;
        if (saveData) {
            body.classList.add('video-fallback');
            videos.forEach(function (video) {
                try {
                    video.pause();
                } catch (e) {}
            });
            return;
        }

        videos.forEach(function (video) {
            var wrap = video.closest('.hero-reel-wrap');

            function markReady() {
                video.classList.add('is-ready');
                if (wrap) {
                    wrap.classList.add('is-ready');
                }
            }

            function markFailed() {
                video.classList.add('is-failed');
                if (video.classList.contains('bg-video')) {
                    body.classList.add('video-fallback');
                }
            }

            if (video.readyState >= 2) {
                markReady();
            }

            video.addEventListener('loadeddata', markReady, { once: true });
            video.addEventListener('canplay', markReady, { once: true });
            video.addEventListener('error', markFailed);
            video.addEventListener('stalled', markFailed);
        });
    }

    function initReveal() {
        var items = document.querySelectorAll('.reveal');
        if (!items.length) return;

        if (prefersReducedMotion) {
            items.forEach(function (el) {
                el.classList.add('is-visible');
            });
            return;
        }

        var observer = new IntersectionObserver(
            function (entries, obs) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        obs.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.14, rootMargin: '0px 0px -40px 0px' }
        );

        items.forEach(function (item) {
            observer.observe(item);
        });
    }

    function initCursor() {
        if ('ontouchstart' in window) return;

        var dot = document.getElementById('cursorDot');
        var glow = document.getElementById('cursorGlow');
        if (!dot || !glow) return;

        var x = window.innerWidth / 2;
        var y = window.innerHeight / 2;
        var gx = x;
        var gy = y;

        document.addEventListener('mousemove', function (e) {
            x = e.clientX;
            y = e.clientY;
            dot.style.left = x + 'px';
            dot.style.top = y + 'px';
        });

        function animateGlow() {
            gx += (x - gx) * 0.18;
            gy += (y - gy) * 0.18;
            glow.style.left = gx + 'px';
            glow.style.top = gy + 'px';
            window.requestAnimationFrame(animateGlow);
        }
        animateGlow();

        var hoverables = document.querySelectorAll('a, button, input, textarea');
        hoverables.forEach(function (el) {
            el.addEventListener('mouseenter', function () {
                glow.classList.add('is-hover');
            });
            el.addEventListener('mouseleave', function () {
                glow.classList.remove('is-hover');
            });
        });
    }

    function initParallax() {
        if (prefersReducedMotion) return;

        var els = document.querySelectorAll('[data-parallax]');
        if (!els.length) return;

        document.addEventListener('mousemove', function (e) {
            var rx = (e.clientX / window.innerWidth - 0.5) * 2;
            var ry = (e.clientY / window.innerHeight - 0.5) * 2;
            els.forEach(function (el) {
                var depth = Number(el.getAttribute('data-parallax')) || 10;
                var tx = rx * depth * 0.6;
                var ty = ry * depth * 0.35;
                el.style.transform = 'translate3d(' + tx.toFixed(2) + 'px,' + ty.toFixed(2) + 'px,0)';
            });
        });
    }

    function initModal() {
        var modal = document.getElementById('projectModal');
        if (!modal) return;

        var title = document.getElementById('modalTitle');
        var description = document.getElementById('modalDescription');
        var tech = document.getElementById('modalTech');
        var image = document.getElementById('modalImage');
        var link = document.getElementById('modalLink');
        var close = document.getElementById('modalClose');
        var defaultTitle = modal.dataset.defaultTitle || 'Project';
        var techLabel = (modal.dataset.techLabel || 'Technologies:').trim();

        function closeModal() {
            modal.classList.remove('is-open');
            modal.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        }

        function openModal(btn) {
            title.textContent = btn.dataset.title || defaultTitle;
            description.textContent = btn.dataset.description || '';
            tech.textContent = btn.dataset.tech ? (techLabel + ' ' + btn.dataset.tech).trim() : '';
            link.setAttribute('href', btn.dataset.link || '#');

            if (btn.dataset.image) {
                image.src = btn.dataset.image;
                image.classList.add('has-image');
            } else {
                image.removeAttribute('src');
                image.classList.remove('has-image');
            }

            modal.classList.add('is-open');
            modal.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden';
        }

        document.querySelectorAll('.preview-btn').forEach(function (btn) {
            btn.addEventListener('click', function () {
                openModal(btn);
            });
        });

        modal.addEventListener('click', function (e) {
            if (e.target.dataset.closeModal === '1') {
                closeModal();
            }
        });

        if (close) {
            close.addEventListener('click', closeModal);
        }

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && modal.classList.contains('is-open')) {
                closeModal();
            }
        });
    }

    function initCounters() {
        var counters = document.querySelectorAll('[data-counter]');
        if (!counters.length) return;

        function runCounter(el) {
            var target = Number(el.getAttribute('data-counter')) || 0;
            var duration = 1000;
            var start = performance.now();

            function tick(now) {
                var progress = Math.min((now - start) / duration, 1);
                var value = Math.round(progress * target);
                el.textContent = value;
                if (progress < 1) {
                    requestAnimationFrame(tick);
                }
            }

            requestAnimationFrame(tick);
        }

        if (prefersReducedMotion) {
            counters.forEach(function (el) {
                el.textContent = el.getAttribute('data-counter');
            });
            return;
        }

        var observer = new IntersectionObserver(
            function (entries, obs) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        runCounter(entry.target);
                        obs.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.5 }
        );

        counters.forEach(function (counter) {
            observer.observe(counter);
        });
    }

    function initTiltCards() {
        if (prefersReducedMotion || 'ontouchstart' in window) return;

        var cards = document.querySelectorAll('.project-card');
        if (!cards.length) return;

        cards.forEach(function (card) {
            card.addEventListener('mousemove', function (e) {
                var rect = card.getBoundingClientRect();
                var x = (e.clientX - rect.left) / rect.width;
                var y = (e.clientY - rect.top) / rect.height;
                var ry = (x - 0.5) * 8;
                var rx = (0.5 - y) * 8;
                card.style.setProperty('--rx', rx.toFixed(2) + 'deg');
                card.style.setProperty('--ry', ry.toFixed(2) + 'deg');
            });

            card.addEventListener('mouseleave', function () {
                card.style.setProperty('--rx', '0deg');
                card.style.setProperty('--ry', '0deg');
            });
        });
    }

    function initScrollProgress() {
        var bar = document.getElementById('scrollProgressBar');
        if (!bar) return;

        function update() {
            var scrollTop = window.scrollY || document.documentElement.scrollTop;
            var docHeight = document.documentElement.scrollHeight - window.innerHeight;
            var percent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
            bar.style.width = percent.toFixed(2) + '%';
        }

        window.addEventListener('scroll', update, { passive: true });
        update();
    }

    function initTestimonialsSlider() {
        var slider = document.querySelector('[data-testimonials-slider="1"]');
        if (!slider) return;

        var wrap = slider.querySelector('.testimonials-track-wrap');
        var track = slider.querySelector('.testimonials-track');
        var prevBtn = slider.querySelector('[data-slider-dir="prev"]');
        var nextBtn = slider.querySelector('[data-slider-dir="next"]');
        if (!wrap || !track) return;

        var autoTimer = null;

        function slideDistance() {
            var first = track.querySelector('.testimonial-slide');
            if (!first) return 320;
            var gapValue = window.getComputedStyle(track).gap || window.getComputedStyle(track).columnGap || '12px';
            var gap = Number(String(gapValue).replace('px', '')) || 12;
            return first.getBoundingClientRect().width + gap;
        }

        function move(direction) {
            var amount = slideDistance() * direction;
            wrap.scrollBy({ left: amount, behavior: 'smooth' });
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', function () {
                move(-1);
            });
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', function () {
                move(1);
            });
        }

        function startAuto() {
            if (prefersReducedMotion) return;
            stopAuto();
            autoTimer = window.setInterval(function () {
                var maxScroll = wrap.scrollWidth - wrap.clientWidth;
                if (wrap.scrollLeft >= maxScroll - 5) {
                    wrap.scrollTo({ left: 0, behavior: 'smooth' });
                } else {
                    move(1);
                }
            }, 5000);
        }

        function stopAuto() {
            if (autoTimer) {
                window.clearInterval(autoTimer);
                autoTimer = null;
            }
        }

        slider.addEventListener('mouseenter', stopAuto);
        slider.addEventListener('mouseleave', startAuto);
        startAuto();
    }

    function initBookingSlots() {
        var input = document.querySelector('input[name="preferred_datetime"]');
        var picks = document.querySelectorAll('.slot-pick-btn');
        if (!input || !picks.length) return;

        picks.forEach(function (btn) {
            btn.addEventListener('click', function () {
                picks.forEach(function (b) {
                    b.classList.remove('is-selected');
                });
                btn.classList.add('is-selected');
                input.value = btn.dataset.slotValue || '';
                input.dispatchEvent(new Event('change', { bubbles: true }));
            });
        });
    }

    function initServiceWorker() {
        if (!('serviceWorker' in navigator)) return;
        window.addEventListener('load', function () {
            navigator.serviceWorker.register('/sw.js').catch(function () {});
        });
    }

    initTheme();
    initMobileNav();
    hideLoader();
    initVideoExperience();
    initReveal();
    initCursor();
    initParallax();
    initModal();
    initCounters();
    initTiltCards();
    initScrollProgress();
    initTestimonialsSlider();
    initBookingSlots();
    initServiceWorker();
})();
