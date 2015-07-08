// NHN Flash UI common - Flash Contents
// v0.9 lastUpdate : 2007. 4. 5
var fc_isIE  = (navigator.appVersion.indexOf("MSIE") != -1) ? true : false;
var fc_isWin = (navigator.appVersion.toLowerCase().indexOf("win") != -1) ? true : false;
var fc_isOpera = (navigator.userAgent.indexOf("Opera") != -1) ? true : false;

function checkFlashPlayerVersion(){
	var _version;
	var _e;
	try {
		var _axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.5");
		_version = _axo.GetVariable("$version");
	} catch (_e) {
		_version = -1;
	}
	return _version;
}

function makeFlashObj(_swfURL_,_flashID_,_width_,_height_,_wmode_,_flashVars_,_bgColor_,_allowFullScreen_,_menu_){
	_wmode_ = (_wmode_ == undefined)? "transparent" : _wmode_;	      // wmode = "window/ opaque/ transparent"
	_bgColor_ = (_bgColor_ == undefined)? "#FFFFFF" : _bgColor_;	    // default "#000000" -> "#FFFFFF" _change 2007. 6. 14
	_allowFullScreen_ = (_allowFullScreen_ == undefined)? true : _allowFullScreen_;	 // allowFullScreen = true / false
	_menu_ = (_menu_ == undefined)? false : _menu_;
	var _object_;
	
	var arr_obj = [];
	arr_obj.push('<object width="'+_width_+'" height="'+_height_+'" id="'+_flashID_+'" classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="https://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,0,0" >');
	arr_obj.push('<param name="allowScriptAccess" value="always" />');
	arr_obj.push('<param name="quality" value="high" />');
	arr_obj.push('<param name="menu" value="'+_menu_+'" />');
	arr_obj.push('<param name="movie" value="'+_swfURL_+'" />');
	arr_obj.push('<param name="wmode" value="'+_wmode_+'" />'); 
	arr_obj.push('<param name="bgcolor" value="'+_bgColor_+'" />');
	arr_obj.push('<param name="FlashVars" value="'+_flashVars_+'">');
	arr_obj.push('<param name="allowFullScreen" value="'+_allowFullScreen_+'">');
	arr_obj.push('<embed src="'+_swfURL_+'" quality="high" wmode="'+_wmode_+'" menu= "'+_menu_ +'" FlashVars="'+_flashVars_+'" bgcolor="'+_bgColor_+'" width="'+_width_+'" height="'+_height_+'" name="'+_flashID_+'" allowFullScreen="'+_allowFullScreen_+'" align="middle" allowScriptAccess="always" type="application/x-shockwave-flash" pluginspage="https://www.macromedia.com/go/getflashplayer"  />');
	arr_obj.push('</object>');
	_object_ =  arr_obj.join("");
	return _object_;
	//document.write(_object_);
}

function showFlashagain(_swfURL_,_flashID_,_width_,_height_,_wmode_,_flashVars_,_bgColor_,_allowFullScreen_,_menu_){
	_wmode_ = (_wmode_ == undefined)? "transparent" : _wmode_;	      // wmode = "window/ opaque/ transparent"
	_bgColor_ = (_bgColor_ == undefined)? "#FFFFFF" : _bgColor_;	    // default "#000000" -> "#FFFFFF" _change 2007. 6. 14
	_allowFullScreen_ = (_allowFullScreen_ == undefined)? true : _allowFullScreen_;	 // allowFullScreen = true / false
	_menu_ = (_menu_ == undefined)? false : _menu_;
	var _object_;
	
	var arr_obj = [];
	arr_obj.push('<object width="'+_width_+'" height="'+_height_+'" id="'+_flashID_+'" classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="https://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,0,0" >');
	arr_obj.push('<param name="allowScriptAccess" value="always" />');
	arr_obj.push('<param name="quality" value="high" />');
	arr_obj.push('<param name="menu" value="'+_menu_+'" />');
	arr_obj.push('<param name="movie" value="'+_swfURL_+'" />');
	arr_obj.push('<param name="wmode" value="'+_wmode_+'" />'); 
	arr_obj.push('<param name="bgcolor" value="'+_bgColor_+'" />');
	arr_obj.push('<param name="FlashVars" value="'+_flashVars_+'">');
	arr_obj.push('<param name="allowFullScreen" value="'+_allowFullScreen_+'">');
	arr_obj.push('<embed src="'+_swfURL_+'" quality="high" wmode="'+_wmode_+'" menu= "'+_menu_ +'" FlashVars="'+_flashVars_+'" bgcolor="'+_bgColor_+'" width="'+_width_+'" height="'+_height_+'" name="'+_flashID_+'" allowFullScreen="'+_allowFullScreen_+'" align="middle" allowScriptAccess="always" type="application/x-shockwave-flash" pluginspage="https://www.macromedia.com/go/getflashplayer"  />');
	arr_obj.push('</object>');
	_object_ =  arr_obj.join("");
	return _object_;
	//document.write(_object_);
}

// 1.1 version support
//showFlash("swfURLh.swf", "flashID", width, height, "transparent", flashVars, bgColor,allowFullScreen);
function showFlash(_swfURL_,_flashID_,_width_,_height_,_wmode_,_flashVars_,_bgColor_,_allowFullScreen_){
	document.write(makeFlashObj(_swfURL_,_flashID_,_width_,_height_,_wmode_,_flashVars_,_bgColor_,_allowFullScreen_));
}
function findFlashObj(_flashID_){
	return fc_isIE ? document.getElementById(_flashID_) : document[_flashID_];
}

// for 'Out of memory line at 56' error    - add 2007. 6. 12
function flashExternalCleanup() {
	try {
	__flash_unloadHandler = function(){
		externalProbSet = true;
		obj = document.getElementsByTagName('OBJECT');
		for (i=0;i<obj.length;i++){
			var theObj = eval(obj[i]);
			theObj.style.display = "none";
		for (var prop in theObj){
			if (typeof(theObj[prop]) == "function"){
				theObj[prop]=null
			}
		}
		}
	}
	if (window.onunload != __flash_unloadHandler){
		__flash_savedUnloadHandler = window.onunload;
		window.onunload = __flash_unloadHandler;
	}
	} catch (e) {}
}
window.onbeforeunload=flashExternalCleanup;

var isshift = false;
var loadFlash = false;

function $() {
	var ret = [];
	for ( var i = 0; i < arguments.length; i++) {
		if (typeof arguments[i] == 'string') {
			ret[ret.length] = document.getElementById(arguments[i]);
		} else {
			ret[ret.length] = arguments[i];
		}
	}
	return ret[1] ? ret : ret[0];
}

function showElement(nm) {
	try {
		$(nm).style.display = 'block';
	} catch (e) {
	}
}
function hideElement(nm) {
	try {
		$(nm).style.display = 'none';
	} catch (e) {
	}
}

function checkRelease() {
	try {
		if ($('enctp').value==1) {
			$('uid').Blur();
			$('upw').Blur();
		}
	} catch (e) {}
}

/* cookie setting */
function getCookie(name) {
	var arg = name + "=";
	var alen = arg.length;
	var clen = document.cookie.length;
	var i = 0;
	while (i < clen) {
		var j = i + alen;
		if (document.cookie.substring(i, j) == arg) {
			var end = document.cookie.indexOf(";", j);
			if (end == -1)
				end = document.cookie.length;
			return unescape(document.cookie.substring(j, end));
		}
		i = document.cookie.indexOf(" ", i) + 1;
		if (i == 0)
			break;
	}
	return null;
}
var userStrokes = false;
/* capslock event */
function capslockevt(e) {
	userStrokes = true;
	var myKeyCode = 0;
	var myShiftKey = false;
	if (window.event) { // IE
		myKeyCode = e.keyCode;
		myShiftKey = e.shiftKey;
	} else if (e.which) { // netscape ff opera
		myKeyCode = e.which; // myShiftKey=( myKeyCode == 16 ) ? true :
								// false;
		myShiftKey = isshift;
	}
	if ((myKeyCode >= 65 && myKeyCode <= 90) && !myShiftKey) {
		showErrorDiv(1);
		setTimeout("hideCapslock()",3000);
	} else if ((myKeyCode >= 97 && myKeyCode <= 122) && myShiftKey) {
		showErrorDiv(1);
		setTimeout("hideCapslock()",3000);
	}
}
function hideCapslock() {
	if (!addshow) {  
		showErrorDiv(-1);
	}
}
function setUserStroke() {
	try {
		parent.window.ac.acHideAct();
	} catch (e) {}
	userStrokes = true;
}
function checkUserStroke() {
	return userStrokes;
}
function checkShiftUp(e) {
	if (e.which && e.which == 16) {
		isshift = false;
	}
}
function checkShiftDown(e) {
	if (e.which && e.which == 16) {
		isshift = true;
	}
}

