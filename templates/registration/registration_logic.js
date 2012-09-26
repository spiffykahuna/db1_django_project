// function deleteFavourite(event) {
//   var source = (event.target) ? event.target : e.srcElement;  
//   varuosa_id = source.id.split("_")[1];
//   
//   var jqxhr = $.post("/shop/delete_part_from_favourites/" + varuosa_id)
//   .success( function(data) {
//     //alert('Success:\n' + data);  
//     // replace document with returned page
//     document.body.innerHTML = data;
//   })
//   .error(function(data) {
// 	    alert("Error: \n" + data.responseText);    
//   });
// 
// };


$(document).ready(function() {
  
  hideRegSelectors();
  
  $("#id_make").change(function () {
    //alert('test');    
    mark_id = $("#id_make option:selected").val();
    if(mark_id == "0") {
      hideSelectors();
      return
    }
    $("#id_model").empty();
    $("#id_model").append('<option value=0>Select model</option>');
    
    insert_models($("#id_model"), mark_id);   
    
    $("#id_model").show();    
    $("label[for='id_model']").show();
  });
  
  $("#id_model").change(function () {
    //alert('test');    
    mark_id = $("#id_make option:selected").val();
    if(mark_id == "0") {
      hideRegSelectors();
      return
    }
    
    model_id = $("#id_model option:selected").val();	
    if(model_id == "0") {
      $("#id_engine").hide();
      // hide label too
      $("label[for='id_engine']").hide();
      return
    }
    
    append_engines($("#id_engine"), mark_id, model_id);
    
    $("#id_engine").show();    
    $("label[for='id_engine']").show();
  });
  
  
});

function hideRegSelectors() {
  $("#id_model").hide();
  // hide label too
  $("label[for='id_model']").hide(); 
  
  $("#id_engine").hide();
  // hide label too
  $("label[for='id_engine']").hide();
  
};