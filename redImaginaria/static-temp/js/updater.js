(function(a,c){c=a(c);a.fn.updater=function(h,g){var f=a.extend(true,{},b,h),e=setInterval(d.init,f.interval);c.data("updater",{options:f,callback:g,interval:e,isActive:true,lastRequest:""});c.bind("init.updater",d.init).bind("start.updater",d.reboot).bind("stop.init",d.stop).trigger("init.updater");return};var d={init:function(){if(d.obj().isActive){var e=d.obj().options,f=d.obj().callback;d.pull(e,f)}return},setStatus:function(e){d.obj().lastRequest=e;return},pull:function(e,g){var f=(e.method==="post")?"POST":"GET";a.ajax({url:e.url,data:e.data,type:f,dataType:e.response,success:function(i,h){d.setStatus(h);g(i,h)},error:function(h){d.setStatus(h)}});return},stop:function(){if(d.obj().isActive){clearInterval(d.obj().interval)}d.obj().isActive=false;return},reboot:function(){if(!d.obj().isActive){var f=d.obj().options,e=d.obj().callback;a.updater(f,e)}d.obj().isActive=true;return},obj:function(){return c.data("updater")},debug:function(){if(console){console.group();console.log("Url: ",d.obj().options.url);console.log("Interval: ",d.obj().options.interval);console.log("Method: ",d.obj().options.method);console.log("Data: ",d.obj().options.data);console.log("Callback: ",d.obj().callback);console.log("Last Request: ",d.obj().lastRequest);console.log("Requests Continues: ",d.obj().isActive);console.groupEnd()}return}},b={url:undefined,data:undefined,method:"post",response:"json",interval:3000,};a.updater=a.fn.updater;a.updater.stop=d.stop;a.updater.start=d.reboot;a.updater.debug=d.debug})(jQuery,document);