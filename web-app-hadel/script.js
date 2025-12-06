function updateDateTime() {
    const el = document.getElementById('datetime');
    const now = new Date();
    const formatted = now.toLocaleString('ar-EG', {
        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
        hour: '2-digit', minute: '2-digit', second: '2-digit'
    });
    el.textContent = formatted;
}
updateDateTime();
setInterval(updateDateTime, 1000);

document.addEventListener('DOMContentLoaded', function () {
    const p1 = document.getElementById('p1');
    const p1contentSpan = document.getElementById('p1-content');
    p1contentSpan.textContent = p1.textContent;

    const btnRed = document.getElementById('btn-red');
    const heading1 = document.getElementById('heading1');
    btnRed.addEventListener('click', function () {
        heading1.style.color = 'red';
    });

    const img = document.getElementById('swapImg');
    const hoverImgSrc = 'smiley.gif.mp4';
    const originalSrc = img.src;

    img.addEventListener('mouseover', function () {
        img.src = hoverImgSrc;
        img.style.transform = 'scale(1.03)';
    });
    img.addEventListener('mouseout', function () {
        img.src = originalSrc;
        img.style.transform = 'scale(1)';
    });

    const btnHover = document.getElementById('btn-hover');
    const originalHoverText = btnHover.textContent;
    btnHover.addEventListener('mouseover', function () {
        btnHover.textContent = 'you Thank';
    });
    btnHover.addEventListener('mouseout', function () {
        btnHover.textContent = originalHoverText;
    });

    const btnClick = document.getElementById('btn-click');
    const originalClickText = btnClick.textContent;
    const originalClickColor = btnClick.style.backgroundColor || '';

    btnClick.addEventListener('mousedown', function () {
        btnClick.textContent = 'Me Release';
        btnClick.style.backgroundColor = '#cfe7ff';
        btnClick.style.borderColor = '#73a9ff';
    });

    btnClick.addEventListener('mouseup', function () {
        btnClick.textContent = originalClickText;
        btnClick.style.backgroundColor = originalClickColor;
        btnClick.style.borderColor = '';
    });

    btnClick.addEventListener('mouseleave', function () {
        btnClick.textContent = originalClickText;
        btnClick.style.backgroundColor = originalClickColor;
        btnClick.style.borderColor = '';
    });

    const nameInput = document.getElementById('nameInput');
    nameInput.addEventListener('blur', function () {
        nameInput.value = nameInput.value.toUpperCase();
    });

    nameInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            nameInput.value = nameInput.value.toUpperCase();
            nameInput.blur();
        }
    });
});
