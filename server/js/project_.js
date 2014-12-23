
function get_project(path) {
  $.blockUI(block_setting);
  $("section.dp-project").empty();
  $.post(api_url, {
      "type": "pipe", 
      "name": "project_html",
      "args": JSON.stringify([path,]), 
    }, function (res) {
      var name = res["name"];
      var table_html = res["html"];
      $("section.dp-project")
        .empty()
        .append(table_html);
      var li$ = $("<li>").appendTo("ol#LocationBar");
      $("<a>")
        .attr("dp-path", path)
        .append(name)
        .appendTo(li$);
      enable_project_link();
      enable_editable_comment();
    }).always(function(){
      $.unblockUI();
    });
}

function show_project(){
  $("section.dp-projectlist").hide(animation_speed);
  $("section.dp-run").hide(animation_speed);
  $("a.dp-projectlist").show(animation_speed);
  $("a.dp-run").show(animation_speed);
  $(".dp-project").show(animation_speed);
}

function enable_project_link(){
  $("a.dp-project")
    .off("click")
    .on("click", function(){
      var path = $(this).attr("dp-path");
      get_project(path);
      show_project();
    });
  _enable_nav();
}
