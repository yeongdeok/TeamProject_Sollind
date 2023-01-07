var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

const app = require('express')();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));


var update = false;
var io = require("socket.io")();
io.listen(5454); 
io.sockets.on("connection",function(socket){
	setInterval(() => {
		if (update) {
			io.sockets.emit("return", {id: "test", text: "tttt"});
			update = false;
		}
	}, 60000);
});
const port = 7665;

app.get('/update', function(req,res){
	update = true;
	res.end();
});
app.get('/company.get', function(req,res){
	var mjs = require("mongojs");
	var db = mjs("192.168.0.126/xe", ["View_Ranking"]);
	
	//원래 mongoDB에서 쓰던 문법 + 콜백함수
	db.View_Ranking.find().sort({sr_c_count:-1}, function(e, result){
		res.header("Access-Control-Allow-Origin", "*");
		res.writeHead(200, { 'Content-Type': 'application/json' });
   	 	const obj = {
		result
		};
		res.write(JSON.stringify(obj));
		res.end();		
	});
});
app.get('/company.get.spare', function(req,res){
	var mjs = require("mongojs");
	var db = mjs("192.168.0.126/xe", ["Save_Ranking"]);
	
	//원래 mongoDB에서 쓰던 문법 + 콜백함수
	db.Save_Ranking.find().sort({sr_c_count:-1}, function(e, result){
		res.header("Access-Control-Allow-Origin", "*");
		res.writeHead(200, { 'Content-Type': 'application/json' });
		const obj = {
		result
		};
    		res.write(JSON.stringify(obj));
		res.end();	
	});
});

app.listen(port, function(err) {
  console.log('Connected port' + port);
  if (err) {
    return console.log('Found error', err);
  }
});
// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
