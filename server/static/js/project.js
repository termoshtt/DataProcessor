
function get_project(path) {
  $("section").hide(ANIMATION_SPEED);
  _sync_pipe_api_call({
    "name": "project_html",
    "args": [path,],
  }, function(html){
    $("section.dp-project")
      .empty()
      .append(html);
    enable_link();
    $("table.dp-project").DataTable(DATATABLES_SETTING);
    $(".dp-project").show(ANIMATION_SPEED);
  });
}

function enable_project_link(){
  $("a.dp-project")
    .on("click", function(){
      var path = $(this).attr("dp-path");
      var name = $(this).text();
      get_project(path);
      if(! $(this).hasClass("dp-nav")){
        add_nav_link(path, name, "dp-project");
      }
    });
}
