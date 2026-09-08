const setupSectionNavigation = () => {
  const header = document.querySelector('.site-header');
  const links = Array.from(document.querySelectorAll('.menu-container a[data-section]'));

  if (!links.length) {
    return;
  }

  const sections = links
    .map((link) => document.getElementById(link.dataset.section))
    .filter(Boolean);

  if (!sections.length) {
    return;
  }

  const setActiveSection = (sectionID) => {
    links.forEach((link) => {
      const isActive = link.dataset.section === sectionID;
      link.classList.toggle('active', isActive);

      if (isActive) {
        link.setAttribute('aria-current', 'location');
      } else {
        link.removeAttribute('aria-current');
      }
    });
  };

  const updateHeaderOffset = () => {
    if (!header) {
      return;
    }

    const offset = Math.ceil(header.getBoundingClientRect().height + 16);
    document.documentElement.style.setProperty('--sticky-header-offset', `${offset}px`);
  };

  let frameRequested = false;
  const updateActiveSection = () => {
    const threshold = (header?.getBoundingClientRect().bottom ?? 0) + 8;
    let activeSection = sections[0].id;

    sections.forEach((section) => {
      if (section.getBoundingClientRect().top <= threshold) {
        activeSection = section.id;
      }
    });

    setActiveSection(activeSection);
    frameRequested = false;
  };

  const requestSectionUpdate = () => {
    if (!frameRequested) {
      frameRequested = true;
      window.requestAnimationFrame(updateActiveSection);
    }
  };

  links.forEach((link) => {
    link.addEventListener('click', () => setActiveSection(link.dataset.section));
  });

  window.addEventListener('scroll', requestSectionUpdate, { passive: true });
  window.addEventListener('resize', () => {
    updateHeaderOffset();
    requestSectionUpdate();
  });
  window.addEventListener('hashchange', requestSectionUpdate);
  window.addEventListener('load', () => {
    updateHeaderOffset();
    requestSectionUpdate();
  });

  updateHeaderOffset();
  updateActiveSection();
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', setupSectionNavigation);
} else {
  setupSectionNavigation();
}
