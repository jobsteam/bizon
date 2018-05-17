$(function() {
    $('.auto-height').matchHeight({
        byRow: true,
        property: 'height',
        target: null,
        remove: false
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
    $('.marquee').simplemarquee({
        speed: 50,
        cycles: 5,
        space: 0,
        pause: 0,
        delayBetweenCycles: 0,
        handleHover: true,
        handleResize: true
    });
});