function delayFocus(objnm) {
	try {
			setTimeout("directFocus('" + objnm + "')", 200)
	} catch (e) {
		try {
			setTimeout("directFocus('" + objnm + "')", 500)
		} catch (e) {
		}
	}
}
function directFocus(objnm) {
	try {
	if ($(objnm)) {
		$(objnm).focus();
	}
	} catch(e) {}
}
function setLevel(login_level) {
	if ($('enctp').value != login_level) {
		useLevel(login_level);
	}
}

function swapSmartIP(e) {
	if ($('smart_ip').className == 'on') {
		try {
			parent.clickcr($('smart_ip'), 'log_off.ipoffset', '', '', e);
		} catch (e) {}
		$('smart_ip').className = 'off';
		$('smart_level').value = -1;
		setSmartLevel(-1);
		$('smart_ip').title = 'IP 보안이 꺼져 있습니다.';
	} else {
		try {
			parent.clickcr($('smart_ip'), 'log_off.iponset', '', '', e);
		} catch (e) {}
		$('smart_ip').className = 'on';
		$('smart_level').value = 1;
		setSmartLevel(1);
		$('smart_ip').title = 'IP 보안이 켜져 있습니다.';
	}
	try {
		$('smart_ip').blur();
	} catch (e) {
	}
}
function setSmartLevel(level) {
	var today = new Date();
	var expire = new Date(today.getTime() + 60 * 60 * 24 * 365 * 1000);
	var curCookie = "nid_slevel=" + escape(level) + "; expires="
			+ expire.toGMTString() + "; path=/; domain=.nid.naver.com;";
	document.cookie = curCookie;
}

/* get key functions */
var getkeyurl = '/login/ext/keys.nhn';
var curtimecheck = 0;
var ajaxavail = -1;
var keystr = null;
var keys = null;
var sessionkey = null;
var keyname = null;
var evalue = null;
var nvalue = null;
var fkeys = null;

function getKeys() {
	enctp = getCookie("nid_enctp") ? getCookie("nid_enctp") : 2;
	if (enctp==2) {
	} else {
		getKeysv2();
	}
}

function getKeysv2() {
	var curtimes = new Date();
	if (curtimecheck == 0) {
		getAjaxResult(getkeyurl);
		curtimecheck = curtimes.getTime();
	} else if (curtimes.getTime() - curtimecheck > 60000) {
		curtimecheck = curtimes.getTime();
		getAjaxResult(getkeyurl);
	} else {
		if ($('enctp').value==2) {
			curtimecheck = curtimes.getTime();
			getAjaxResult(getkeyurl);
		}
	}
}

function getXmlHttp() {
	var xmlhttp;
	try {
		xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
	} catch (e) {
		try {
			xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
		} catch (E) {
			xmlhttp = false;
		}
	}
	if (!xmlhttp && typeof XMLHttpRequest != 'undefined') {
		xmlhttp = new XMLHttpRequest();
	}
	return xmlhttp;
}

function getAjaxResult(urls) {
	try {
		var xmlhttp = getXmlHttp();
		xmlhttp.open("GET", urls);
		xmlhttp.onreadystatechange = function() {
			if (xmlhttp.readyState == 4) {
				keystr = xmlhttp.responseText
				if ($('enctp').value == 2) {
					keySetting(keystr);
				}
			}
		}
		xmlhttp.send(null);
	} catch (e) {
		if (window.bridgeGotTime) {
			throw e;
		} else {
			// page reload?
		}
	}
}
function getLenChar(texts) {
	texts = texts + '';
	return String.fromCharCode(texts.length);
}

function keySplit() {
	if (!keystr) {
	return false;
	}
	keys = keystr.split(",");
	if (!keystr || !keys[0] || !keys[1] || !keys[2] || !keys[3]) {
		//alert('키 발급 실패 ');
		return false;
	}
	sessionkey = keys[0];
	keyname = keys[1];
	evalue = keys[2];
	nvalue = keys[3];
	$('encnm').value = keyname;
	return true;
}
var alreadyfail=false;
function getKeyByRuntimeInclude() {
	try {
		//ajax call fail so get it by js runtime include
		var keyjs  = document.createElement('script');
		keyjs.type = 'text/javascript';
		keyjs.src = '/login/ext/keys_js.nhn';
		document.getElementsByTagName('head')[0].appendChild(keyjs);
	} catch (e) {
		showErrorDiv(4);
	}
}
function confirm_submit() {
	if ($('enctp').value == 1) {
		if ($('uid').value == "") {
			alert('아이디를 입력하세요');
			$('uid').focus();
			return false;
		} else if ($('upw').value == "") {
			alert('비밀번호를 입력하세요');
			$('upw').focus();
			return false;
		}
		var rsa = new RSAKey();
		if (keySplit()) {
			rsa.setPublic(evalue, nvalue);
			$('encpw').value = rsa.encrypt(getLenChar(sessionkey) + sessionkey
					+ getLenChar($('uid').value) + $('uid').value
					+ getLenChar($('upw').value) + $('upw').value);
			$('upw').value = "";
			$('uid').value = "";
		} else {
			//alert('key 발급 실패 ');
			if (alreadyfail) {
				$('enctp').value = getCookie("nid_enctp") ? getCookie("nid_enctp") : 2;
				return true;
			} else {
				//showErrorDiv(4);
				getKeyByRuntimeInclude();
				alreadyfail=true;
			}
			return false;
		}
	} else if ($('enctp').value == 2) {
		return false;
	} else if ($('enctp').value == 3) {
		if (level3_frame.thirdAction()) {
			$('encpw').value = $('level3_frame').contentWindow.document
					.getElementById('encpw').value;
			$('encnm').value = $('level3_frame').contentWindow.document
					.getElementById('encnm').value;
			$('enctp').value = 3;
			$('uid').value = "";
			$('upw').value = "";
			return true;
		} else {
			return false;
		}
	}
	return true;
}
function checkEnt(e) {
	 if (window.event) { // IE
    myKeyCode = e.keyCode;
    myShiftKey = e.shiftKey;
  } else if (e.which) { // netscape ff opera
    myKeyCode = e.which; 
    myShiftKey = isshift;
  }   
  if (myKeyCode == 13) {
	if (navigator.userAgent.indexOf("MSIE") != -1) {
			if (confirm_submit())
			{
				frmNIDLogin.submit();
			}
	}
  }
	
}
function loadComplete() {
	loadFlash = true;
}
// 로그인할 암호화된 아이디와 비밀번호 전달
function login(keyData) {
	fkeys = keyData.split(",");
	if (!fkeys || !fkeys[0] || !fkeys[1] || fkeys[0]=='null' || fkeys[0]=='undefined' || fkeys[1]=='null' || fkeys[1]=='undefined') {
		if (alreadyfail==true) {
			//showErrorDiv(4); 
		} else {
			getKeyByRuntimeInclude();
		}
		alreadyfail=true;
		return false;
	}
	$('encpw').value = fkeys[1];
	$('encnm').value = fkeys[0];
	$('enctp').value = 2;
	$('uid').value = "";
	$('upw').value = "";
	$('frmNIDLogin').submit();
}
function showMsg(arg) {
}
// 플래시의 아이디 필드에 텍스트 입력시 호출
function loginID(arg) {
	try {
		$('uid').value = arg;
	} catch (e) {
	}
}

function capslock() {
	showErrorDiv(1);
	setTimeout("hideCapslock()",3000);
}
// 플래시에서 alt + s 눌렀을 때 이벤트를 넘겨 받는다.
function getAltS(bool) {
	try {
		parent.document.getElementById('query').focus();
	} catch (e) {
	}
}
function getKey() {
	getKeysv2();
}
function inputError(message) {
	if (message == 'idNull') {
		if (navigator.userAgent.indexOf("Firefox") != -1 ) {
		} else {
			alert('아이디를 입력하세요');
		}
		focusID();
	} else if (message == 'pwNull') {
		if (navigator.userAgent.indexOf("Firefox") != -1 ) {
		} else {
			alert('비밀번호를 입력하세요');
		}
		focusID();
	}
}
/* Flash to JS Function END */
var flashretry = 0;
/* JS to Flash Function START */
function keySetting(rsakey) {
	try {
		findSwf("flashlogin").keySetting(rsakey);
		flashretry = 0;
	} catch (e) {
		flashretry++;
		if (flashretry < 5) {
			setTimeout("keySetting('" + rsakey + "')", 100);
		} else {
			if (alreadyfail==true) {
				showErrorDiv(4); 
			} else {
				getKeyByRuntimeInclude();
			}
		}
	}
}
function idset_focus() {
	if (needDelay()) {
		setTimeout("idset_focus_run()", 300);
	} else {
		idset_focus_run();
	}
}

function idset_focus_run() {
	try {
		if ($('enctp').value == 2 && $('login_wrap').className == 'step2') {
			userid = $('uid').value;
			findSwf("flashlogin").idSetting(userid);
			findSwf("flashlogin").focus();
			findSwf("flashlogin").pwSetting("pw");
			findSwf("flashlogin").focusInID();
			loadFlash = true;
			flashretry = 0;
		}
	} catch (e) {
		// alert("code:" + e.number +":" + userid + ",설명:" + e.description)
		flashretry++;
		if (flashretry < 5) {
			setTimeout("idset_focus_run()", 200);
		}
	}
}

