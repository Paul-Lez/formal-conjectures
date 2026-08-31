(() => {
  const revealHash = () => {
    if (!location.hash) return;
    let id;
    try {
      id = decodeURIComponent(location.hash.slice(1));
    } catch {
      return;
    }
    const target = document.getElementById(id);
    if (!target) return;
    const headerHeight = document.querySelector('.title-bar')?.offsetHeight || 0;
    window.scrollTo(0, target.getBoundingClientRect().top + scrollY - headerHeight - 16);
  };

  const queueHashReveal = () => setTimeout(revealHash, 100);
  queueHashReveal();
  addEventListener('load', queueHashReveal, { once: true });
  addEventListener('hashchange', queueHashReveal);

  const menu = document.getElementById('menu-toggle');
  const tree = document.querySelector('.module-tree');
  const filter = document.getElementById('module-filter');
  if (!tree) return;

  const current = tree.querySelector('.current');
  current?.querySelector('a')?.setAttribute('aria-current', 'page');
  const sidebar = tree.closest('.sidebar');
  if (current && sidebar) {
    sidebar.scrollTop += current.getBoundingClientRect().top -
      sidebar.getBoundingClientRect().top - sidebar.clientHeight / 2;
  }

  tree.addEventListener('click', event => {
    if (event.target.closest('a') && menu) menu.checked = false;
  });

  if (!filter) return;
  const leaves = [...tree.querySelectorAll('.leaf')];
  const branches = [...tree.querySelectorAll('details')];
  const initiallyOpen = new WeakMap(branches.map(branch => [branch, branch.open]));

  filter.addEventListener('input', () => {
    const query = filter.value.trim().toLocaleLowerCase();
    for (const leaf of leaves) {
      const link = leaf.querySelector('a');
      leaf.hidden = Boolean(query) &&
        !`${leaf.textContent} ${link?.title || ''}`.toLocaleLowerCase().includes(query);
    }

    for (const branch of branches.slice().reverse()) {
      branch.hidden = Boolean(query) && !branch.querySelector('.leaf:not([hidden])');
      branch.open = query ? !branch.hidden : initiallyOpen.get(branch);
    }
    if (query && sidebar) sidebar.scrollTop = 0;
  });
})();
