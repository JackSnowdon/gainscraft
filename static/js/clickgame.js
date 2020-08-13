window.localStorage;

$(document).ready(function() {

    var hero_strengh = $("#herostrengh").html()
    var hero_name = $("#heroname").html()
    var enemy_name = $("#enemyname").html()
    var enemy_hp = $("#enemyhp").html()
    var enemy_current_hp = enemy_hp
    var enemy_strengh = $("#enemystrengh").html()
    var enemy_xp = $("#enemyxp").html()
    var kills = 0
    var xp = 0

    $("#attack-button").click(function() {
        basicAttack();
        if (enemy_current_hp <= 0) {
            enemy_current_hp = 0;
            kills++;
            earnXP();
            $("#kill-counter").html(kills);
            $("#xp-counter").html(xp);
            $("#kills-form").val(kills);
            $("#xp-form").val(xp);
            $("#hero-bar").text(hero_name + " Kills " + enemy_name)
        }
        $("#enemyhp").html(enemy_current_hp);
        if (enemy_current_hp == 0) {
            $("#attack-button").attr("disabled", true);
            setTimeout(function() {
                enemy_current_hp = enemy_hp;
                $("#enemyhp").html(enemy_current_hp);
                $("#attack-button").attr("disabled", false);
                $("#commit-kills").css("display", "inline-flex");
            }, 250)
        }
    })


    // Helper Functions

    function basicAttack() {
        var base_attack = Math.floor(hero_strengh / 2);
        var attack_total = (getDiceRoll(hero_strengh) + base_attack) - getDiceRoll(enemy_strengh / 2);
        enemy_current_hp = enemy_current_hp - attack_total;
        $("#hero-bar").text(hero_name + " Attacks For " + attack_total + "HP")
    }

    function earnXP() {
        var base_xp = Math.floor(enemy_xp / 2);
        var final_xp = base_xp + getDiceRoll(enemy_xp);
        xp = parseInt(xp) + parseInt(final_xp);
    }

    function getDiceRoll(x) {
        return Math.floor(Math.random() * x) + 1;
    }

});