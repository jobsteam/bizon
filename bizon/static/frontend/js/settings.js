$(function() {
    $('.auto-height').matchHeight({
        byRow: true,
        property: 'height',
        target: null,
        remove: false});

    $('.marquee').animate({
        opacity: 1.0
    }, 2000);

    $('.marquee').marquee({
        pauseOnHover: true,
        speed: 40,
        direction: 'left',
        duplicated: true,
        startVisible: true
    });
    $(".sand").click(function() {
        if ($("div.menu").is(":hidden")) {
            $(".menu").show();
        }
        else {
            $(".menu").hide();
        }
        return false;
    });
    $(".close-popup").click(function() {
        $(".popup-bg").hide();
        return false;
    });
    $(".search").click(function() {
        $(".search-form").show();
        $(".search-text").focus();
        return false;
    });
});