function wait(msecs) {
	var start = new Date().getTime();
	var cur = start
	while (cur - start < msecs) {
		cur = new Date().getTime();
	}
}
var pageinit=0;
function idSetting() {
	if (needDelay()) {
		setTimeout("idset()", 400);
	} else {
		idset();
	}
}
function idset() {
	try {
		if ($('enctp').value == 2) {
			if (pageinit>=3) {
				findSwf("flashlogin").focus();
			}
			pageinit++;
			findSwf("flashlogin").idSetting($('uid').value);
			loadFlash = true;
			flashretry = 0;
		}
	} catch (e) {
		//alert(e);
		flashretry++;
		if (flashretry < 5) {
			setTimeout("idset()", 100);
		}
	}
}
function pwSetting() {
	if (needDelay()) {
		setTimeout("pwset()", 300);
	} else {
		pwset();
	}
}
function pwset() {
	try {
		findSwf("flashlogin").pwSetting("pw");
		flashretry = 0;
	} catch (e) {
		// alert(e);
		flashretry++;
		if (flashretry < 5) {
			setTimeout("pwset()", 100);
		}
	}
}
function focusID() {
	if (needDelay()) {
		setTimeout("focus_id()", 500);
	} else {
		focus_id();
	}
}
function focus_id() {
	try {
		window.focus();
		findSwf("flashlogin").focus();
		findSwf("flashlogin").focusInID();
		flashretry = 0;
		setUserStroke();
	} catch (e) {
		// alert(e);
		flashretry++;
		if (flashretry < 5) {
			setTimeout("focus_id()", 100);
		}
	}
}
// 플래시에게 로그인 버튼 클릭 알림
function loginClick() {
	try {
		window.focus();
		findSwf("flashlogin").focus();
		findSwf("flashlogin").loginCheck();
		flashretry = 0;
	} catch (e) {
		flashretry++;
		if (flashretry < 3) {
			setTimeout("loginClick()", 100);
		} else {
			showErrorDiv(4);
		}
	}
}
/* JS to Flash Function END */
// swf movie 찾기
function findSwf(_flashID_) {
	return fc_isIE ? document.getElementById(_flashID_) : document[_flashID_];
}

/* activeX module install */
function onActiveXInst() {
	$('login_wrap').className = 'step3';
	if (navigator.appName.indexOf("Opera") != -1) {
		clear3rdLevel();
	}
	$('level3_frame').src = "/login/ext/waitInst.nhn?20090507";
}
function needDelay() {
	if (navigator.userAgent.indexOf("Firefox") != -1
			|| navigator.userAgent.indexOf("Safari") != -1
			|| navigator.userAgent.indexOf("Opera") != -1) {
		return true;
	} else {
		return false;
	}
}
/* ipcheck level 관련 */
function ipCheckOff() {
	$('smart_ip').className = 'off';
	$('smart_level').value = -1;
	setSmartLevel(-1);
	$('smart_ip').title = 'IP 보안이 꺼져 있습니다.';
}

function ipCheckOn(slevel) {
	$('smart_ip').className = 'on';
	$('smart_level').value = slevel;
	setSmartLevel(slevel);
	$('smart_ip').title = 'IP 보안이 켜져 있습니다.';
}
/* enctpl popup link js function */
function checkSlide(enclevel) {
	useLevel(enclevel);
}

function cookie_init2() {
	sid = getCookie("nid_sid");
	if (sid) {
		$('saveID').value = "1";
		$('uid').value = sid;
		$('uid').className = 'input_text focusnot';
	}	  
	smart_level = getCookie("nid_slevel") ? getCookie("nid_slevel") : 1;
	$('smart_level').value = smart_level;
	if (smart_level > 0) {
		$('smart_ip').className = 'on';
		$('smart_ip').title = 'IP 보안이 켜져 있습니다.';
	} else {
		$('smart_ip').className = 'off';
		$('smart_ip').title = 'IP 보안이 꺼져 있습니다.';
	}
	enctp = getCookie("nid_enctp") ? getCookie("nid_enctp") : 1;
	$('enctp').value = enctp;
	try {
		//idSetting();
		if ( navigator.userAgent.indexOf(";01") != -1 ) {
			$('uid').style.left='14px';
			$('uid').style.top='-47px';
			$('upw').style.left='14px';
			$('upw').style.top='-47px';
		}
		$('upw').value = "";
		if ($('uid').value.length > 0) {
			$('uid').className = 'input_text focusnot';
		}
	} catch (e) {
	}	  
}

function cookie_init() {
	sid = getCookie("nid_sid");
	if (sid) {
		$('saveID').value = "1";
		$('uid').value = sid;
		$('uid').className = 'input_text focusnot';
	}
	smart_level = getCookie("nid_slevel") ? getCookie("nid_slevel") : 1;
	$('smart_level').value = smart_level;
	if (smart_level > 0) {
		$('smart_ip').className = 'on';
		$('smart_ip').title = 'IP 보안이 켜져 있습니다.';
	} else {
		$('smart_ip').className = 'off';
		$('smart_ip').title = 'IP 보안이 꺼져 있습니다.';
	}
	enctp = getCookie("nid_enctp") ? getCookie("nid_enctp") : 2;
	$('enctp').value = enctp;
	try {
		slideinit(enctp);
	} catch (e) {
		setTimeout("slideinit(" + enctp + ")", 500);
	}
	//if (enctp == 2) {
	//      setTimeout("idSetting()", 300);
	//}
}
var onError = false;
/* error level view */
function showErrorDiv(errno) {
	try {
	if (errno == 1) {
		swapLevel = -1;
	}
	/* 3단계는 2단계로 강제 이동 */
	if (errno >= 3 && errno <= 12) {
		$('login_wrap').className = 'step1';
		swapLevel = 1;
		if (errno==4) {
			alreadyfail=true;
		}
		if (navigator.appVersion.indexOf("MSIE 8")) {
			try {
				$('flashlogin').style.visibility = 'hidden';
			} catch (e) {}
		}
	}
	for (i = 1; i <= 14; i++) {
		if (errno == i) {
			showElement("m" + i);
			if (i != 1) {
				delayFocus("m" + i + "b");
				onError = true;
			}
		} else {
			hideElement("m" + i);
		}
	}
	if (errno == -1) {
		onError = false;
		if (navigator.appVersion.indexOf("MSIE 8")) {
			try {
				$('flashlogin').style.visibility = 'visible';
			} catch (e) {}
		}
		if (swapLevel != -1) {
			useLevel(swapLevel);
			swapLevel = -1;
		}
		ErrorDivno = -1;
	}
	} catch (e) {
	}
}
/* level change */
var ErrorDivno = -1;
var swapLevel = 1;
function useLevel(levelno) {
	if (onError==true) {
		return ;
	}
	if (addshow==true) {
		return ;
	}
	if (alreadyfail==true && levelno!=1) {
		showErrorDiv(4);
		return ;
	}
	chglevel = levelFilter(levelno);
	$('login_wrap').className = 'step' + chglevel;
	setLevelImg(chglevel);
	$('enctp').value = chglevel;
	if (chglevel == 3) {
		$('upw').value = "";
		$('level3_frame').src = activex_url;
	} else if (chglevel == 2) {
		$('upw').value = "";
		/* flash loading problem delay 500 ms */
		clear3rdLevel();
		if (navigator.userAgent.indexOf("Opera") != -1 || navigator.userAgent.indexOf("Safari") != -1 || (navigator.userAgent.indexOf("Safari") != -1 && navigator.platform.indexOf("Mac") != -1 )) {
		try {
				$('flasharea').innerHTML = showFlashagain("/login/image/commonLoginF.swf", "flashlogin", 159, 49, "window", "null", "#f7f7f7", "false");
				loadFlash = false;
			} catch(e) {}
		}
		if (!loadFlash) {
			setTimeout("checkFlashLoad(0)", 100);
		} else {
			//if ($('uid').value.length > 0) {
				idSetting();
			//}
			pwSetting();
			//if (navigator.userAgent.indexOf("Firefox") != -1|| navigator.userAgent.indexOf("Safari") != -1) {
			if (navigator.userAgent.indexOf("Firefox") != -1) {
				focusID();
			} else {
				focus_id();
			}
		}
	} else {
		chglevel = 1;
		$('upw').value = "";
		clear3rdLevel();
		if ($('uid').value.length > 0) {
			$('uid').className = 'input_text focusnot';
			delayFocus("upw");
		} else {
			delayFocus("uid");
		}
		if (navigator.userAgent.indexOf("Opera") != -1 || navigator.userAgent.indexOf("Safari") != -1 || (navigator.userAgent.indexOf("Safari") != -1 && navigator.platform.indexOf("Mac") != -1 )) {
			try {
				flashExternalCleanup();
				loadFlash = false;
			} catch (e) {}
		}
	}
	if (chglevel != levelno) {
		if (chglevel == 2) {
			swapLevel = 1;
			$('login_wrap').className = 'step1';
			showErrorDiv(ErrorDivno);
		} else if (ErrorDivno != -1) {
			showErrorDiv(ErrorDivno);
		}
	}
}
function slideinit(levelno) {
	if (navigator.platform.indexOf("Linux") != -1 || navigator.userAgent.indexOf('MSIE 5.5')!=-1 ) {
		levelno = 1;
		$('enctp').value = 1;
	}
	if (navigator.userAgent.indexOf("WIPI") != -1 || navigator.userAgent.indexOf("lgtelecom") != -1 || navigator.userAgent.indexOf("NATE") != -1 || navigator.userAgent.indexOf("POLARIS") != -1) {
		levelno = 1;
		$('enctp').value = 1;
	}
	if ( navigator.userAgent.indexOf(";01") != -1 ) {
		$('uid').style.left='14px';
		$('uid').style.top='-47px';
		$('upw').style.left='14px';
		$('upw').style.top='-47px';
		levelno = 1; 
		$('enctp').value = 1;
	} 
	$('url').value = url;
	if (navigator.userAgent.indexOf("Firefox") != -1 && navigator.platform.indexOf("Linux") != -1) {
		levelno = 1;
		$('enctp').value = 1;
	}
	$('login_wrap').className = 'step' + levelno;
	setLevelImg(levelno);
	if (levelno == 3) {
		$('level3_frame').src = activex_url;
	} else if (levelno == 2) {
		/* flash loading problem delay 500 ms */
		if (!loadFlash) {
			setTimeout("checkFlashinit(0)", 100);
		}
		idSetting();
	} else {
		$('upw').value = "";
		if ($('uid').value.length > 0) {
			$('uid').className = 'input_text focusnot';
		} else {
		}
	}
}
function clear3rdLevel() {
	if ($('level3_frame').src != "/login/ext/blank.html") {
		$('level3_frame').src = "/login/ext/blank.html";
	}
}
function checkFlashLoad(retry) {
	retry++;
	if (loadFlash) {
		ErrorDivno = -1;
		idset_focus();
	} else if (retry > 30) {
		ErrorDivno = 3;
		$('login_wrap').className = 'step1';
		showErrorDiv(3);
	} else {
		setTimeout("checkFlashLoad(" + retry + ")", 30);
	}
}
function checkFlashinit(retry) {
	retry++;
	if (loadFlash) {
		ErrorDivno = -1;
		idSetting();
	} else if (retry > 30) {
		ErrorDivno = 3;
		useLevel(1);
	} else {
		setTimeout("checkFlashinit(" + retry + ")", 30);
	}
}

