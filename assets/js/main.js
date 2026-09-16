const setupSectionNavigation = () => {
  const header = document.querySelector('.site-index');
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

    // The section rail uses the same signal: the number of the section you
    // are reading lights up, so it reads as an index rather than decoration.
    sections.forEach((section) => {
      section.classList.toggle('is-current', section.id === sectionID);
    });
  };

  // The one number both the scroll landing and the scroll-spy read from. It has
  // to be one number: `scroll-margin-top` parks a clicked section on this line,
  // so if the spy tested a different line the section would land just short of
  // its own threshold and the menu would highlight the section above it.
  let headerOffset = 0;
  const updateHeaderOffset = () => {
    if (!header) {
      return;
    }

    headerOffset = Math.ceil(header.getBoundingClientRect().height + 16);
    document.documentElement.style.setProperty('--sticky-header-offset', `${headerOffset}px`);
  };

  // The header changes height after load in ways `resize` never reports: the
  // Iosevka webfont swapping in, the nav re-wrapping, browser zoom. A stale
  // offset makes the sticky section headings stick too high and collide with
  // the header, so track the real height instead of sampling it twice.
  if (header && typeof ResizeObserver === 'function') {
    new ResizeObserver(updateHeaderOffset).observe(header);
  }

  if (document.fonts?.ready) {
    document.fonts.ready.then(updateHeaderOffset);
  }

  let frameRequested = false;
  const updateActiveSection = () => {
    // +1 absorbs the sub-pixel rounding of a scroll landing, so a section that
    // has arrived exactly on its own margin counts as reached.
    const threshold = headerOffset + 1;
    let activeSection = sections[0].id;

    sections.forEach((section) => {
      if (section.getBoundingClientRect().top <= threshold) {
        activeSection = section.id;
      }
    });

    // The document runs out of scroll before the last sections can reach the
    // threshold, so clicking the final entry would otherwise leave the one
    // above it lit. At the bottom, the deepest section on screen is the one
    // being read.
    const scrollBottom = window.scrollY + window.innerHeight;
    if (scrollBottom >= document.documentElement.scrollHeight - 2) {
      const onScreen = sections.filter(
        (section) => section.getBoundingClientRect().top < window.innerHeight
      );

      if (onScreen.length) {
        activeSection = onScreen[onScreen.length - 1].id;
      }
    }

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

// The masthead carries the name and scrolls away; the sticky index strip brings
// a small version of it back, but only once the real one is gone -- otherwise
// the page states its own name twice, a few pixels apart.
const setupMastheadCondense = () => {
  const masthead = document.querySelector('.site-masthead');
  const index = document.querySelector('.site-index');

  if (!masthead || !index || typeof IntersectionObserver !== 'function') {
    return;
  }

  // The strip itself covers the bottom of the masthead, so the handover point
  // is the masthead's bottom edge crossing the strip's height, not the viewport
  // top. A rootMargin equal to that height lines the two up.
  const observe = () => {
    const height = Math.ceil(index.getBoundingClientRect().height);
    const observer = new IntersectionObserver(
      ([entry]) => index.classList.toggle('is-condensed', !entry.isIntersecting),
      { rootMargin: `-${height}px 0px 0px 0px`, threshold: 0 }
    );

    observer.observe(masthead);
    return observer;
  };

  let observer = observe();

  if (typeof ResizeObserver === 'function') {
    // Re-anchor when the strip re-wraps or the webfont swaps in; rootMargin is
    // fixed at construction time, so the observer has to be rebuilt.
    let height = Math.ceil(index.getBoundingClientRect().height);
    new ResizeObserver(() => {
      const next = Math.ceil(index.getBoundingClientRect().height);
      if (next !== height) {
        height = next;
        observer.disconnect();
        observer = observe();
      }
    }).observe(index);
  }
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
  setupMastheadCondense();
  setupAbstractDisclosures();
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', setupPage);
} else {
  setupPage();
}
