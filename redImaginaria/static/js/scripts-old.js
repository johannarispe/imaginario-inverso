$(function() {
var submit_form = function(e) {
	//$.getJSON($SCRIPT_ROOT + '/_conversar', {
	$.post('http://inverso.local:5000/_conversar', {
		mensaje: $('#mensaje').val()
	}, function(data) {
		$('input[name=mensaje]').focus().select();
		$('#mensajes ul').append(
			$('<li>').append(		
			$('<p>').append(
			$('<span>').attr('class', 'mensajeTX').append(data.time+" : "+data.mensaje)
		)));
		$('#mensaje').val('');
	 });
	 return false;
};
	$('#enviar').bind('click', submit_form);
	$('input[type=text]').bind('keydown', function(e) {
		if (e.keyCode == 13) {
			submit_form(e);
		}
		});
	$('input[name=mensaje]').focus();
});
	var horaDeInicioSession = new Date();
	var lista = [];
	$.updater({
		//url: $SCRIPT_ROOT + '/_mensajes',
		url: 'http://inverso.local:5000/_mensajes',
		method: 'get',
		dataType: 'json',	
		interval: 1500
	},
	function(data, response){
		$('#mensajes ul').html("");
		mensajes = data.result.mensajes;
		if ( mensajes.length >= 1 ) {
			$.each(mensajes, function(index, data) {
				msg = JSON.parse(data.replace(/'/g, "\""));
				var horaDelMensaje = new Date(msg.time);
				//'2014-12-05 10:40
				if (esHoy(horaDelMensaje,horaDeInicioSession)){
				if (lista.indexOf(index) == -1){
				lista[index] =msg.mensaje;
				console.log(lista[index]);
				var msgChat = horaDelMensaje.getUTCDate() + ":" + horaDelMensaje.getMonth() + " :: " +  msg.mensaje;
				$('#mensajes ul').append(
				$('<li>').append(
				$('<p>').append(
				$('<span>').attr('class', 'mensajeRX').append(msgChat)
			)));
				}
				}

			});
		}
	});
function esHoy( d1, d2 ){	
	if(d1.getUTCFullYear() == d2.getUTCFullYear() &&
	d1.getUTCMonth() == d2.getUTCMonth() &&
	d1.getUTCDate() == d2.getUTCDate()) {
		if(d1.getUTCHours() ==  d2.getUTCHours()){
			console.log("d1:" + d1.getUTCMinutes() + "d2:" +d2.getUTCMinutes()); 
			return true;
			//return d1.getUTCMinutes() >= d2.getUTCMinutes();
	}
}
}

function utf8_encode(argString) {
  if (argString === null || typeof argString === 'undefined') {
    return '';
  }

  // .replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  var string = (argString + '');
  var utftext = '',
    start, end, stringl = 0;

  start = end = 0;
  stringl = string.length;
  for (var n = 0; n < stringl; n++) {
    var c1 = string.charCodeAt(n);
    var enc = null;

    if (c1 < 128) {
      end++;
    } else if (c1 > 127 && c1 < 2048) {
      enc = String.fromCharCode(
        (c1 >> 6) | 192, (c1 & 63) | 128
      );
    } else if ((c1 & 0xF800) != 0xD800) {
      enc = String.fromCharCode(
        (c1 >> 12) | 224, ((c1 >> 6) & 63) | 128, (c1 & 63) | 128
      );
    } else {
      // surrogate pairs
      if ((c1 & 0xFC00) != 0xD800) {
        throw new RangeError('Unmatched trail surrogate at ' + n);
      }
      var c2 = string.charCodeAt(++n);
      if ((c2 & 0xFC00) != 0xDC00) {
        throw new RangeError('Unmatched lead surrogate at ' + (n - 1));
      }
      c1 = ((c1 & 0x3FF) << 10) + (c2 & 0x3FF) + 0x10000;
      enc = String.fromCharCode(
        (c1 >> 18) | 240, ((c1 >> 12) & 63) | 128, ((c1 >> 6) & 63) | 128, (c1 & 63) | 128
      );
    }
    if (enc !== null) {
      if (end > start) {
        utftext += string.slice(start, end);
      }
      utftext += enc;
      start = end = n + 1;
    }
  }

  if (end > start) {
    utftext += string.slice(start, stringl);
  }

  return utftext;
}

function utf8_decode(str_data) {

  var tmp_arr = [],
    i = 0,
    c1 = 0,
    seqlen = 0;

  str_data += '';

  while (i < str_data.length) {
    c1 = str_data.charCodeAt(i) & 0xFF;
    seqlen = 0;

    // http://en.wikipedia.org/wiki/UTF-8#Codepage_layout
    if (c1 <= 0xBF) {
      c1 = (c1 & 0x7F);
      seqlen = 1;
    } else if (c1 <= 0xDF) {
      c1 = (c1 & 0x1F);
      seqlen = 2;
    } else if (c1 <= 0xEF) {
      c1 = (c1 & 0x0F);
      seqlen = 3;
    } else {
      c1 = (c1 & 0x07);
      seqlen = 4;
    }

    for (var ai = 1; ai < seqlen; ++ai) {
      c1 = ((c1 << 0x06) | (str_data.charCodeAt(ai + i) & 0x3F));
    }

    if (seqlen == 4) {
      c1 -= 0x10000;
      tmp_arr.push(String.fromCharCode(0xD800 | ((c1 >> 10) & 0x3FF)), String.fromCharCode(0xDC00 | (c1 & 0x3FF)));
    } else {
      tmp_arr.push(String.fromCharCode(c1));
    }

    i += seqlen;
  }

  return tmp_arr.join("");
}
