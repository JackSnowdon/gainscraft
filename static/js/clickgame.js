window.localStorage;

$(document).ready(function() {

    var hero_strengh = $("#herostrengh").html()
    var enemy_hp = $("#enemyhp").html()
    var enemy_current_hp = enemy_hp
    var enemy_strengh = $("#enemystrengh").html()
    var enemy_xp = $("#enemyxp").html()
    var kills = 0

    $("#attack-button").click(function() {
        enemy_current_hp = enemy_current_hp - hero_strengh;
        if (enemy_current_hp < 0) {
            enemy_current_hp = 0;
            kills++;
            $("#kill-counter").html(kills);
        }
        $("#enemyhp").html(enemy_current_hp);
        if (enemy_current_hp == 0) {
            $("#attack-button").attr("disabled", true);
            setTimeout(function() {
                enemy_current_hp = enemy_hp;
                $("#enemyhp").html(enemy_current_hp);
                $("#attack-button").attr("disabled", false);
            }, 1000)
        }
    })
});