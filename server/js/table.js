/**
 * send comment to server
 */
function send_comment(comment, path){
    $.post("/cgi-bin/api.cgi",
        {
            "type": "pipe",
            "name": "add_comment",
            "args": JSON.stringify([comment, path])
        }, notice_api_result, "json"
    );
}


/**
 * generate a wedget <div/> in section#Widgets
 */
function widget_html(title, widgets){
    var $widget_html = $("<div>").addClass("Widget");
    $("<h2>")
        .addClass("WidgetTitle")
        .text(title)
        .appendTo($widget_html);
    $("<button>")
        .text("hide")
        .bind("click", function(event){
            $(this).parent().remove();
        })
        .appendTo($widget_html);

    for(var i=0; i<widgets.length; i++){
        $(widgets[i])
            .addClass("WidgetBody")
            .appendTo($widget_html);
    }
    // create hide and show checkbox
    var $items = $widget_html.find("table.childrenTableWidget>thead>tr.items>th");
    var $div_check = $("<div>").addClass("hide-show");
    var previous_group = "";
    var $group = "";
    var $span = "";
    var $input = "";
    for (var i = 0; i<$items.length;i++){
        // checked item strings are set to bold
        var now_item = $items.eq(i).attr("class");
        var group = $items.eq(i).data("group");
        if (group != previous_group) {
            $div_check.append($group);
            $group = $("<div>").text(": ");
            $span = $("<span>").text(group).addClass("group")
                .css("font-weight", "bold")
                .data("group", group).data("show", true);
            $group.prepend($span);
        }
        $span = $("<span>").text(now_item).addClass("item").css("font-weight", "bold")
            .data("item", now_item).data("show", true);
        $group.append($span);
        $group.append($("<span>").text(" "));
        previous_group = group;
    }
    $div_check.append($group);
    $widget_html.find("table.childrenTableWidget").before($div_check);
    return $widget_html;
}

/**
 * ready table
 */
function ready_table(){
    $("section, nav#Projects")
        .off("click", "table>tbody>tr>td.name")
        .off("click", "table>tbody>tr>td.comment")
        .off("blur", "table>tbody>tr>input.comment");
    $("section, nav#Projects")
        .on("click", "table>tbody>tr>td.name", function(event){
            var name = this.innerHTML;
            var path = $(this).parent().attr("path");
            $.getJSON("/cgi-bin/body.cgi",
                {
                    "type": "Widgets",
                    "path": path,
                    "table_type": "children"
                }, function(widgets){
                    var $widget_html = widget_html(name, widgets);
                    $("section#Widgets").append($widget_html);
                    ready_table();
                });
        })
        .on("click", "table>tbody>tr>td.comment", function(event){
            var comment = this.innerHTML;
            var path = $(this).parent().attr("path");
            var $parent = $(this).parent();
            $(this).replaceWith(
                $("<input>")
                    .addClass("comment")
                    .attr("value", comment)
                    .attr("path", path)
                );
            $parent.find("input.comment").focus();
        })
        .on("blur", "table>tbody>tr>input.comment", function(event){
            var comment = this.value;
            var path = $(this).parent().attr("path");
            send_comment(comment, path);
            $(this).replaceWith(
                $("<td>")
                    .addClass("comment")
                    .text(comment)
                    .attr("path", path)
                );
        });

/**
 * Sort table
 */
    var sortOrder = 1;
    $("section").off("click", "div.Widget>table>thead>tr.items>th");
    $("section").on("click", "div.Widget>table>thead>tr.items>th",
                    function(){
                        // get tbody
                        var $rows = $(this).parents("table").children("tbody").find("tr");
                        var col = $(this).index();

                        // Sort
                        $rows.sort(function(a, b){
                            return compare(a, b, col) * sortOrder;
                        });
                        $(this).parents("table").children("tbody")
                            .empty().append($rows);

                        // update mark of sort order
                        var arrow = sortOrder === 1 ? "▲" : "▼";
                        $(this).parent().find('span').remove();
                        var span = $('<span>');
                        $(this).prepend(span);
                        $(this).find('span').text(arrow);

                        // change sort order
                        sortOrder *= - 1;
 });
    function compare(a, b, col) {
        var _a = $(a).find('td').eq(col).text();
        var _b = $(b).find('td').eq(col).text();
        if (isNaN(parseFloat(_a))) {
            // var __a = _a.toLowerCase();
            // var __b = _b.toLowerCase();
            var __a = _a;
            var __b = _b;
            if (__a < __b) //sort string ascending
                return -1;
            if (__a > __b)
                return 1;
            return 0; //default return value (no sorting)
        } else {
            var __a = parseFloat(_a);
            var __b = parseFloat(_b);
            return (__a - __b);
        }
    };

/**
 * Hide or Show table Item
*/
    $("section")
        .off("click", "div.hide-show>div>span.item");
    $("section").on("click", "div.hide-show>div>span.item",
                    function(){
                        var now_item = $(this).data("item");
                        var selector = "table th." + now_item +
                                ", table td." + now_item;
                        console.log($(this).data("show"));
                        if ($(this).data("show")){
                            $(this).css("font-weight", "normal").css("color", "gray");
                            $(this).parents("div.Widget").find(selector).hide();
                            $(this).data("show", false);
                        } else {
                            $(this).css("font-weight", "bold").css("color", "black");
                            $(this).parents("div.Widget").find(selector).show();
                            $(this).data("show", true);
                        }
                        correct_width_table($(this).parents("div.Widget")
                                            .find("table.childrenTableWidget"));
                    });

    function correct_width_table($table_object){
        var $groups = $table_object.find("thead>tr.group>th");
        // create group name list
        var group_list = [];
        for (var i = 0; i<$groups.length; i++){
            group_list.push($groups.eq(i).data("group"));
        }
        // count group number
        var group_num = {};
        for (var i in group_list){
            group_num[group_list[i]] = 0;
        }
        // count each group number
        var $items = $table_object.find("thead>tr.items>th");
        for (var i = 0; i<$items.length; i++){ //
            if ($items.eq(i).is(":visible")) {
                for (var j in group_list){
                    if ($items.eq(i).data("group") == group_list[j]){
                        group_num[group_list[j]] += 1;
                        break;
                    }}}}
        // correct width of table.
        for (var i = 0; i<$groups.length; i++){
            $groups.eq(i).attr("colspan", group_num[$groups.eq(i).data("group")]);
            if (group_num[$groups.eq(i).data("group")] == 0){
                $groups.eq(i).hide();
            } else {
                $groups.eq(i).show();
            }}}


    $("section")
        .off("click", "div.hide-show>div>span.group");
    $("section").on("click", "div.hide-show>div>span.group",
                    function(){
                        var now_group = $(this).data("group");
                        var selector = "table th[data-group=" + now_group + "]" +
                                ", table td[data-group=" + now_group + "]";
                        if ($(this).data("show")){
                            $(this).css("font-weight", "normal").css("color", "gray");
                            $(this).siblings().css("font-weight", "normal").css("color", "gray");
                            $(this).siblings().data("show", false);
                            $(this).data("show", false);
                            $(this).parents("div.Widget").find(selector).hide();
                        } else {
                            $(this).css("font-weight", "bold").css("color", "black");
                            $(this).siblings().css("font-weight", "bold").css("color", "black");
                            $(this).siblings().data("show", true);
                            $(this).data("show", true);
                            $(this).parents("div.Widget").find(selector).show();
                        }
                        correct_width_table($(this).parents("div.Widget").find("table.childrenTableWidget"));
                    });


            }
