const select = $('#dropdown');

function showTab(name) {
    /*
    Shows a specific tab
     */
    name = '#' + name;
    $('.dropdown-container > div').not(name).css('display', 'none');
    $(name).css('display', 'block');
}

// If the value of the dropdown menu changes than the showTab function is called
select.change(function () {
    showTab($(this).val());
});
// Shows the elements that is a part op the choice from the dropdown menu
showTab(select.val());