function levelFilter(levelno) {
	agentStr = navigator.userAgent;
	platform = navigator.platform;
	/* 3rd level only user in IE & not 64bit */
	if (levelno == 3) {
		if (platform == "Win32" 
				&& (navigator.appVersion.indexOf("4.") != -1  || navigator.appVersion.indexOf("5.") != -1)) {
			if ((agentStr.indexOf("MSIE 5") != -1
					|| agentStr.indexOf("MSIE 6") != -1
					|| agentStr.indexOf("MSIE 9") != -1
					|| agentStr.indexOf("MSIE 10") != -1
					|| agentStr.indexOf("MSIE 7") != -1 || agentStr
					.indexOf("MSIE 8") != -1)) {
				if(navigator.cpuClass.toLowerCase() == "x64") {
					ErrorDivno = 8;
					return 1;
				} else {
					return 3;
				}
			} else {
				ErrorDivno = 6;
				return 1;
			}
		} else {
			try {
				cpuclass = navigator.cpuClass.toLowerCase();
			}catch (e){
				cpuclass = '';
			}
			if (cpuclass == "x64") {
				ErrorDivno = 8;
			} else{ 
				ErrorDivno = 6;
			}
			return 1;
		}
	} else if (levelno == 2) {
		if ( navigator.userAgent.indexOf("MSIE 5.5") != -1 ) {
			ErrorDivno = 2;
			return 1;
		}
		if ((navigator.userAgent.indexOf(";01") != -1) ) {
			ErrorDivno = 2;
			return 1;
		}
		if (navigator.userAgent.indexOf("Firefox") != -1 && navigator.platform.indexOf("Linux") != -1) {
			ErrorDivno = 2;
			return 1;
		} else {
			return 2;
		}
	} else {
		return 1;
	}
}
function setLevelImg(lv) {
	if (lv==1) {
		$('slide_btn1').className ='level1 level_on';
		$('slide_btn2').className ='level2';
		$('slide_btn3').className ='level3';
		$('lv1_img').src='https://static.nid.naver.com/images/login/btn_security1_on.gif';
		$('lv2_img').src='https://static.nid.naver.com/images/login/btn_security2_off.gif';
		$('lv3_img').src='https://static.nid.naver.com/images/login/btn_security3_off.gif';
	} else if (lv==2) {
		$('slide_btn1').className ='level1';
		$('slide_btn2').className ='level2 level_on';
		$('slide_btn3').className ='level3';
		$('lv1_img').src='https://static.nid.naver.com/images/login/btn_security1_off.gif';
		$('lv2_img').src='https://static.nid.naver.com/images/login/btn_security2_on.gif';
		$('lv3_img').src='https://static.nid.naver.com/images/login/btn_security3_off.gif';
    } else if (lv==3) {
		$('slide_btn1').className ='level1';
		$('slide_btn2').className ='level2';
		$('slide_btn3').className ='level3 level_on';
		$('lv1_img').src='https://static.nid.naver.com/images/login/btn_security1_off.gif';
		$('lv2_img').src='https://static.nid.naver.com/images/login/btn_security2_off.gif';
		$('lv3_img').src='https://static.nid.naver.com/images/login/btn_security3_on.gif';
    } else {
		$('slide_btn1').className ='level1';
		$('slide_btn2').className ='level2 level_on';
		$('slide_btn3').className ='level3';
		$('lv1_img').src='https://static.nid.naver.com/images/login/btn_security1_off.gif';
		$('lv2_img').src='https://static.nid.naver.com/images/login/btn_security2_on.gif';
		$('lv3_img').src='https://static.nid.naver.com/images/login/btn_security3_off.gif';
	}
}
var addshow=false;
function checkAd(flags) {
	initEnc = $('enctp').value;
	if (navigator.userAgent.indexOf("Firefox") != -1 && navigator.platform.indexOf("Linux") != -1) {
		initEnc = 1;
	}
	if (!onError) {
		if ((flags == '1' || flags == 1)
				&& (initEnc == 1 || initEnc == 2 || initEnc == 3)) {
			addshow=true;
			swapLevel = initEnc;
			if (initEnc == 2) {
				if (navigator.appVersion.indexOf("MSIE")) {
					$('flashlogin').blur(); 
					$('smart_ip').focus();  
				}
				if (navigator.userAgent.indexOf("Opera") != -1 || navigator.userAgent.indexOf("Safari") != -1 || (navigator.userAgent.indexOf("Safari") != -1 && navigator.platform.indexOf("Mac") != -1 )) {
					try {
						flashExternalCleanup();
						loadFlash = false;
					} catch (e) {}
				}
				$('login_wrap').className = 'step1';
			} else if (initEnc == 3) {
				$('login_wrap').className = 'step1';
			}
			$('smart_ip').focus();  
			$('smart_ip').blur();   
			if (navigator.appVersion.indexOf("MSIE 8")) {
				$('flashlogin').style.visibility = 'hidden';
			}
			try {
				if ($('uid').value.length > 0) {
					$('uid').className='input_text focusnot';
				} else {
					$('uid').className='input_text';
				}
			} catch (e) {}
			try {
				if ($('upw').value.length > 0) {
					$('upw').className='input_text focusnot';
				} else {
					$('upw').className='input_text';
				}
			} catch (e) {}
			try {
				//$('upw').disabled=true;
				//$('uid').disabled=true;
			} catch (e) {}
			$('level_img1').src = 'https://static.nid.naver.com/images/login/h_security' + initEnc + '_txt.gif';
		} else {
			addshow=false;
			if (swapLevel == 2) {
				if (navigator.userAgent.indexOf("Opera") != -1 || navigator.userAgent.indexOf("Safari") != -1 || (navigator.userAgent.indexOf("Safari") != -1 && navigator.platform.indexOf("Mac") != -1 )) {
					try {
						$('flasharea').innerHTML = showFlashagain("/login/image/commonLoginF.swf", "flashlogin", 159, 49, "window", "null", "#f7f7f7", "false");
						loadFlash = false;
					} catch (e) {}
				}
				$('login_wrap').className = 'step2';
				if (!loadFlash) {
					setTimeout("checkFlashinit(0)", 100);
				}
				if (navigator.userAgent.indexOf("Firefox") != -1 || navigator.userAgent.indexOf("Opera") != -1 || navigator.userAgent.indexOf("Safari") != -1) {
					idSetting();
				}
			} else if (swapLevel == 3) {
				$('login_wrap').className = 'step3';
			} else if (swapLevel == 1) {
				$('login_wrap').className = 'step1';
			} else {
				$('login_wrap').className = 'step1';
				swapLevel=1;
			}
			setLevelImg(swapLevel);
			if (navigator.appVersion.indexOf("MSIE 8")) {
				$('flashlogin').style.visibility = 'visible';
			}
			$('level_img1').src = 'https://static.nid.naver.com/images/login/h_security1_txt.gif';
			swapLevel = -1;
			hideElement("m1");
			try {
				//$('upw').disabled=false;
				//$('uid').disabled=false;
			} catch (e) {}
		}
	}
}
function checkAd_self() {
	try {
		if (!onError && addshow==true) {
			if ( navigator.userAgent.indexOf("Opera") != -1 || navigator.userAgent.indexOf("Safari") != -1) {
				try{
					//parent.$('query').blur();
					swapLevel = $('enctp').value;
					parent.$('query').blur();
					//checkAd(0);
				} catch (e) {}
			}
		}
	} catch (e) {}
}
/* naver top focus control */
function checkFocus2() {
	if ($('enctp').value == 2) {
		focusID();
	} else if ($('enctp').value == 1) {
		if ($('uid').value.length > 0) {
			$('uid').className = 'input_text focusnot';
			delayFocus("upw");
		} else {
			delayFocus("uid");
		}
	}
}

