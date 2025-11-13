// Close offcanvas after selecting a tab (applies to templates that use offcanvas + nav-pills)
document.addEventListener('DOMContentLoaded', function () {
  const pillButtons = document.querySelectorAll('[data-bs-toggle="pill"]');
  pillButtons.forEach(btn => {
    btn.addEventListener('shown.bs.tab', () => {
      const off = document.querySelector('.offcanvas.show');
      if (off) {
        const instance = bootstrap.Offcanvas.getInstance(off);
        if (instance) instance.hide();
      }
    });
  });
});