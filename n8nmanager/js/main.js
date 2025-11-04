// n8nManager Landing Page - Main JavaScript
// 所有交互功能的原生 JavaScript 實現

document.addEventListener('DOMContentLoaded', function() {

  // ==================== 行動版選單 ====================
  const mobileMenuButton = document.getElementById('mobile-menu-button');
  const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
  const mobileMenuPanel = document.getElementById('mobile-menu-panel');
  let isMobileMenuOpen = false;

  function toggleMobileMenu() {
    isMobileMenuOpen = !isMobileMenuOpen;

    if (isMobileMenuOpen) {
      // 開啟選單
      mobileMenuOverlay.classList.remove('hidden');
      mobileMenuPanel.classList.remove('translate-x-full');
      mobileMenuButton.setAttribute('aria-expanded', 'true');
      mobileMenuButton.setAttribute('aria-label', '關閉選單');

      // 更換圖標為 X
      mobileMenuButton.innerHTML = `
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      `;

      // 鎖定背景滾動
      document.body.style.overflow = 'hidden';
    } else {
      // 關閉選單
      mobileMenuOverlay.classList.add('hidden');
      mobileMenuPanel.classList.add('translate-x-full');
      mobileMenuButton.setAttribute('aria-expanded', 'false');
      mobileMenuButton.setAttribute('aria-label', '開啟選單');

      // 更換圖標為 hamburger
      mobileMenuButton.innerHTML = `
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      `;

      // 解鎖背景滾動
      document.body.style.overflow = 'unset';
    }
  }

  // 選單按鈕點擊事件
  if (mobileMenuButton) {
    mobileMenuButton.addEventListener('click', toggleMobileMenu);
  }

  // 遮罩層點擊事件（關閉選單）
  if (mobileMenuOverlay) {
    mobileMenuOverlay.addEventListener('click', function() {
      if (isMobileMenuOpen) {
        toggleMobileMenu();
      }
    });
  }

  // 選單內連結點擊後關閉選單
  if (mobileMenuPanel) {
    const mobileMenuLinks = mobileMenuPanel.querySelectorAll('a');
    mobileMenuLinks.forEach(link => {
      link.addEventListener('click', function() {
        if (isMobileMenuOpen) {
          toggleMobileMenu();
        }
      });
    });
  }

  // ==================== FAQ 展開/收合 ====================
  const faqButtons = document.querySelectorAll('.faq-button');

  faqButtons.forEach((button, index) => {
    button.addEventListener('click', function() {
      const answer = this.nextElementSibling;
      const icon = this.querySelector('.faq-icon');
      const isExpanded = this.getAttribute('aria-expanded') === 'true';

      // 關閉所有其他 FAQ
      faqButtons.forEach((otherButton, otherIndex) => {
        if (otherIndex !== index) {
          const otherAnswer = otherButton.nextElementSibling;
          const otherIcon = otherButton.querySelector('.faq-icon');
          otherAnswer.style.maxHeight = '0';
          otherIcon.style.transform = 'rotate(0deg)';
          otherButton.setAttribute('aria-expanded', 'false');
        }
      });

      // 切換當前 FAQ
      if (isExpanded) {
        // 關閉
        answer.style.maxHeight = '0';
        icon.style.transform = 'rotate(0deg)';
        this.setAttribute('aria-expanded', 'false');
      } else {
        // 開啟
        answer.style.maxHeight = answer.scrollHeight + 'px';
        icon.style.transform = 'rotate(180deg)';
        this.setAttribute('aria-expanded', 'true');
      }
    });
  });

  // ==================== Smooth Scroll 平滑滾動 ====================
  const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');

  smoothScrollLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      const href = this.getAttribute('href');

      // 確保是內部錨點
      if (href === '#' || !href.startsWith('#')) {
        return;
      }

      e.preventDefault();

      const targetId = href.substring(1);
      const targetElement = document.getElementById(targetId);

      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // ==================== Intersection Observer 滾動淡入動畫 ====================
  const fadeInElements = document.querySelectorAll('.fade-in-section');

  const fadeInObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        // 可選：觀察一次後就停止觀察
        // observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1, // 當 10% 的元素可見時觸發
    rootMargin: '0px 0px -50px 0px' // 提前觸發動畫
  });

  fadeInElements.forEach(element => {
    fadeInObserver.observe(element);
  });

  // ==================== 頁面載入動畫 ====================
  // 為 Hero Section 和 Navigation 添加淡入動畫
  window.addEventListener('load', function() {
    const header = document.querySelector('header');
    const heroSection = document.querySelector('section');

    if (header) {
      header.style.animation = 'fadeInUp 0.8s ease-out forwards';
    }

    if (heroSection) {
      heroSection.style.animation = 'fadeIn 1s ease-out 0.2s forwards';
    }
  });

  // ==================== 視窗大小改變時處理 ====================
  window.addEventListener('resize', function() {
    // 如果視窗變大（超過 md breakpoint），關閉行動版選單
    if (window.innerWidth >= 768 && isMobileMenuOpen) {
      toggleMobileMenu();
    }

    // 調整已展開的 FAQ 答案高度
    faqButtons.forEach(button => {
      const isExpanded = button.getAttribute('aria-expanded') === 'true';
      if (isExpanded) {
        const answer = button.nextElementSibling;
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });

  // ==================== 防止背景滾動洩漏 ====================
  // 確保頁面卸載時解鎖滾動
  window.addEventListener('beforeunload', function() {
    document.body.style.overflow = 'unset';
  });

  // ==================== 主題切換功能 ====================
  const html = document.documentElement;
  const themeToggle = document.getElementById('theme-toggle');
  const sunIcon = document.getElementById('sun-icon');
  const moonIcon = document.getElementById('moon-icon');

  // 從 localStorage 讀取已儲存的主題，預設為 dark
  const savedTheme = localStorage.getItem('theme') || 'dark';

  // 套用儲存的主題
  html.setAttribute('data-theme', savedTheme);
  updateThemeIcons(savedTheme);

  // 主題切換按鈕事件
  if (themeToggle) {
    themeToggle.addEventListener('click', function() {
      const currentTheme = html.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

      // 更新 HTML 屬性
      html.setAttribute('data-theme', newTheme);

      // 儲存到 localStorage
      localStorage.setItem('theme', newTheme);

      // 更新圖示
      updateThemeIcons(newTheme);
    });
  }

  // 更新主題圖示顯示
  function updateThemeIcons(theme) {
    if (!sunIcon || !moonIcon) return;

    if (theme === 'dark') {
      // 深色模式顯示太陽圖示（點擊後切換到淺色）
      sunIcon.classList.remove('hidden');
      moonIcon.classList.add('hidden');
    } else {
      // 淺色模式顯示月亮圖示（點擊後切換到深色）
      sunIcon.classList.add('hidden');
      moonIcon.classList.remove('hidden');
    }
  }
});
