

// Onclick= attribute for every <a> tag displaying the character's name. Opens the window to apply for the gig. Long term goal is to put this in the email.
function selectPhoto(iid, bid, el) {
    if (typeof(window) !== "undefined") {
        var editcart = "";
        var winl = (screen.width - 800) / 2;
        var wint = (screen.height - 600) / 2;
        winprops = 'top='+wint+',left='+winl;
        if (typeof el !== 'undefined' && el.tagName == 'A' && el.text.indexOf('CHANGE PHOTO') > -1){
        editcart = "&editcart=1";
        }
        window.open('/projects/?view=selectphoto&from=breakdowns&region=32&iid=' + iid + '&bid=' + bid + editcart, 'select_photo', 'scrollbars,resizable,width=800,height=600,' + winprops);
    }
    return 0;
}
function remove(iid) {
    redirect_url = '/projects/?view=breakdowns&breakdown=724155&region=32&removeitem=' + iid;
    location.replace(redirect_url);
}
selectPhoto(4512834,725387)
// print()
// javascript: selectPhoto(4512834,725387);