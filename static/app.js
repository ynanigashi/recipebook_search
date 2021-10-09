$(function(){
    setTimeout("$('.flash').fadeOut('slow')", 5000);
  });

$(document).ready(function() {
    $('.select').select2();
});


$(function () {
  $('input[name="t"]').change(function () {
    if($(this).val() === 'ingredients'){
      $('#ing-select').show()
      $('#search-input').hide()
    }else{
      $('#ing-select').hide()
      $('#search-input').show()
    }
  });
});