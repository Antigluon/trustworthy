function initalize() {
    var myFullpage = new fullpage('#fullpage', {
        anchors:['home', 'about', 'demo'],
        sectionsColor: ['#00A7E1', '#003459', '#ffffff'],
        navigation: true,
        navigationPosition: 'right',
        css3: true,
        navigation: true,
        navigationPosition: 'right',
        slidesNavigation: true,
        slidesNavPosition: 'bottom',
        continuousHorizontal: true,
        dragAndMove: true,
        normalScrollElements: '.demoappscrollable',
        recordHistory: false,
    });
}

window.onresize = function() {
    if (document.getElementById("demoapp")) {
        const dt = document.getElementsByClassName("demotitle")[0];
        const dapw = document.getElementById("demoapp").offsetWidth;
        dt.setAttribute("style","width:"+dapw+"px");
    }
}

window.addEventListener( "load", function () {
    initalize();

    document.getElementById('url').select();

    function sendData() {
        const XHR = new XMLHttpRequest();
        const FD = new FormData(form);
        XHR.addEventListener( "load", function(event) {
            if (event.target.responseText !== "ERROR") {
                const slide = '<div class="section"><div id="demoapp"></div></div>';
                let page = document.getElementById('fullpage').innerHTML;
                document.getElementById('fullpage').innerHTML = page + slide;

                document.getElementById('demoapp').classList.add('demoappscrollable');
                let resp = JSON.parse(event.target.responseText);
                document.getElementById('demoapp').innerHTML = '<div class="demotitle"><h1 class="title">' + resp.title + '</h1><h1 class="close" id="close">x</h1></div><hr style="opacity: 0;">' + resp.text;
                
                fullpage_api.destroy('all');
                initalize();
                if (document.getElementById("demoapp")) {
                    const dt = document.getElementsByClassName("demotitle")[0];
                    const dapw = document.getElementById("demoapp").offsetWidth;
                    dt.setAttribute("style","width:"+dapw+"px");
                }
                fullpage_api.moveTo('demo');

                document.getElementById('close').onclick = function() {
                    fullpage_api.moveTo('home');
                    window.location.reload(false);
                }
            }
        });

        XHR.addEventListener( "error", function( event ) {
            alert('Oops! Something went wrong.');
        });
        
        XHR.open("POST", "/api");
        XHR.send(FD);
    }

    // Access the form element...
    const form = document.getElementById("demoform");
    
    // ...and take over its submit event.
    form.addEventListener( "submit", function ( event ) {
        event.preventDefault();
        sendData();
    });
});