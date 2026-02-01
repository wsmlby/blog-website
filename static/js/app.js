document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle (if we still have one, though new design doesn't show it explicitly)
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Dynamically add copy buttons to code blocks generated from markdown
    const codeBlocks = document.querySelectorAll('.prose pre');
    codeBlocks.forEach(pre => {
        if (pre.parentElement.classList.contains('code-wrapper')) return;

        const wrapper = document.createElement('div');
        wrapper.className = 'relative group code-wrapper';
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(pre);

        const button = document.createElement('button');
        button.className = 'copy-btn absolute top-4 right-4 p-2 rounded-lg bg-white/10 hover:bg-white/20 text-white/50 hover:text-white transition-all opacity-0 group-hover:opacity-100 focus:opacity-100 outline-none';
        button.innerHTML = `
            <span class="material-symbols-outlined text-sm">content_copy</span>
            <span class="copy-tooltip absolute -top-10 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-[10px] font-bold uppercase tracking-widest py-1 px-2 rounded border border-white/10 opacity-0 pointer-events-none transition-opacity duration-300">Copied!</span>
        `;
        wrapper.appendChild(button);

        button.addEventListener('click', (e) => {
            e.preventDefault();
            const code = pre.querySelector('code');
            const textToCopy = code ? code.innerText : pre.innerText;

            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(textToCopy).then(() => {
                    const tooltip = button.querySelector('.copy-tooltip');
                    if (tooltip) {
                        tooltip.style.opacity = 1;
                        setTimeout(() => {
                            tooltip.style.opacity = 0;
                        }, 1500);
                    }
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            }
        });
    });
});
