const openModalButtons = document.querySelectorAll('[data-modal-open]');
const closeModalButtons = document.querySelectorAll('[data-close-button');
const overlay = document.getElementById('overlay');

overlay.addEventListener('click', () =>{
    const modals = document.querySelectorAll('.modal.active');
    modals.forEach(modal => {
        closeModal(modal)
    });
});

openModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = document.querySelector(button.dataset.modalOpen);
        openModal(modal);
    });
});

closeModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = button.closest('.modal');
        closeModal(modal);
    });
});

function openModal(modal) {
    if (modal == null){
        return
    }
    modal.classList.add('active')
    overlay.classList.add('active')
}

function closeModal(modal) {
    if (modal == null){
        return
    }
    modal.classList.remove('active')
    overlay.classList.remove('active')
}