$(document).ready(function() {
    var numBgs = 6;
    var i = 0;

    function changeBackground() {
        $("html").css("background-image", 'url(/static/img/pics/bg' + i%numBgs + '.jpg)');
        i++;
        setTimeout(function() {
            changeBackground();
        }, 3000);
    }
    
    function changeBackground3() {
        $('html').fadeTo('slow', 0.3, function() {
            $(this).css('background-image', 'url(/static/img/pics/bg' + i%numBgs + '.jpg)');
            i++;
        }).delay(1000).fadeTo('slow', 1);
        setTimeout(function() {
            changeBackground3();
        }, 3000);
    }


    function changeBackground2() {
        var image = $("html");
        image.fadeOut(500, function() {
            image.css("background-image", 'url(/static/img/pics/bg' + i%numBgs + '.jpg)');
            image.fadeIn(500);
            i++;
        });
        setTimeout(function() {
            changeBackground2();
        }, 3000);
    }

    changeBackground();
});


var image = $('#image-holder');
    image.fadeOut(1000, function () {
        image.css("background", "url('images/design-" + newColor + ".jpg')");
        image.fadeIn(1000);
    });