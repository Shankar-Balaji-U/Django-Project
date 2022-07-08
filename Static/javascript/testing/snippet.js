var pathname = window.location.pathname; // Returns path only (/path/example.html)
var url      = window.location.href;     // Returns full URL (https://example.com/path/example.html)
var origin   = window.location.origin;   // Returns base URL (https://example.com)


var opacity = 0;
const fadeIn = function(id) {
    setInterval(function () {
        id.style.display = 'block';
        opacity = Number(id.style.opacity);
        if(opacity < 1) {
            id.style.opacity = opacity + 0.01;
        } else {
            clearInterval(0);
        }
    }, .5);
};

const fadeOut = function(id) {
    console.log(id.style.opacity);
    setInterval(function () {
        opacity = Number(id.style.opacity);
        if(opacity > 0) {
            id.style.style.cssText = `opacity: ${Number(opacity - 0.01)}`;
            
        } else {
            id.style.display = 'none';
            
            clearInterval(0);
        }
    }, 1);
};
































































/* -------------------------------------------------------------------------
     class - airbox message read
     ----------------------------------------------------------------------------- */
AIRBOX.smsRead = (function() {
    var s = {
            $content: $("article#sms"),
            $smsContent: $("#smsContent"),
            $list: $("article#sms div.list"),
            $reply: $(".reply"),
            phoneNumList: [],
            unReadNum: 0,
            loadedPageNum: 0,
            totalPage: 0
        },
        lnboxList = new Array();
    cs = {};

    function init(options) {
        $.extend(s, options);
        cs = AIRBOX.core.settings;
        _initStatus();
    };

    function _initStatus() {
        showSmsCardState(simCardState, pinState, simlockState, function() {
            //smsNumber = SDK.SMS.GetSMSContentList(0, currContactId).PhoneNumber;
            _initContentList(currContactId);
            sms_store = SDK.SMS.GetSMSStorageState();
            currentCount = sms_store.TUseCount;
            leftCount = sms_store.LeftCount;
            _initMessageContent();
            _initScroll();
            _initClickReply();
            _clickSmsIcon();
            _hoverTitle();
        });
    }

    function _initoverScroll() {

        $('.scroll-pane', s.$content).on(cs.overEvent, function(event) {
            event.preventDefault();
            event.stopPropagation();
            //_initScroll();                    
        });
    };

    function _initContentList(contactId) {
        $("#ContentListTable").html("");
        draftId = null;
        contentListInfo = SDK.SMS.GetSMSContentList(0, contactId);
        smsNumber = contentListInfo.PhoneNumber;
        if (contentListInfo.PhoneNumber.length == 0 && $("#messageContent").val() == "") {
            page.changePage("sms/smsList.html")
        }
        /*
        s.totalPage = contentListInfo.TotalPageCount;
        var currlnboxList = [];
        for (var i = 0; i < s.totalPage; i++) {
            currlnboxList = SDK.SMS.GetSMSContentList(i + 1, contactId).SMSContentList;
            $.merge(lnboxList, currlnboxList);
        }

        lnboxList = lnboxList.reverse();
        showItem(lnboxList);
        */
        showItem(contentListInfo.SMSContentList.reverse());
        showPhoneNumber();

        $("#sms_not_read").html(s.unReadTotalNum);
        _initDeleteButtons();
    };

    function showPhoneNumber() {
        var phoneNumStr = "";
        if (smsNumber.length == 0) {
            str2 = "";
        } else {
            for (i = 0; i < smsNumber.length - 1; i++) {
                phoneNumStr = phoneNumStr + smsNumber[i] + ";";
            }
            phoneNumStr = phoneNumStr + smsNumber[smsNumber.length - 1];
            $(".contact-number").html(phoneNumStr);
        }
    }

    function showItem(smslist) {
        var i = 0,smsTimeLines,month = new Array();
        if (smslist != null) {
            for (var e in smslist) {
                var connectlnbox = smslist[e];
                if(config.SupportTimeLine){
                    var smsTime = connectlnbox.SMSTime;
                    var timeVal = getSmsMonth(connectlnbox.SMSTime);
                    var tmpDate = smsTime.split(" ")[0];
                    var smsMonth = tmpDate.split("-")[1];
                    month[i] = smsMonth;
                    
                    if(i == 0){
                        smsTimeLines = "<li class='smsTimeLine'><span>"+timeVal+"</span></li>";
                    }else if(month[i-1] != month[i]){
                        smsTimeLines = "<li class='smsTimeLine'><span>"+timeVal+"</span></li>";
                        }else{
                            smsTimeLines = "";
                        }
                }else{
                    smsTimeLines = "";
                }
                if (connectlnbox != "") {
                    _addItem(connectlnbox,smsTimeLines);
                }
                i++;
            }
        }
    }

    function _addItem(itemvalue,smsMonthVal) {
        var _sms_id = itemvalue.SMSId,
            _sms_time = fomatTime(itemvalue.SMSTime),
            _sms_content = itemvalue.SMSContent.HTMLEncode(),
            _sms_type = itemvalue.SMSType;

        _sms_content = _sms_content.replace(/\n/g, "<br />");

        var smsTypeHtml = "";
        if (_sms_type == SMS_LIST_SMS_TYPE_SENT_FAILED) {
            smsTypeHtml = "<span class=\"sms-icon icon-fail\"></span>";
        }
        var itemTable = $("#ContentListTable");
        var itemStr = "";
        var smsMevalue = /^[2,3,6]$/;
        isSmsMe = smsMevalue.test(_sms_type) ? "\"sms-boxme\"" : "\"sms-box\"";
        if (_sms_type == SMS_LIST_SMS_TYPE_DRAFT) {
            draftId = _sms_id;
            smsContent = _sms_content;
        } else {
            if (_sms_type == SMS_LIST_SMS_TYPE_REPORT) {
                itemStr += "<h3>" + sys.getRes("ids_sms_delivered") + "</h3>";
            } else {
                itemStr += "<h3>" + _sms_content + "</h3>";
                itemStr += "<span class=\"sms-icon trash\"></span><span class=\"sms-icon reply\"></span>";
            }

            itemStr += "<span class=sms-time>" + _sms_time + "</span>" + smsTypeHtml;
            itemTable.append(smsMonthVal +"<li class=" + isSmsMe + "value=" + _sms_id + "><div class=\"sms-textbg\">&nbsp;</div><div class=\"sms-text\">" + itemStr + "</div></li>");
        }
        if(config.TimeForNonInbox){
            timeForNonInbox();
        }

    }

    function timeForNonInbox(){
        $(".icon-fail").siblings(".sms-time").addClass("hidden");
    }

    function getSmsMonth(smsTime){
        var tmpDate = smsTime.split(" ")[0];
        var smsMonth = tmpDate.split("-")[1];
        var smsDay = tmpDate.split("-")[2];
        var smsYear = tmpDate.split("-")[0];
        var times;
        switch(config.SmsTimeFormat){
            case 0:
                times = smsYear +" "+timeRule(smsMonth)+" "+smsDay;;
                break;
            case 1:
                times = smsDay +" "+timeRule(smsMonth)+" "+smsYear;
                break;
            case 2:
                times = timeRule(smsMonth)+" "+smsDay+" "+smsYear;
                break;
            case 3:
                times = smsDay+" "+timeRule(smsMonth)+" "+smsYear;
                break;
            default:
                times = smsYear +" "+timeRule(smsMonth)+" "+smsDay;
        };
        return times;
    }
    function timeRule(timeVal){
        var monthData = new Array();

            monthData[0] = "January";
            monthData[1] = "February";
            monthData[2] = "March";
            monthData[3] = "April";
            monthData[4] = "May";
            monthData[5] = "June";
            monthData[6] = "July";
            monthData[7] = "August";
            monthData[8] = "September";
            monthData[9] = "October";
            monthData[10] = "November";
            monthData[11] = "December";

        return monthData[timeVal - 1];
    }

    function _initScroll() {
        if (lnboxList.length + "=" + $("#ContentListTable li").length) {
            _hideLoading();
        }

        var api;
        trig = true;

        var pane = $('.scroll-pane', s.$content);
        pane.jScrollPane();
        var jspapi = pane.data('jsp');
        jspapi.scrollToBottom();
    };



    function loadnext() {
        if (s.loadedPageNum < s.totalPage) {
            _showLoading();
            _initContentList(currContactId);
            _initScroll();
        }

        setTimeout(function() {
            trig = true;
        }, 1000);
    }

    function _showLoading() {
        $("#MessageLoadingBkg,#MessageLoading").css("display", "block");
    }

    function _hideLoading() {
        $("#MessageLoadingBkg,#MessageLoading").css("display", "none");
    }

    function _initDeleteButtons() {
        $("#ContentListTable li", s.$content).each(function(i) {
            $(".trash", this).on(cs.clickEvent, {
                index: i
            }, function(event) {
                $el = $(this).parent().parent("li");
                if (config.supportSmsDeleteALLsingle) {
                    messages = 'ids_sms_deleteSingleWarning';
                }
                AIRBOX.smsList.deleteEvent(SMS_DELETE_FLAG_Content, currContactId, parseInt($el.val()), function() {
                    _initRead();
                }, messages);
            });
        });
    };

    function _initClickReply() {
        $("#scrollContent li", s.$content).each(function(i) {
            $(".reply", this).on(cs.clickEvent, function(event) {
                $el = $(this).parent(".sms-text");
                var _sms_id = $el.parent("li").val();
                var replyPage = "#sms/smsWrite.html?&doAction=forward&sms_id=" + _sms_id;
                page.changePage(replyPage);
            });
        });
    };

    function _initMessageContent() {
        doActionFun(doAction);
        $("#btnSent").click(function() {
            startQueueEvent("send");
        })
        $(".back-icon").click(function() {
            startQueueEvent("save", currContactId, draftId);
        })
        showNumCount();
        listenCharCount();
        $("#messageContent").bind("input change keyup keydown paste", function() {
            listenCharCount()
        })
    };

    function _clickSmsIcon() {
        $.each($(".icon-fail"), function(i, obj) {
            var $this = $(obj);
            $this.on("click", function() {
                var clickId = $this.parent().parent("li").attr("value");
                var smsHCont = $this.siblings("h3").html();
                var smsCont = smsHCont.HTMLDecode();
                //SDK.SMS.DeleteSMS(SMS_DELETE_FLAG_Content,currContactId,clickId);
                startQueueEvent("repeat", currContactId, clickId, smsCont, function() {
                    _initRead();
                });
            });
        });
    };

    function _hoverTitle() {
        var titleSpan = $(".contact-number");
        var titleVal = titleSpan.text();
        titleSpan.hover(function() {
            titleSpan.attr("title", titleVal);
        }, function() {
            titleSpan.removeAttr("title");
        });
    };

    function _initRead() {
        s.loadedPageNum = 0;
        sms_store = SDK.SMS.GetSMSStorageState();
        currentCount = sms_store.TUseCount;
        leftCount = sms_store.LeftCount;
        lnboxList = new Array();
        _initContentList(currContactId);
        _initScroll();
        _initClickReply();
        _clickSmsIcon();
    }

    return {
        init: init,
        initScrol: _initScroll,
        initContentList: _initContentList,
        initRead: _initRead
    };
}())

AIRBOX.smsRead.init();