document.domain = "naver.com";
function setBackGround() {
	var imgUrl = ""; // "img/bg_d372.gif";
	return imgUrl;
}
function setIdTextField() {
	var idX, idY, idWidth, idHeight, idMaxChars, idTextDefault, idTextFont, idTextColor, idTextSize, idBgColor, idChangeBGColor, idBorderSize, idBorderColor, idBorderFocusColor, idActualText;
	idX = "1";
	idY = "0";
if ((navigator.appVersion.indexOf("MSIE 9") != -1))	
	idWidth = "154";
else
	idWidth = "155";
	idHeight = "20";
	idMaxChars = "25";
	idTextDefault = "https://static.nid.naver.com/images/login/bg_login_id_main_6.gif";
	idTextFont = "돋움";
	idBoldTag = ""; // true
	idTextColor = "444444";
	idTextSize = "12";
	idBgColor = "ffffff";
	idChangeBGColor = "ffffff";
	idBorderSize = "1";
	idBorderColor = "bebebe";
	idBorderFocusColor = "5aa409";
	idActualText = "아이디";
	var returnval = idX + "," + idY + "," + idWidth + "," + idHeight + ","
			+ idMaxChars + "," + idTextDefault + "," + idTextFont + ","
			+ idBoldTag + "," + idTextColor + "," + idTextSize + ","
			+ idBgColor + "," + idChangeBGColor + "," + idBorderSize + ","
			+ idBorderColor + "," + idBorderFocusColor + "," + idActualText;
	return returnval;
}
function setPwTextField() {
	var pwX, pwY, pwWidth, pwHeight, pwMaxChars, pwTextDefault, pwTextFont, pwBoldTag, pwTextColor, pwTextSize, pwBgColor, pwChangeBGColor, pwBorderSize, pwBorderColor, pwBorderFocusColor, pwActualText;
	pwX = "1";
	pwY = "25";
if ((navigator.appVersion.indexOf("MSIE 9") != -1))	
	pwWidth = "154";
else
	pwWidth = "155";
	pwHeight = "20";
	pwMaxChars = "16";
	pwTextDefault = "https://static.nid.naver.com/images/login/bg_login_pw_main_6.gif";
	pwTextFont = "돋움";
	pwBoldTag = ""; // true
	pwTextColor = "444444";
	pwTextSize = "12";
	pwBgColor = "ffffff";
	pwChangeBGColor = "ffffff";
	pwBorderSize = "1";
	pwBorderColor = "bebebe";
	pwBorderFocusColor = "5aa409";
	pwActualText = "비밀번호";
	var returnval = pwX + "," + pwY + "," + pwWidth + "," + pwHeight + ","
			+ pwMaxChars + "," + pwTextDefault + "," + pwTextFont + ","
			+ pwBoldTag + "," + pwTextColor + "," + pwTextSize + ","
			+ pwBgColor + "," + pwChangeBGColor + "," + pwBorderSize + ","
			+ pwBorderColor + "," + pwBorderFocusColor + "," + pwActualText;
	return returnval;
}
var loadFlash = false;
// Copyright (c) 2005 Tom Wu
// All Rights Reserved.
// See "LICENSE" for details.

// Basic JavaScript BN library - subset useful for RSA encryption.

// Bits per digit
var dbits;

// JavaScript engine analysis
var canary = 0xdeadbeefcafe;
var j_lm = ((canary & 0xffffff) == 0xefcafe);

// (public) Constructor
function BigInteger(a, b, c) {
	if (a != null)
		if ("number" == typeof a)
			this.fromNumber(a, b, c);
		else if (b == null && "string" != typeof a)
			this.fromString(a, 256);
		else
			this.fromString(a, b);
}

// return new, unset BigInteger
function nbi() {
	return new BigInteger(null);
}

// am: Compute w_j += (x*this_i), propagate carries,
// c is initial carry, returns final carry.
// c < 3*dvalue, x < 2*dvalue, this_i < dvalue
// We need to select the fastest one that works in this environment.

// am1: use a single mult and divide to get the high bits,
// max digit bits should be 26 because
// max internal value = 2*dvalue^2-2*dvalue (< 2^53)
function am1(i, x, w, j, c, n) {
	while (--n >= 0) {
		var v = x * this[i++] + w[j] + c;
		c = Math.floor(v / 0x4000000);
		w[j++] = v & 0x3ffffff;
	}
	return c;
}
// am2 avoids a big mult-and-extract completely.
// Max digit bits should be <= 30 because we do bitwise ops
// on values up to 2*hdvalue^2-hdvalue-1 (< 2^31)
function am2(i, x, w, j, c, n) {
	var xl = x & 0x7fff, xh = x >> 15;
	while (--n >= 0) {
		var l = this[i] & 0x7fff;
		var h = this[i++] >> 15;
		var m = xh * l + h * xl;
		l = xl * l + ((m & 0x7fff) << 15) + w[j] + (c & 0x3fffffff);
		c = (l >>> 30) + (m >>> 15) + xh * h + (c >>> 30);
		w[j++] = l & 0x3fffffff;
	}
	return c;
}
// Alternately, set max digit bits to 28 since some
// browsers slow down when dealing with 32-bit numbers.
function am3(i, x, w, j, c, n) {
	var xl = x & 0x3fff, xh = x >> 14;
	while (--n >= 0) {
		var l = this[i] & 0x3fff;
		var h = this[i++] >> 14;
		var m = xh * l + h * xl;
		l = xl * l + ((m & 0x3fff) << 14) + w[j] + c;
		c = (l >> 28) + (m >> 14) + xh * h;
		w[j++] = l & 0xfffffff;
	}
	return c;
}
if (j_lm && (navigator.appName == "Microsoft Internet Explorer")) {
	BigInteger.prototype.am = am2;
	dbits = 30;
} else if (j_lm && (navigator.appName != "Netscape")) {
	BigInteger.prototype.am = am1;
	dbits = 26;
} else { // Mozilla/Netscape seems to prefer am3
	BigInteger.prototype.am = am3;
	dbits = 28;
}

BigInteger.prototype.DB = dbits;
BigInteger.prototype.DM = ((1 << dbits) - 1);
BigInteger.prototype.DV = (1 << dbits);

var BI_FP = 52;
BigInteger.prototype.FV = Math.pow(2, BI_FP);
BigInteger.prototype.F1 = BI_FP - dbits;
BigInteger.prototype.F2 = 2 * dbits - BI_FP;

// Digit conversions
var BI_RM = "0123456789abcdefghijklmnopqrstuvwxyz";
var BI_RC = new Array();
var rr, vv;
rr = "0".charCodeAt(0);
for (vv = 0; vv <= 9; ++vv)
	BI_RC[rr++] = vv;
rr = "a".charCodeAt(0);
for (vv = 10; vv < 36; ++vv)
	BI_RC[rr++] = vv;
rr = "A".charCodeAt(0);
for (vv = 10; vv < 36; ++vv)
	BI_RC[rr++] = vv;

function int2char(n) {
	return BI_RM.charAt(n);
}
function intAt(s, i) {
	var c = BI_RC[s.charCodeAt(i)];
	return (c == null) ? -1 : c;
}

// (protected) copy this to r
function bnpCopyTo(r) {
	for ( var i = this.t - 1; i >= 0; --i)
		r[i] = this[i];
	r.t = this.t;
	r.s = this.s;
}

// (protected) set from integer value x, -DV <= x < DV
function bnpFromInt(x) {
	this.t = 1;
	this.s = (x < 0) ? -1 : 0;
	if (x > 0)
		this[0] = x;
	else if (x < -1)
		this[0] = x + DV;
	else
		this.t = 0;
}

