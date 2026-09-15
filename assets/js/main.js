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

const setupAbstractDisclosures = () => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  document.querySelectorAll('#publications details.abstract').forEach((details) => {
    const summary = details.querySelector('summary');
    const panel = details.querySelector('.abstract-panel');

    if (!summary || !panel || typeof panel.animate !== 'function') {
      return;
    }

    let animation = null;
    let closing = false;

    summary.addEventListener('click', (event) => {
      event.preventDefault();

      const shouldOpen = closing || !details.open;
      const startHeight = details.open ? panel.getBoundingClientRect().height : 0;
      const startOpacity = details.open ? Number(getComputedStyle(panel).opacity) : 0;
      animation?.cancel();
      animation = null;

      if (reducedMotion.matches) {
        details.open = shouldOpen;
        closing = false;
        delete details.dataset.collapsing;
        panel.style.removeProperty('height');
        panel.style.removeProperty('opacity');
        return;
      }

      // Keep the content clipped before opening <details>, so its first
      // visible frame starts at zero height instead of flashing open.
      panel.style.height = `${startHeight}px`;
      panel.style.opacity = `${startOpacity}`;

      if (shouldOpen) {
        details.open = true;
        delete details.dataset.collapsing;
      } else {
        details.dataset.collapsing = '';
      }

      closing = !shouldOpen;
      const endHeight = shouldOpen ? panel.scrollHeight : 0;
      const currentAnimation = panel.animate(
        [
          { height: `${startHeight}px`, opacity: startOpacity },
          { height: `${endHeight}px`, opacity: shouldOpen ? 1 : 0 },
        ],
        {
          duration: 280,
          easing: 'cubic-bezier(0.2, 0.7, 0.2, 1)',
          fill: 'forwards',
        }
      );

      animation = currentAnimation;
      currentAnimation.onfinish = () => {
        if (animation !== currentAnimation) {
          return;
        }

        if (!shouldOpen) {
          details.open = false;
          delete details.dataset.collapsing;
        }

        panel.style.removeProperty('height');
        panel.style.removeProperty('opacity');
        currentAnimation.cancel();
        animation = null;
        closing = false;
      };
    });
  });
};

const setupPage = () => {
  setupSectionNavigation();
  setupAbstractDisclosures();
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', setupPage);
} else {
  setupPage();
}
