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

function  getUserCarDetails() {
  var userCar = {};
  $.getJSON('/shop/json/get_user_car_details/', function(details) {
    //var details = details[0];
    if (details.fields != null) {
      userCar.make_id = details.fields.auto_mark;
      userCar.model_id = details.fields.auto_mudel;
      userCar.engine_id = details.fields.mootor;
    };
    
    if (userCar.make_id != null) {    
      $("#id_make [value='" + userCar.make_id + "']").attr("selected", "selected"); 
      
      insert_models($("#id_model"), userCar.make_id, function() {
	$("#id_model [value='" + userCar.model_id + "']").attr("selected", "selected");
      }
      );
      
      
      if (userCar.model_id != null) {    
	$("#id_model [value='" + userCar.model_id + "']").attr("selected", "selected");
	if (userCar.make_id != null) {
	  append_engines($("#id_engine"), userCar.make_id, userCar.model_id, selectUserEngine);
	  
	}
	
	if (userCar.engine_id != null) {    
	  $("#id_engine [value='" + userCar.engine_id + "']").attr("selected", "selected");	  
	};
      };
    } else {
//       $("#id_make").empty();
//       $("#id_make").append('<option value=0>Select make</option>');
      
      $("#id_model").empty();
      $("#id_model").append('<option value=0>Select model</option>');
      
      $("#id_engine").empty();
      $("#id_engine").append('<option value=0>Select engine</option>');
      
      
    };
    
  }).error(function() { 
    hideRegSelectors();    
  });	  
  return userCar;
};


$(document).ready(function() {
  
  //hideRegSelectors();
  userCar = getUserCarDetails();
  
  
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
    
    append_engines($("#id_engine"), mark_id, model_id, selectUserEngine);
    
    $("#id_engine").show();    
    $("label[for='id_engine']").show();
  });
  
  selectUserEngine();
});

function hideRegSelectors() {
  $("#id_model").hide();
  // hide label too
  $("label[for='id_model']").hide(); 
  
  $("#id_engine").hide();
  // hide label too
  $("label[for='id_engine']").hide();
  
};

function selectUserEngine(engine_id) {
  $("#id_engine [value='" + userCar.engine_id + "']").attr("selected", "selected"); 
};