// return bigint initialized to value
function nbv(i) {
	var r = nbi();
	r.fromInt(i);
	return r;
}

// (protected) set from string and radix
function bnpFromString(s, b) {
	var k;
	if (b == 16)
		k = 4;
	else if (b == 8)
		k = 3;
	else if (b == 256)
		k = 8; // byte array
	else if (b == 2)
		k = 1;
	else if (b == 32)
		k = 5;
	else if (b == 4)
		k = 2;
	else {
		this.fromRadix(s, b);
		return;
	}
	this.t = 0;
	this.s = 0;
	var i = s.length, mi = false, sh = 0;
	while (--i >= 0) {
		var x = (k == 8) ? s[i] & 0xff : intAt(s, i);
		if (x < 0) {
			if (s.charAt(i) == "-")
				mi = true;
			continue;
		}
		mi = false;
		if (sh == 0)
			this[this.t++] = x;
		else if (sh + k > this.DB) {
			this[this.t - 1] |= (x & ((1 << (this.DB - sh)) - 1)) << sh;
			this[this.t++] = (x >> (this.DB - sh));
		} else
			this[this.t - 1] |= x << sh;
		sh += k;
		if (sh >= this.DB)
			sh -= this.DB;
	}
	if (k == 8 && (s[0] & 0x80) != 0) {
		this.s = -1;
		if (sh > 0)
			this[this.t - 1] |= ((1 << (this.DB - sh)) - 1) << sh;
	}
	this.clamp();
	if (mi)
		BigInteger.ZERO.subTo(this, this);
}

// (protected) clamp off excess high words
function bnpClamp() {
	var c = this.s & this.DM;
	while (this.t > 0 && this[this.t - 1] == c)
		--this.t;
}

// (public) return string representation in given radix
function bnToString(b) {
	if (this.s < 0)
		return "-" + this.negate().toString(b);
	var k;
	if (b == 16)
		k = 4;
	else if (b == 8)
		k = 3;
	else if (b == 2)
		k = 1;
	else if (b == 32)
		k = 5;
	else if (b == 4)
		k = 2;
	else
		return this.toRadix(b);
	var km = (1 << k) - 1, d, m = false, r = "", i = this.t;
	var p = this.DB - (i * this.DB) % k;
	if (i-- > 0) {
		if (p < this.DB && (d = this[i] >> p) > 0) {
			m = true;
			r = int2char(d);
		}
		while (i >= 0) {
			if (p < k) {
				d = (this[i] & ((1 << p) - 1)) << (k - p);
				d |= this[--i] >> (p += this.DB - k);
			} else {
				d = (this[i] >> (p -= k)) & km;
				if (p <= 0) {
					p += this.DB;
					--i;
				}
			}
			if (d > 0)
				m = true;
			if (m)
				r += int2char(d);
		}
	}
	return m ? r : "0";
}

// (public) -this
function bnNegate() {
	var r = nbi();
	BigInteger.ZERO.subTo(this, r);
	return r;
}

// (public) |this|
function bnAbs() {
	return (this.s < 0) ? this.negate() : this;
}

// (public) return + if this > a, - if this < a, 0 if equal
function bnCompareTo(a) {
	var r = this.s - a.s;
	if (r != 0)
		return r;
	var i = this.t;
	r = i - a.t;
	if (r != 0)
		return r;
	while (--i >= 0)
		if ((r = this[i] - a[i]) != 0)
			return r;
	return 0;
}

// returns bit length of the integer x
function nbits(x) {
	var r = 1, t;
	if ((t = x >>> 16) != 0) {
		x = t;
		r += 16;
	}
	if ((t = x >> 8) != 0) {
		x = t;
		r += 8;
	}
	if ((t = x >> 4) != 0) {
		x = t;
		r += 4;
	}
	if ((t = x >> 2) != 0) {
		x = t;
		r += 2;
	}
	if ((t = x >> 1) != 0) {
		x = t;
		r += 1;
	}
	return r;
}

// (public) return the number of bits in "this"
function bnBitLength() {
	if (this.t <= 0)
		return 0;
	return this.DB * (this.t - 1)
			+ nbits(this[this.t - 1] ^ (this.s & this.DM));
}

// (protected) r = this << n*DB
function bnpDLShiftTo(n, r) {
	var i;
	for (i = this.t - 1; i >= 0; --i)
		r[i + n] = this[i];
	for (i = n - 1; i >= 0; --i)
		r[i] = 0;
	r.t = this.t + n;
	r.s = this.s;
}

// (protected) r = this >> n*DB
function bnpDRShiftTo(n, r) {
	for ( var i = n; i < this.t; ++i)
		r[i - n] = this[i];
	r.t = Math.max(this.t - n, 0);
	r.s = this.s;
}

// (protected) r = this << n
function bnpLShiftTo(n, r) {
	var bs = n % this.DB;
	var cbs = this.DB - bs;
	var bm = (1 << cbs) - 1;
	var ds = Math.floor(n / this.DB), c = (this.s << bs) & this.DM, i;
	for (i = this.t - 1; i >= 0; --i) {
		r[i + ds + 1] = (this[i] >> cbs) | c;
		c = (this[i] & bm) << bs;
	}
	for (i = ds - 1; i >= 0; --i)
		r[i] = 0;
	r[ds] = c;
	r.t = this.t + ds + 1;
	r.s = this.s;
	r.clamp();
}

// (protected) r = this >> n
function bnpRShiftTo(n, r) {
	r.s = this.s;
	var ds = Math.floor(n / this.DB);
	if (ds >= this.t) {
		r.t = 0;
		return;
	}
	var bs = n % this.DB;
	var cbs = this.DB - bs;
	var bm = (1 << bs) - 1;
	r[0] = this[ds] >> bs;
	for ( var i = ds + 1; i < this.t; ++i) {
		r[i - ds - 1] |= (this[i] & bm) << cbs;
		r[i - ds] = this[i] >> bs;
	}
	if (bs > 0)
		r[this.t - ds - 1] |= (this.s & bm) << cbs;
	r.t = this.t - ds;
	r.clamp();
}

// (protected) r = this - a
function bnpSubTo(a, r) {
	var i = 0, c = 0, m = Math.min(a.t, this.t);
	while (i < m) {
		c += this[i] - a[i];
		r[i++] = c & this.DM;
		c >>= this.DB;
	}
	if (a.t < this.t) {
		c -= a.s;
		while (i < this.t) {
			c += this[i];
			r[i++] = c & this.DM;
			c >>= this.DB;
		}
		c += this.s;
	} else {
		c += this.s;
		while (i < a.t) {
			c -= a[i];
			r[i++] = c & this.DM;
			c >>= this.DB;
		}
		c -= a.s;
	}
	r.s = (c < 0) ? -1 : 0;
	if (c < -1)
		r[i++] = this.DV + c;
	else if (c > 0)
		r[i++] = c;
	r.t = i;
	r.clamp();
}

// (protected) r = this * a, r != this,a (HAC 14.12)
// "this" should be the larger one if appropriate.
function bnpMultiplyTo(a, r) {
	var x = this.abs(), y = a.abs();
	var i = x.t;
	r.t = i + y.t;
	while (--i >= 0)
		r[i] = 0;
	for (i = 0; i < y.t; ++i)
		r[i + x.t] = x.am(0, y[i], r, i, 0, x.t);
	r.s = 0;
	r.clamp();
	if (this.s != a.s)
		BigInteger.ZERO.subTo(r, r);
}

// (protected) r = this^2, r != this (HAC 14.16)
function bnpSquareTo(r) {
	var x = this.abs();
	var i = r.t = 2 * x.t;
	while (--i >= 0)
		r[i] = 0;
	for (i = 0; i < x.t - 1; ++i) {
		var c = x.am(i, x[i], r, 2 * i, 0, 1);
		if ((r[i + x.t] += x.am(i + 1, 2 * x[i], r, 2 * i + 1, c, x.t - i - 1)) >= x.DV) {
			r[i + x.t] -= x.DV;
			r[i + x.t + 1] = 1;
		}
	}
	if (r.t > 0)
		r[r.t - 1] += x.am(i, x[i], r, 2 * i, 0, 1);
	r.s = 0;
	r.clamp();
}

