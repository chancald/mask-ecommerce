document.getElementById("first_name").value = getSavedValue("first_name");
document.getElementById("last_name").value = getSavedValue("last_name");
document.getElementById("email").value = getSavedValue("email");
document.getElementById("phone").value = getSavedValue("phone");
document.getElementById("street_address").value = getSavedValue("street_address");
document.getElementById("street_address_2").value = getSavedValue("street_address_2");


function saveValue(e){
    let id = e.id;
    let val = e.value;
    localStorage.setItem(id, val);
}
 
function getSavedValue  (v){
    if (!localStorage.getItem(v)) {
        return "";
    }
    return localStorage.getItem(v);
}

