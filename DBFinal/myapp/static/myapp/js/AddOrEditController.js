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
function setSpeciesID(sId) {
    var setValue = document.getElementById("update")
    setValue.value = sId
}
function setSpeciesEditValues(id, commonName, scientificName, region, conservationStatus, group) {
    document.getElementById("id_cName").value = commonName
    document.getElementById("id_sName").value = scientificName
    setSpeciesID(id)
    setRegion = document.getElementById("id_reg")
    setStatus = document.getElementById("id_cStatus")
    setGroup = document.getElementById("id_grp")
    for(var i = 0, j = setRegion.options.length; i < j; ++i) {
        if(setRegion.options[i].innerHTML === region) {
           setRegion.selectedIndex = i;
           break;
        }
    }
    for(var i = 0, j = setStatus.options.length; i < j; ++i) {
        if(setStatus.options[i].innerHTML === conservationStatus) {
           setStatus.selectedIndex = i;
           break;
        }
    }
    for(var i = 0, j = setGroup.options.length; i < j; ++i) {
        if(setGroup.options[i].innerHTML === group) {
           setGroup.selectedIndex = i;
           break;
        }
    }
}
function setGroupID(groupID) {
    var setValue = document.getElementById("update")
    setValue.value = groupID
}

function setGroupEditValues(id, group) {
    document.getElementById("id_grp").value = group
    setGroupID(id)
}
function setStatusID(statusId) {
    var setValue = document.getElementById("update");
    setValue.value = statusId;
}

function setStatusEditValues(id, region) {
    document.getElementById("id_stat").value = region;
    setStatusID(id);
}

function setRegionID(regionID) {
    var setValue = document.getElementById("update")
    setValue.value = regionID
}

function setRegionEditValues(id, region) {
    document.getElementById("id_reg").value = region
    setRegionID(id)
}