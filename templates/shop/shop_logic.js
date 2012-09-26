// $(document).ajaxSend(function(event, xhr, settings) {
//     function getCookie(name) {
//         var cookieValue = null;
//         if (document.cookie && document.cookie != '') {
//             var cookies = document.cookie.split(';');
//             for (var i = 0; i < cookies.length; i++) {
//                 var cookie = jQuery.trim(cookies[i]);
//                 // Does this cookie string begin with the name we want?
//                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }
//     function sameOrigin(url) {
//         // url could be relative or scheme relative or absolute
//         var host = document.location.host; // host + port
//         var protocol = document.location.protocol;
//         var sr_origin = '//' + host;
//         var origin = protocol + sr_origin;
//         // Allow absolute or scheme relative URLs to same origin
//         return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
//             (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
//             // or any other URL that isn't scheme relative or absolute i.e relative.
//             !(/^(\/\/|http:|https:).*/.test(url));
//     }
//     function safeMethod(method) {
//         return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
//     }
// 
//     if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
//         xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
//     }
// });

$(document).ready(function() { 
   
   $("#selectors").empty();
   
   $("#selectors").append('<select class="selector" id="model_select" size="0"  name="model_select"></select><br>');
   $("#model_select").append('<option value=0>Select model</option>');           
   
   $("#selectors").append('<select class="selector" id="motor_select" size="0"  name="motor_select"></select><br>');
   $("#motor_select").append('<option value=0>Select engine</option>');
   
   $("#selectors").append('<select class="selector" id="category_select" size="0"  name="category_select"></select><br>');
   $("#category_select").append('<option value=0>Select category</option>');
   
   hideSelectors();
   
   $("#mark_select").append('<option value=0>Select mark</option>');            
   $.getJSON('/shop/json/get_car_mark', function(carMarks) {
        for (var i in carMarks){            
	    $("#mark_select").append(new Option(carMarks[i].fields.mark, carMarks[i].pk));
        };
   });
   
   $("#mark_select").change(function () {
	  hideSelectors();
	  // get selected id value
          mark_id = $("#mark_select option:selected").val();
	  if(mark_id == "0") {
	    hideSelectors();
	    return
	  }
	  
	  //if model selector exists
	  if($("#model_select").length == 0) {
	    
	    //$("#selectors").append('<select id="model_select" simodelze="0"  name="model_select"></select>');	    
	    insert_models($("#model_select"), mark_id);
	    $("#model_select").show();
	    
	  } else {
	    // if it already exists ->  fill with  new values
	    $("#model_select").empty();
	    $("#model_select").append('<option value=0>Select model</option>');           
	    
	    insert_models($("#model_select"), mark_id);
	    
	    $("#model_select").show();
	  }
        });

    $("#model_select").change(function () {
	mark_id = $("#mark_select option:selected").val();
	if(mark_id == "0") {
	  hideSelectors();
	  return
	}
	
	model_id = $("#model_select option:selected").val();	
	if(model_id == "0") {
	  hideSelectors();
	  return
	}
	
	append_engines($("#motor_select"), mark_id, model_id);
	
	$("#motor_select").show();
       
    });
    
    $("#motor_select").change(function () {
       
        $("#category_select").empty();
        $("#category_select").append('<option value=0>Select category</option>');
        
	$.getJSON('/shop/json/get_goods_categories/', function(categories) {
		  for (var i in categories){
		      $("#category_select").append(new Option(categories[i].fields.nimetus, categories[i].pk));            
		  };
	    });	     
	    $("#category_select").show();
       
    });
    
    $("#search_form").submit(function() {
      search_items();
      return false;
    });
   
     
});

function hideSelectors() {
  $("#model_select").hide();
  $("#motor_select").hide();
  $("#category_select").hide();
}