// (protected) divide this by m, quotient and remainder to q, r (HAC 14.20)
// r != q, this != m. q or r may be null.
function bnpDivRemTo(m, q, r) {
	var pm = m.abs();
	if (pm.t <= 0)
		return;
	var pt = this.abs();
	if (pt.t < pm.t) {
		if (q != null)
			q.fromInt(0);
		if (r != null)
			this.copyTo(r);
		return;
	}
	if (r == null)
		r = nbi();
	var y = nbi(), ts = this.s, ms = m.s;
	var nsh = this.DB - nbits(pm[pm.t - 1]); // normalize modulus
	if (nsh > 0) {
		pm.lShiftTo(nsh, y);
		pt.lShiftTo(nsh, r);
	} else {
		pm.copyTo(y);
		pt.copyTo(r);
	}
	var ys = y.t;
	var y0 = y[ys - 1];
	if (y0 == 0)
		return;
	var yt = y0 * (1 << this.F1) + ((ys > 1) ? y[ys - 2] >> this.F2 : 0);
	var d1 = this.FV / yt, d2 = (1 << this.F1) / yt, e = 1 << this.F2;
	var i = r.t, j = i - ys, t = (q == null) ? nbi() : q;
	y.dlShiftTo(j, t);
	if (r.compareTo(t) >= 0) {
		r[r.t++] = 1;
		r.subTo(t, r);
	}
	BigInteger.ONE.dlShiftTo(ys, t);
	t.subTo(y, y); // "negative" y so we can replace sub with am later
	while (y.t < ys)
		y[y.t++] = 0;
	while (--j >= 0) {
		// Estimate quotient digit
		var qd = (r[--i] == y0) ? this.DM : Math.floor(r[i] * d1
				+ (r[i - 1] + e) * d2);
		if ((r[i] += y.am(0, qd, r, j, 0, ys)) < qd) { // Try it out
			y.dlShiftTo(j, t);
			r.subTo(t, r);
			while (r[i] < --qd)
				r.subTo(t, r);
		}
	}
	if (q != null) {
		r.drShiftTo(ys, q);
		if (ts != ms)
			BigInteger.ZERO.subTo(q, q);
	}
	r.t = ys;
	r.clamp();
	if (nsh > 0)
		r.rShiftTo(nsh, r); // Denormalize remainder
	if (ts < 0)
		BigInteger.ZERO.subTo(r, r);
}

// (public) this mod a
function bnMod(a) {
	var r = nbi();
	this.abs().divRemTo(a, null, r);
	if (this.s < 0 && r.compareTo(BigInteger.ZERO) > 0)
		a.subTo(r, r);
	return r;
}

// Modular reduction using "classic" algorithm
function Classic(m) {
	this.m = m;
}
function cConvert(x) {
	if (x.s < 0 || x.compareTo(this.m) >= 0)
		return x.mod(this.m);
	else
		return x;
}
function cRevert(x) {
	return x;
}
function cReduce(x) {
	x.divRemTo(this.m, null, x);
}
function cMulTo(x, y, r) {
	x.multiplyTo(y, r);
	this.reduce(r);
}
function cSqrTo(x, r) {
	x.squareTo(r);
	this.reduce(r);
}

Classic.prototype.convert = cConvert;
Classic.prototype.revert = cRevert;
Classic.prototype.reduce = cReduce;
Classic.prototype.mulTo = cMulTo;
Classic.prototype.sqrTo = cSqrTo;

// (protected) return "-1/this % 2^DB"; useful for Mont. reduction
// justification:
// xy == 1 (mod m)
// xy = 1+km
// xy(2-xy) = (1+km)(1-km)
// x[y(2-xy)] = 1-k^2m^2
// x[y(2-xy)] == 1 (mod m^2)
// if y is 1/x mod m, then y(2-xy) is 1/x mod m^2
// should reduce x and y(2-xy) by m^2 at each step to keep size bounded.
// JS multiply "overflows" differently from C/C++, so care is needed here.
function bnpInvDigit() {
	if (this.t < 1)
		return 0;
	var x = this[0];
	if ((x & 1) == 0)
		return 0;
	var y = x & 3; // y == 1/x mod 2^2
	y = (y * (2 - (x & 0xf) * y)) & 0xf; // y == 1/x mod 2^4
	y = (y * (2 - (x & 0xff) * y)) & 0xff; // y == 1/x mod 2^8
	y = (y * (2 - (((x & 0xffff) * y) & 0xffff))) & 0xffff; // y == 1/x mod 2^16
	// last step - calculate inverse mod DV directly;
	// assumes 16 < DB <= 32 and assumes ability to handle 48-bit ints
	y = (y * (2 - x * y % this.DV)) % this.DV; // y == 1/x mod 2^dbits
	// we really want the negative inverse, and -DV < y < DV
	return (y > 0) ? this.DV - y : -y;
}

// Montgomery reduction
function Montgomery(m) {
	this.m = m;
	this.mp = m.invDigit();
	this.mpl = this.mp & 0x7fff;
	this.mph = this.mp >> 15;
	this.um = (1 << (m.DB - 15)) - 1;
	this.mt2 = 2 * m.t;
}

// xR mod m
function montConvert(x) {
	var r = nbi();
	x.abs().dlShiftTo(this.m.t, r);
	r.divRemTo(this.m, null, r);
	if (x.s < 0 && r.compareTo(BigInteger.ZERO) > 0)
		this.m.subTo(r, r);
	return r;
}

// x/R mod m
function montRevert(x) {
	var r = nbi();
	x.copyTo(r);
	this.reduce(r);
	return r;
}

// x = x/R mod m (HAC 14.32)
function montReduce(x) {
	while (x.t <= this.mt2)
		// pad x so am has enough room later
		x[x.t++] = 0;
	for ( var i = 0; i < this.m.t; ++i) {
		// faster way of calculating u0 = x[i]*mp mod DV
		var j = x[i] & 0x7fff;
		var u0 = (j * this.mpl + (((j * this.mph + (x[i] >> 15) * this.mpl) & this.um) << 15))
				& x.DM;
		// use am to combine the multiply-shift-add into one call
		j = i + this.m.t;
		x[j] += this.m.am(0, u0, x, i, 0, this.m.t);
		// propagate carry
		while (x[j] >= x.DV) {
			x[j] -= x.DV;
			x[++j]++;
		}
	}
	x.clamp();
	x.drShiftTo(this.m.t, x);
	if (x.compareTo(this.m) >= 0)
		x.subTo(this.m, x);
}

// r = "x^2/R mod m"; x != r
function montSqrTo(x, r) {
	x.squareTo(r);
	this.reduce(r);
}

// r = "xy/R mod m"; x,y != r
function montMulTo(x, y, r) {
	x.multiplyTo(y, r);
	this.reduce(r);
}

Montgomery.prototype.convert = montConvert;
Montgomery.prototype.revert = montRevert;
Montgomery.prototype.reduce = montReduce;
Montgomery.prototype.mulTo = montMulTo;
Montgomery.prototype.sqrTo = montSqrTo;

// (protected) true iff this is even
function bnpIsEven() {
	return ((this.t > 0) ? (this[0] & 1) : this.s) == 0;
}

// (protected) this^e, e < 2^32, doing sqr and mul with "r" (HAC 14.79)
function bnpExp(e, z) {
	if (e > 0xffffffff || e < 1)
		return BigInteger.ONE;
	var r = nbi(), r2 = nbi(), g = z.convert(this), i = nbits(e) - 1;
	g.copyTo(r);
	while (--i >= 0) {
		z.sqrTo(r, r2);
		if ((e & (1 << i)) > 0)
			z.mulTo(r2, g, r);
		else {
			var t = r;
			r = r2;
			r2 = t;
		}
	}
	return z.revert(r);
}

// (public) this^e % m, 0 <= e < 2^32
function bnModPowInt(e, m) {
	var z;
	if (e < 256 || m.isEven())
		z = new Classic(m);
	else
		z = new Montgomery(m);
	return this.exp(e, z);
}

// protected
BigInteger.prototype.copyTo = bnpCopyTo;
BigInteger.prototype.fromInt = bnpFromInt;
BigInteger.prototype.fromString = bnpFromString;
BigInteger.prototype.clamp = bnpClamp;
BigInteger.prototype.dlShiftTo = bnpDLShiftTo;
BigInteger.prototype.drShiftTo = bnpDRShiftTo;
BigInteger.prototype.lShiftTo = bnpLShiftTo;
BigInteger.prototype.rShiftTo = bnpRShiftTo;
BigInteger.prototype.subTo = bnpSubTo;
BigInteger.prototype.multiplyTo = bnpMultiplyTo;
BigInteger.prototype.squareTo = bnpSquareTo;
BigInteger.prototype.divRemTo = bnpDivRemTo;
BigInteger.prototype.invDigit = bnpInvDigit;
BigInteger.prototype.isEven = bnpIsEven;
BigInteger.prototype.exp = bnpExp;

// public
BigInteger.prototype.toString = bnToString;
BigInteger.prototype.negate = bnNegate;
BigInteger.prototype.abs = bnAbs;
BigInteger.prototype.compareTo = bnCompareTo;
BigInteger.prototype.bitLength = bnBitLength;
BigInteger.prototype.mod = bnMod;
BigInteger.prototype.modPowInt = bnModPowInt;

// "constants"
BigInteger.ZERO = nbv(0);
BigInteger.ONE = nbv(1);
// prng4.js - uses Arcfour as a PRNG

function Arcfour() {
	this.i = 0;
	this.j = 0;
	this.S = new Array();
}

