/* Utrujj homepage prototype — interaction layer */
(function () {
  "use strict";

  const header = document.querySelector("[data-header]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const mobileMenu = document.querySelector("[data-mobile-menu]");
  const searchOpen = document.querySelector("[data-search-open]");
  const searchPanel = document.querySelector("[data-search-panel]");
  const searchClose = document.querySelector("[data-search-close]");
  const searchInput = document.querySelector("#site-search");
  const dropdowns = Array.from(document.querySelectorAll(".nav-item.has-sub"));

  /* Sticky header state */
  const setHeaderState = () => {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  };
  setHeaderState();
  window.addEventListener("scroll", setHeaderState, { passive: true });

  /* Dropdown menus */
  const closeDropdowns = (except) => {
    dropdowns.forEach((item) => {
      if (item === except) return;
      item.classList.remove("is-open");
      const button = item.querySelector(".nav-link");
      if (button) button.setAttribute("aria-expanded", "false");
    });
  };

  dropdowns.forEach((item) => {
    const button = item.querySelector(".nav-link");
    if (!button) return;

    button.addEventListener("click", (event) => {
      event.stopPropagation();
      const isOpen = item.classList.toggle("is-open");
      button.setAttribute("aria-expanded", String(isOpen));
      closeDropdowns(isOpen ? item : null);
    });

    item.addEventListener("mouseleave", () => {
      if (!item.classList.contains("is-open")) return;
      item.classList.remove("is-open");
      button.setAttribute("aria-expanded", "false");
    });
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".nav-item.has-sub")) closeDropdowns();
  });

  /* Mobile menu */
  const menuIcon = menuToggle ? menuToggle.querySelector("use") : null;

  const setMenu = (open) => {
    if (!menuToggle || !mobileMenu) return;
    mobileMenu.hidden = !open;
    menuToggle.setAttribute("aria-expanded", String(open));
    menuToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.body.classList.toggle("menu-open", open);
    if (menuIcon) menuIcon.setAttribute("href", open ? "#i-close" : "#i-menu");
  };

  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener("click", () => {
      setMenu(mobileMenu.hidden);
    });

    mobileMenu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => setMenu(false));
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 1020) setMenu(false);
    });
  }

  /* Search panel */
  const setSearch = (open) => {
    if (!searchPanel) return;
    searchPanel.hidden = !open;
    document.body.classList.toggle("search-open", open);
    if (open && searchInput) {
      window.setTimeout(() => searchInput.focus(), 40);
    }
  };

  if (searchOpen && searchPanel) {
    searchOpen.addEventListener("click", () => setSearch(true));
  }
  if (searchClose && searchPanel) {
    searchClose.addEventListener("click", () => setSearch(false));
  }
  if (searchPanel) {
    searchPanel.addEventListener("click", (event) => {
      if (event.target === searchPanel) setSearch(false);
    });
  }

  /* Escape closes overlays */
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    if (searchPanel && !searchPanel.hidden) setSearch(false);
    if (mobileMenu && !mobileMenu.hidden) setMenu(false);
    closeDropdowns();
  });

  /* Reveal on scroll */
  const reveals = Array.from(document.querySelectorAll(".reveal"));
  if ("IntersectionObserver" in window && reveals.length) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
    );
    reveals.forEach((element) => observer.observe(element));
  } else {
    reveals.forEach((element) => element.classList.add("is-visible"));
  }

  /* Newsletter prototype behaviour */
  const newsletter = document.querySelector("[data-newsletter]");
  if (newsletter) {
    newsletter.addEventListener("submit", (event) => {
      event.preventDefault();
      const note = newsletter.querySelector("[data-form-note]");
      if (note) {
        note.textContent = "JazakAllah khair — you're on the list. Look out for our next email.";
        note.classList.add("is-success");
      }
      newsletter.reset();
    });
  }
})();