function search_items() {
  
  var mark_id = $("#mark_select option:selected").val();
  var mark_text = $("#mark_select option:selected").text();
  
  var model_id = $("#model_select option:selected").val();
  var model_text = $("#model_select option:selected").text();
  
  var motor_id = $("#motor_select option:selected").val();
  var motor_text = $("#motor_select option:selected").text();
  
  var category_id = $("#category_select option:selected").val();
  var category_text = $("#category_select option:selected").text();
  
  var outData = { 
    "mark_id": mark_id,
    "mark_text": mark_text,
    "model_id": model_id,
    "model_text": model_text,
    "motor_id": motor_id,
    "motor_text": motor_text,
    "category_id": category_id,
    "category_text": category_text    
  };
  
  var jqxhr = $.post("/shop/search/", outData)
  .success( function(data) {
     /*
      * [{"pk": 1, "model": "shop.varuosa", "fields": {"monteerimis_koht": "parem lohzheron", "katalogi_nr": "ALM-3242", "kulg": "parem", "kauba_kategooria": 1, "mootmed": "40x50"}}]
      */ 
//       var count = 0;
//       varuosad = $.parseJSON(data);
//       $("#search_response").empty(); 
//       //$("#search_response").append(data);      
//       table = '<table border="1" width="100%" align="center">';
//       //$("#search_response").append('<table border="1">');
//       for (var i in varuosad){
// 	table +='<tr>';
// 	table += '<td>' + varuosad[i].fields.katalogi_nr + '</td>' ;
// 	table += '<td>' + varuosad[i].fields.monteerimis_koht + '</td>' ;
// 	table += '<td>' + varuosad[i].fields.kulg + '</td>';
// 	table += '<td>' + varuosad[i].fields.mootmed + '</td>';
// 	table += '<td onclick="addFavourite(event)" id="varuosa_' + varuosad[i].pk + '">' + ++count + '</td>';
// 	table +='</tr>';
// // 	$("#search_response").append('<tr>');
// // 	$("#search_response").append('<td>' + varuosad[i].fields.katalogi_nr + '</td>' );
// // 	$("#search_response").append('<td>' + varuosad[i].fields.monteerimis_koht + '</td>' );
// // 	$("#search_response").append('<td>' + varuosad[i].fields.kulg + '</td>' );
// // 	$("#search_response").append('<td>' + varuosad[i].fields.mootmed + '</td>' );
// // 	$("#search_response").append('</tr>');
//       };
//       table +='</table>';


      $("#search_response").empty();
      $("#search_response").append(data);
      //$("#search_response").append('</table>');
      //$("#search_response").append(data);
	    //alert("Data Loaded: " + data);    
  })
  .error(function(data) {
	    alert("Error: \n" + data.responseText);    
  });

/*
$.ajax({
  type: 'POST',
  url: "/shop/search/",
  processData: true,
  data: { name: "John", time: "2pm" }mootori_tyyp
  //success: success,
  //dataType: dataType
});*/
	 
}

function insert_models(select, mark_id, callback) {
  select.empty();
  select.append('<option value=0>Select model</option>');
  // get model data
  $.getJSON('/shop/json/get_car_model_by_mark_id/' + mark_id , function(carModels) {
		  for (var i in carModels){
		    
		      // model
		      optionText = carModels[i].fields.mudel;
		      optionText += ' ';
		      // dates released
		      if (carModels[i].fields.valjalaske_algus == null) {
			optionText += '';
		      } else {
			stardDate = new Date(carModels[i].fields.valjalaske_algus);
			optionText += stardDate.getFullYear() + '/' + (stardDate.getMonth()+1);
		      }
			
		      if (carModels[i].fields.valjalaske_lopp == null) {
			optionText += '';
		      } else {
			optionText += ' - ';			
			endDate = new Date(carModels[i].fields.valjalaske_lopp);
			optionText += endDate.getFullYear() + '/' + (endDate.getMonth()+1);			
		      }
		      
		      select.append(new Option(optionText, carModels[i].pk));
		  }; 
		  if ( callback ){ 
                    callback(); 
		  } 
		  
  });	      
}

function append_engines(selector, mark_id, model_id, callback) {
	selector.empty();
	selector.append('<option value=0>Select engine</option>');
	
	$.getJSON('/shop/json/get_engines_by_make_and_model/' + mark_id +'/' + model_id, function(motors) {
		  for (var i in motors){
		      motorText = motors[i].fields.nimetus + ' ' + motors[i].fields.voimsus_kw + ' kW ' + motors[i].fields.mootori_tyyp;
		      selector.append(new Option(motorText, motors[i].pk));            
		  };
		  if ( callback ){ 
		     callback();	  
		  } 
	});	
};

function addFavourite(event) {
  var source = (event.target) ? event.target : e.srcElement;  
  varuosa_id = source.id.split("_")[1];
  
  var jqxhr = $.post("/shop/add_part_to_favourites/" + varuosa_id, 'new User here')
  .success( function(data) {
    alert('Success:\n' + data);    
  })
  .error(function(data) {
	    alert("Error: \n" + data.responseText);    
  });

};

function deleteFavourite(event) {
  var source = (event.target) ? event.target : e.srcElement;  
  varuosa_id = source.id.split("_")[1];
  
  var jqxhr = $.post("/shop/delete_part_from_favourites/" + varuosa_id)
  .success( function(data) {
    //alert('Success:\n' + data);  
    // replace document with returned page
    document.body.innerHTML = data;
  })
  .error(function(data) {
	    alert("Error: \n" + data.responseText);    
  });

};