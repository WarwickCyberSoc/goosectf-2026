const express = require('express');
var session = require('express-session');
const path = require('path');

const app = express();
const port = 5000;

let users = [];

app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(session({secret:'WvWW1Yu3Qr2UT2D3fOb1NwN6T0qOWKID'}));
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
const flagText = "GooseCTF{N0t_4_g00d_Pr0t0TYP3_wH0oP5}";

Object.prototype.admin = false;

function merge(target, source) {
    for (let key in source) {
        if (key === '__proto__') continue;
        if (typeof target[key] === 'object' || typeof target[key] === 'function') {
            merge(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
}

app.get('/', function (req, res) {
    console.log(users);
    return res.render('index');
});

app.post('/register', function (req, res) {
    if (!req.body.username || !req.body.password){
        return res.status(400).json({error: "Empty field(s)"})
    }
    let data = req.body;
    delete data.admin;
    
    let thisUser = {};
    merge(thisUser, data);
    users.push(thisUser);


    return res.redirect('/?message=Successfully%20registered%21&bg=%231b672e');
});

app.post('/login', function (req, res) {
    const { username, password } = req.body;
    const userRecord = users.find(u => u.username === username && u.password === password);

    if (userRecord) {
        req.session.user = userRecord;
        return res.redirect('/dashboard');
    }
    
    return res.redirect('/?message=Incorrect%20Credentials&bg=%2378241e')
});

app.get('/dashboard', function (req, res) {
    if (req.session.user?.username) {
        if (req.session.user.admin === true){
            return res.render('dashboard', {flag: flagText, user: req.session.user})
        }
        return res.render('dashboard', {flag: "", user: req.session.user});
    }
    return res.redirect('/');
});

app.get('/logout', function (req, res) {
    req.session.destroy();
    return res.redirect('/');
});

app.listen(port, () => {
    console.log(`Now listening on port ${port}`);
});