// Initialize arcfour context from key, an array of ints, each from [0..255]
function ARC4init(key) {
	var i, j, t;
	for (i = 0; i < 256; ++i)
		this.S[i] = i;
	j = 0;
	for (i = 0; i < 256; ++i) {
		j = (j + this.S[i] + key[i % key.length]) & 255;
		t = this.S[i];
		this.S[i] = this.S[j];
		this.S[j] = t;
	}
	this.i = 0;
	this.j = 0;
}

function ARC4next() {
	var t;
	this.i = (this.i + 1) & 255;
	this.j = (this.j + this.S[this.i]) & 255;
	t = this.S[this.i];
	this.S[this.i] = this.S[this.j];
	this.S[this.j] = t;
	return this.S[(t + this.S[this.i]) & 255];
}

Arcfour.prototype.init = ARC4init;
Arcfour.prototype.next = ARC4next;

// Plug in your RNG constructor here
function prng_newstate() {
	return new Arcfour();
}

// Pool size must be a multiple of 4 and greater than 32.
// An array of bytes the size of the pool will be passed to init()
var rng_psize = 256;
// Random number generator - requires a PRNG backend, e.g. prng4.js

// For best results, put code like
// <body onClick='rng_seed_time();' onKeyPress='rng_seed_time();'>
// in your main HTML document.

var rng_state;
var rng_pool;
var rng_pptr;

// Mix in a 32-bit integer into the pool
function rng_seed_int(x) {
	rng_pool[rng_pptr++] ^= x & 255;
	rng_pool[rng_pptr++] ^= (x >> 8) & 255;
	rng_pool[rng_pptr++] ^= (x >> 16) & 255;
	rng_pool[rng_pptr++] ^= (x >> 24) & 255;
	if (rng_pptr >= rng_psize)
		rng_pptr -= rng_psize;
}

// Mix in the current time (w/milliseconds) into the pool
function rng_seed_time() {
	rng_seed_int(new Date().getTime());
}

// Initialize the pool with junk if needed.
if (rng_pool == null) {
	rng_pool = new Array();
	rng_pptr = 0;
	var t;
	if (navigator.appName == "Netscape" && navigator.appVersion < "5"
			&& window.crypto) {
		// Extract entropy (256 bits) from NS4 RNG if available
		var z = window.crypto.random(32);
		for (t = 0; t < z.length; ++t)
			rng_pool[rng_pptr++] = z.charCodeAt(t) & 255;
	}
	while (rng_pptr < rng_psize) { // extract some randomness from
									// Math.random()
		t = Math.floor(65536 * Math.random());
		rng_pool[rng_pptr++] = t >>> 8;
		rng_pool[rng_pptr++] = t & 255;
	}
	rng_pptr = 0;
	rng_seed_time();
	// rng_seed_int(window.screenX);
	// rng_seed_int(window.screenY);
}

function rng_get_byte() {
	if (rng_state == null) {
		rng_seed_time();
		rng_state = prng_newstate();
		rng_state.init(rng_pool);
		for (rng_pptr = 0; rng_pptr < rng_pool.length; ++rng_pptr)
			rng_pool[rng_pptr] = 0;
		rng_pptr = 0;
		// rng_pool = null;
	}
	// TODO: allow reseeding after first request
	return rng_state.next();
}

function rng_get_bytes(ba) {
	var i;
	for (i = 0; i < ba.length; ++i)
		ba[i] = rng_get_byte();
}

function SecureRandom() {
}

SecureRandom.prototype.nextBytes = rng_get_bytes;
// Depends on jsbn.js and rng.js

// convert a (hex) string to a bignum object
function parseBigInt(str, r) {
	return new BigInteger(str, r);
}

function linebrk(s, n) {
	var ret = "";
	var i = 0;
	while (i + n < s.length) {
		ret += s.substring(i, i + n) + "\n";
		i += n;
	}
	return ret + s.substring(i, s.length);
}

function byte2Hex(b) {
	if (b < 0x10)
		return "0" + b.toString(16);
	else
		return b.toString(16);
}

// PKCS#1 (type 2, random) pad input string s to n bytes, and return a bigint
function pkcs1pad2(s, n) {
	if (n < s.length + 11) {
		alert("암호화가 정상적으로 이루어지지 않았습니다.");
		return null;
	}
	var ba = new Array();
	var i = s.length - 1;
	while (i >= 0 && n > 0)
		ba[--n] = s.charCodeAt(i--);
	ba[--n] = 0;
	var rng = new SecureRandom();
	var x = new Array();
	while (n > 2) { // random non-zero pad
		x[0] = 0;
		while (x[0] == 0)
			rng.nextBytes(x);
		ba[--n] = x[0];
	}
	ba[--n] = 2;
	ba[--n] = 0;
	return new BigInteger(ba);
}

// "empty" RSA key constructor
function RSAKey() {
	this.n = null;
	this.e = 0;
	this.d = null;
	this.p = null;
	this.q = null;
	this.dmp1 = null;
	this.dmq1 = null;
	this.coeff = null;
}

// Set the public key fields N and e from hex strings
function RSASetPublic(N, E) {
	if (N != null && E != null && N.length > 0 && E.length > 0) {
		this.n = parseBigInt(N, 16);
		this.e = parseInt(E, 16);
	} else
		alert("잘못된 보안키입니다.");
}

// Perform raw public operation on "x": return x^e (mod n)
function RSADoPublic(x) {
	return x.modPowInt(this.e, this.n);
}

// Return the PKCS#1 RSA encryption of "text" as an even-length hex string
function RSAEncrypt(text) {
	var m = pkcs1pad2(text, (this.n.bitLength() + 7) >> 3);
	if (m == null)
		return null;
	var c = this.doPublic(m);
	if (c == null)
		return null;
	var h = c.toString(16);
	var gap = (((this.n.bitLength() + 7) >> 3) << 1) - h.length;
	while (gap-- > 0)
		h = "0" + h;
	// if((h.length & 1) == 0) return h; else return "0" + h;
	return h;
}

// Return the PKCS#1 RSA encryption of "text" as a Base64-encoded string
// function RSAEncryptB64(text) {
// var h = this.encrypt(text);
// if(h) return hex2b64(h); else return null;
// }

// protected
RSAKey.prototype.doPublic = RSADoPublic;

// public
RSAKey.prototype.setPublic = RSASetPublic;
RSAKey.prototype.encrypt = RSAEncrypt;
// RSAKey.prototype.encrypt_b64 = RSAEncryptB64;
var b64map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
var b64pad = "=";

function hex2b64(h) {
	var i;
	var c;
	var ret = "";
	for (i = 0; i + 3 <= h.length; i += 3) {
		c = parseInt(h.substring(i, i + 3), 16);
		ret += b64map.charAt(c >> 6) + b64map.charAt(c & 63);
	}
	if (i + 1 == h.length) {
		c = parseInt(h.substring(i, i + 1), 16);
		ret += b64map.charAt(c << 2);
	} else if (i + 2 == h.length) {
		c = parseInt(h.substring(i, i + 2), 16);
		ret += b64map.charAt(c >> 2) + b64map.charAt((c & 3) << 4);
	}
	while ((ret.length & 3) > 0)
		ret += b64pad;
	return ret;
}

// convert a base64 string to hex
function b64tohex(s) {
	var ret = ""
	var i;
	var k = 0; // b64 state, 0-3
	var slop;
	for (i = 0; i < s.length; ++i) {
		if (s.charAt(i) == b64pad)
			break;
		v = b64map.indexOf(s.charAt(i));
		if (v < 0)
			continue;
		if (k == 0) {
			ret += int2char(v >> 2);
			slop = v & 3;
			k = 1;
		} else if (k == 1) {
			ret += int2char((slop << 2) | (v >> 4));
			slop = v & 0xf;
			k = 2;
		} else if (k == 2) {
			ret += int2char(slop);
			ret += int2char(v >> 2);
			slop = v & 3;
			k = 3;
		} else {
			ret += int2char((slop << 2) | (v >> 4));
			ret += int2char(v & 0xf);
			k = 0;
		}
	}
	if (k == 1)
		ret += int2char(slop << 2);
	return ret;
}

// convert a base64 string to a byte/number array
function b64toBA(s) {
	// piggyback on b64tohex for now, optimize later
	var h = b64tohex(s);
	var i;
	var a = new Array();
	for (i = 0; 2 * i < h.length; ++i) {
		a[i] = parseInt(h.substring(2 * i, 2 * i + 2), 16);
	}
	return a;
}

function savedLong(a) {
	if (a.checked == true) {
		$("chk_long").checked = true;
		$("chk_long2").checked = true;
		$("chk_long3").checked = true;
		ipCheckOff();
		$("nvlong").value = "1";
		showElement("m14");
	} else {
		$("chk_long").checked = false;
		$("chk_long2").checked = false;
		$("chk_long3").checked = false;
		$("nvlong").value = "0";
	}
}
function savedLongHide(b)
{
	if (b==1)   {
		hideElement("m14");
		$("chk_long").checked = false;
		$("chk_long2").checked = false;
		$("chk_long3").checked = false;
		$("nvlong").value = "0";
	}   else {
		hideElement("m14");
	}
}
