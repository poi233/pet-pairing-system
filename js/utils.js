function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[#?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });
    return vars;
}

function parseJwt(token) {
    var base64Url = token.split('.')[1];
    var base64 = decodeURIComponent(atob(base64Url).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(base64);
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function clearCookie(name) {
    setCookie(name, "", -1);
}

function logout() {
    clearCookie("id_token");
    // window.location.href = "https://petpairing.auth.us-west-2.amazoncognito.com/login?client_id=2stvr0481459s1gve6onvtr640&logout_uri=https://petpairing.auth.us-east-1.amazoncognito.com/login?response_type=token&client_id=2stvr0481459s1gve6onvtr640&redirect_uri=https://s3.amazonaws.com/pet-pairing/index.html  \n";
    window.location.href = "https://petpairing.auth.us-east-1.amazoncognito.com/login?response_type=token&client_id=2stvr0481459s1gve6onvtr640&redirect_uri=https://s3.amazonaws.com/pet-pairing/index.html";
}
