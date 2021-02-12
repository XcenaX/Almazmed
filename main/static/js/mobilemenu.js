$( document ).ready(function() {
    $("#open_menu")[0].onclick = function(){
        $("#mobilemenu")[0].classList.toggle("show");
        
        $("#mobilemenu-overlay")[0].style.display = "block";
        
    }
    $("#mobilemenu-overlay")[0].onclick = function(){
        $("#mobilemenu")[0].classList.toggle("show");
        
        $("#mobilemenu-overlay")[0].style.display = "none";
        
    }
});