$(function(){

    history.pushState('', '', '');

    var hidePages = function() {
        $('.page').hide();
    };

    var sidebarHeight = function() {
        $('#sidebar').height($('#content').height() + 200);
    }
    sidebarHeight();

    var desideitems = function() {
        $('.sideitem').removeClass('on');
    }

    var sideitem = function(page) {
        selector = "[data-page='" + page + "']";
        console.log(selector);
        $('.sideitem').filter(selector).addClass('on');
    }

    $('.mi,.sideitem').click(function (e) {
        var page = $(e.currentTarget).data('page');
        desideitems();
        sideitem(page);
        if (page === 'source') {
            window.open("https://github.com/jrwdunham/old", '_blank');
        } else {
            showPage(page);
            history.pushState(page, '', page);
        }
    });

    var showPage = function (page) {
        hidePages();
        if (page) {
            $('#' + page).show();
        } else {
            $('#about').show();
        }
        sidebarHeight();
    }

    $('#titlebar, #logo').click(function() {
        desideitems();
        hidePages();
        $('#about').show();
        history.pushState('', '', '/');
    });

    $('.faq-q').click(function(e) {
        $q = $(e.currentTarget);
        $a = $q.next('.faq-a');
        if ($a.is(':visible')) {
            $a.slideUp();
        } else {
            $a.slideDown();
        }
    });

    $('.faq-show-all').click(function() {
        $('.faq-a').slideDown();
    });

    $('.faq-hide-all').click(function() {
        $('.faq-a').slideUp();
    });

    window.addEventListener('popstate', function(e) {
        showPage(e.state);
    });

    // Here we detect when the user is navigating to a specific "page" and so
    // we display that "page". Note that this requires the server to route
    // requests to /apps, /doc, etc. to /.
    var path = window.location.pathname;
    // pages = ['/getstarted', '/apps', '/faq', '/doc', '/api'];
    pages = ['/getstarted', '/faq', '/api', '/addingupdating', '/searching',
        '/apps', '/install']
    if (pages.indexOf(path) !== -1) {
        showPage(path.replace('/', ''));
    }

});

