'use strict';
{
    $.fn.notification = function(opts) {
        const options = $.extend({}, $.fn.formset.defaults, opts);
        const $this = $(this);
        const $parent = $this.parent();
  
        const toggleVisibility = function(inlineGroup) {

        };
 
        return this;
    };


    /* Setup plugin defaults */
    $.fn.notification.defaults = {
        barid: "notification-bar", // The form prefix for your django formset
        listCssClass: "add-row", // CSS class applied to the add link
        addCssClass: "add-row", // CSS class applied to the add link
        deleteCssClass: "delete-row", // CSS class applied to the delete link
    };
}