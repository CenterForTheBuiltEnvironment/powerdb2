function VQuery(url, callback, allResultsCallBack){
  var that = this;

  this.genConstraint = function(excludeLast){
    var constraint = '';
    var first = true;
    var tags = [];
    var vals = [];
    var ops = [];
      
    $('.vq-constraint-tag').each(function(){
      tags.push($(this).val());
    });

    $('.vq-constraint-val').each(function(){
      vals.push($(this).val());
    });

    $('.vq-constraint-op-btn').each(function(){
      ops.push($(this).text());
    });

    if (excludeLast){
      tags.pop(); vals.pop(); ops.pop(); 
    }
    _.zip(tags, ops, vals).forEach(function(d){
      var and = '';
      var not = '';
      if (d[1] == '≠') { 
        not = 'not ';
        d[1] = '=';
      }
      if (!first) and = 'and ';
      first = false;
      constraint += and + not + d[0] + d[1] + "'" + d[2] + "' ";
    });
    if (constraint!='') constraint = "where " + constraint;
    return constraint;
  };

  this.initConstraint = function(id){
    $('#vq-constraint-op-'+id).click(function(){
      var txt = $(this).text();
      if (txt == "="){
        $(this).text("≠");
      } else if (txt=="≠"){
        $(this).text("~");
      } else{
        $(this).text("=");
      }
    });

    $('#vq-constraint-val-'+id).focus(function(){
      var val = $(this).val();
      var tag = $('#vq-constraint-tag-'+id).val()
      var query = "select distinct " + tag  + " " + that.genConstraint(true);
      console.log(query)
      $.ajax({
        url: url,
        type: "post",
        data: query,
        success: function(data){
          var auto = $('#vq-constraint-val-'+id).typeahead();
          auto.data('typeahead').source = data;
        }
      });
    });
  };
    
  $('#vquery').html(' \
      <div id="vq-constraints"> \
        <div id="vq-constraint-cont-0" class="vq-constraint-row"> \
          <input id="vq-constraint-val-0" class="vq-constraint-val typeahead" type="text"> \
        </div> \
      </div> \
      \
      <div id="vq-search-row"> \
        <button id="vq-search" style="float:right;" data-loading-text="Loading...." class="btn"> \
          <i class="icon-search"></i> Search \
        </button> \
      </div> \
      <br style="clear:both;">\
  ');
 
    
  $('#vq-search').click(function(){
// var query = "select * " + that.genConstraint(false);
// hack to get metadata, uuid, readings in one query
    // var query = "apply null to data before now limit 1 " + that.genConstraint(false);
    _streams = [];
    var query = $("#vq-constraint-val-0").val();
    console.log("Query : " + query);
    $(this).button('loading');
    try{
    $.ajax({
      url: "/search/getresultsStatus/",
      type: "post",
      data: query,
      timeout: 10000,
      success: function(data){
	console.log("Data returned : " + data);
        callback(data);
        $('#vq-search').button('reset');
	$.ajax({
	      url: "/search/getExtraResults/",
	      type: "post",
	      data: query,
	      timeout: 10000,
	      success: function(data){
		console.log("Data returned : " + data);
		allResultsCallBack(data);
		
	      },
	      failure:  function(){
			console.log("query failure"); }
	    });

      },
      failure:  function(){ $('#vq-search').button('reset');
		console.log("query failure"); }
    });
     }
     catch(e)
	{
		console.log(" AJAX failure");
	}
  });
    
  this.initConstraint(0);
  $.ajax({
    url: url,
    type: "post",
    data: "select distinct",
    success: function(res){
      var auto = $('#vq-constraint-tag-0').typeahead();
      auto.data('typeahead').source = res
    }
  });
  $('#vq-constraint-val-0').focus();
}
