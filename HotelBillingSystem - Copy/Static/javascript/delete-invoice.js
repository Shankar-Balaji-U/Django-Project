'use strict';
{
    $.fn.popupInvoiceDelete = function(opts) {
        const options = $.extend({}, $.fn.popupInvoiceDelete.defaults, opts);
        const $this = $(this);
        const urlLocation = window.location.origin;



        const createContainer = function(name, url) {
            let submit = $('<a class="' + options.submitCss + ' fs-6 text-decoration-none col-6 m-0 rounded-0"' + '><strong>Yes, delete</strong></a>'); 
            let cancel = $('<button type="button" class="' + options.cancelCss + ' fs-6 text-decoration-none col-6 m-0 rounded-0" data-bs-dismiss="modal">Cancel</button>'); 

            submit.attr('href', urlLocation + url)

            /* Creating all elements and initiallizations */

            let modal = $('<div class="modal fade" id="' + options.containerId + '" data-bs-backdrop="static" tabindex="-1" aria-labelledby="delete-invoice-label" aria-hidden="true"></div>');

            let dialogue_box = $('<div class="modal-dialog modal-dialog-centered" style="max-width: 350px;"></div>');
            let dialogue_content = $('<div/>').addClass('modal-content');

            let dialogue_body = $('<div/>').addClass('modal-body p-4 text-center');
            let dialogue_form = $('<form/>').attr('method', "post");
            let dialogue_footer = $('<div/>').addClass('modal-footer flex-nowrap p-0');

            let heading = $('<h5 class="modal-title mb-2" id="delete-invoice-label"></h5>').text("Are you sure?");
            let description = $('<p/>').addClass('mb-0').text(options.message);


            $(document.body).append(modal);
            modal.append(dialogue_box);
            dialogue_box.append(dialogue_content);
            dialogue_content.append(dialogue_body);
            dialogue_content.append(dialogue_form);
            dialogue_body.append(heading);
            dialogue_body.append(description);
            dialogue_body.append('<strong>' + name + '</strong>');
            dialogue_form.append(dialogue_footer);
            dialogue_footer.append(options.csrf_token);
            dialogue_footer.append(submit);
            dialogue_footer.append(cancel);

            document.getElementById(options.containerId).addEventListener('hidden.bs.modal', function (event) {
                $(this).remove()
            });
        };


        /* This is to set id of the same dialogue box for all 
        the button by changing the target or focus of the button */
        $('.' + options.deleteBtnCss).each(function() {
            $(this).on('mouseover', function() {
                $(this).attr("data-bs-target", "#" + options.containerId);
                createContainer($(this).data("name"), $(this).data("object-url"));
            });

            $(this).on('mouseout', function() {
                $(this).removeAttr("data-bs-target");
                $("#" + options.containerId).remove();
                
            });
        });
    };
    /* Setup plugin defaults */
    $.fn.popupInvoiceDelete.defaults = {
        containerId: "delete-invoice-dialoguebox",
        csrf_token: '<input type="hidden" name="csrfmiddlewaretoken" value="DwI0rJ2TEupE4MyAoISOgJOyEx76ikq79h31HQFM4i7ZhjAOA1u7fSpoYXJWO2Pa">',
        message: "Do you really want to delete this record? This process cannot be undone.",
        submitCss: "btn btn-lg btn-link",
        cancelCss: "btn btn-lg btn-link",
        deleteBtnCss: "delete-btn"
    };
}


$(document).ready(function() {
    $().popupInvoiceDelete({
        deleteBtnCss: "delete-button"
    });
});




function activeDeleteAllButton() {
    let parent = $(this).parent();

    if($(this).is(':checked')){
        console.log('Preparing for delete all...');

        let $(".delete-option").length
        console.log()

//         parent.append('<button type="submit" class="btn btn-danger">Delete All</button>');
//         parent.append(input);
//         input.checked('true');
    } else {
        console.log('Delete all is cancelled...');
//         parent.html('Delete All');
    }
}



$("#delete-all-btn").on('change', activeDeleteAllButton);