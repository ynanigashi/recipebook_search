$(function(){
    setTimeout("$('.flash').fadeOut('slow')", 5000);
});

$(function() {
    $('.select').select2({
        placeholder: "Select ingredients"
      })
})

$(function() {
  let triggerTabList = [].slice.call(document.querySelectorAll('#nav-tab a'))
  triggerTabList.forEach(triggerEl => {
    let tabTrigger = new bootstrap.Tab(triggerEl)
    triggerEl.addEventListener('click', function(e){
      e.preventDefault()
      tabTrigger.show() 
    })    
  })
})

function select_keyword_tab(){
  let tabTrigger = new bootstrap.Tab(document.querySelector('#nav-word-tab'))
  tabTrigger.show()
}

$(function() {
    $('#select-ings').on('change', function(){
      $('#form-ings').submit()
    })
})

$(function() {
  let catCheckBoxs = document.querySelectorAll('#catCheckBoxs div input')
  catCheckBoxs.forEach(catCheckBox => {
    catCheckBox.addEventListener('click', function(){
      $('#form-ings').submit()
    })
  })
})