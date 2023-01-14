let spinner         = "<div class='spinner-grow text-primary m-1' role='status'><span class='sr-only'>Loading...</span></div>"

// Alert message
function alert_message(type, title, message, additional_message="") {
    // let bg_class    = "";
    // if (type == "danger") {
    //     bg_class = "bg-red2-dark"
    // }

    // let close_button    = "";
    // let result  = "<div class='ml-3 mr-3 alert alert-small rounded-s shadow-xl "+ bg_class +"' role='alert'><span><i class='fa fa-check'></i></span>"+ message +"</strong><button type='button' class='close color-white opacity-60 font-16' data-dismiss='alert' aria-label='Close'>×</button></div>"
    // let result          = "<div class='card card-style '"+ bg +"role='alert'><strong>"+ message +"</strong></div>";
    // let result  = "<div class='alert alert-primary border-0' role='alert'><strong>"+ message +"</strong></div>"

    let result  = "<div class='alert border-0 alert-" + type + "' role='alert'> <strong>" + title + "</strong> <br />" + message + " " + additional_message + "</div>"

    // let result = "<div class='card'> <div class='card-header text-strong text-white bg-" + type +  "'>"  + title + " </div>  <div class='card-body'>  <p class='card-text text-center'>" + message + "</p> </div> </div>"
    return result;
}




/** 
 * Ajax custom function
 * 
*/

// This function will be deleted on next version
// Ajax load
let ajax_load   = (div_id, namespace) => {
    url = namespace
    console.log("Loaded!")
    $.ajax({
        url         : url,
        type        : "GET",
        beforeSend  : function() {
            $("#" + div_id).html(spinner)
        },
        success     : function(response) {
            $("#" + div_id).html(response)
        }
    })
}

// Ajax unload
let ajax_unload = (id_div)=> {
    console.log("Unloaded!")
    $("#" + id_div).empty()
}


// Ajax post
let ajax_post   = (id_form, class_btn_submit, id_message, action_url, load_ajax, load_id_ajax, load_ajax_url, hide_modal, id_modal) => {
    $("#" + id_form).submit(function(e) {
        e.preventDefault();
        let btn_text    = $("." + class_btn_submit).text()
        $('.' + class_btn_submit).html("<span class='fa fa-circle-o-notch fa-spin'></span> Proses...")
        $("." + class_btn_submit).attr('disabled', true)
        let data = $("#" + id_form).serializeArray();
        $.ajax({
            url         : action_url,
            type        : "POST",
            data        : data,
            dataType    : "JSON",
            success : function(response) {
                if (response.status == "success") {
                    message = alert_message(response.type, "Success", response.message)
                    $("#" + id_message).html(message)
                    console.log(response.message)
                    if (hide_modal) {
                        modal_hide(id_modal)
                    }

                    if (load_ajax) {
                        ajax_load(load_id_ajax, load_ajax_url)
                    }
                    $("#" + id_form).trigger("reset")
                }

                if (response.status == "error") {
                    console.log(response.message)
                    message = alert_message(response.type, "Error", response.message)
                    $("#" + id_message).html(message)
                }

                $('.' + class_btn_submit).html(btn_text)
                $("." + class_btn_submit).attr('disabled', false)
            }
        })
    })
}

// Ajax files
let ajax_files   = (id_form, class_btn_submit, id_message, action_url, load_ajax, load_id_ajax, load_ajax_url, hide_modal, id_modal) => {
    $("#" + id_form).submit(function(e) {
        e.preventDefault();
        let btn_text    = $("." + class_btn_submit).text()
        $('.' + class_btn_submit).html("<span class='fa fa-circle-o-notch fa-spin'></span> Proses...")
        $("." + class_btn_submit).attr('disabled', true)
        let data = new FormData($("#" + id_form)[0]); 
        $.ajax({
            url         : action_url,
            type        : "POST",
            data        : data,
            dataType    : "JSON",
            contentType : false,
            processData : false,
            success : function(response) {
                if (response.status == "success") {
                    message = alert_message(response.type, "Success", response.message)
                    $("#" + id_message).html(message)
                    console.log(response.message)
                    if (hide_modal) {
                        modal_hide(id_modal)
                    }

                    if (load_ajax) {
                        ajax_load(load_id_ajax, load_ajax_url)
                    }
                    $("#" + id_form).trigger("reset")
                }

                if (response.status == "error") {
                    console.log(response.message)
                    message = alert_message(response.type, "Error", response.message)
                    $("#" + id_message).html(message)
                }

                $('.' + class_btn_submit).html(btn_text)
                $("." + class_btn_submit).attr('disabled', false)
            }
        })
    })
}







/**
*   Updated by _claudiocanigia
*   Feb 24, 2022
*   new function to handling ajax request
*   this function will replace functions ajax_post and ajax_files 
*   1. xpost
*   2. xupload
*   3. xload
*   4. xunload
*/

//
let show_message    = (message_id) => {}

// Ajax method post
let xpost  = (form_id, namespace, success_function) => {
    $("#" + form_id).submit(function(e) {
        e.preventDefault();
        let data = $("#" + form_id).serializeArray();
        $.ajax({
            url         : namespace,
            type        : "POST",
            data        : data,
            dataType    : "JSON",
            success     : function(response) {
                success_function(response)
            }
        })
    })
}

let xupload = (form_id, namespace, success_function) => {}

let xload   = (div_id, namespace) => {
    url = namespace
    console.log("Loaded!")
    $.ajax({
        url         : url,
        type        : "GET",
        beforeSend  : function() {
            $("#" + div_id).html(spinner)
        },
        success     : function(response) {
            $("#" + div_id).html(response)
        }
    })
}

// Ajax unload
let xunload = (div_id)=> {
    console.log("Unloaded!")
    $("#" + div_id).empty()
}













/** 
 * Modal custom function
 * 
*/

// Show modal
let modal_show  = (modal_id, modal_body_id, namespace) => {
    $("#" + modal_id).modal("show")
    url = namespace
    $.ajax({
        url     : url,
        type    : "GET",
        success : function(response) {
            $("#" + modal_body_id).html(response)
        }
    })
}

// Hide modal
let modal_hide  = (modal_id) => {
    $('#' + modal_id).modal('hide')
}

/** 
 * Touchspin custom function
 * 
*/

let prefix_touchspin    = (input_name) => {
    $("input[name='" + input_name + "']").TouchSpin({
        min             : 0,
        max             : 9999999999999999,
        boostat         : 5,
        maxboostedstep  : 10,
        prefix          : ''
    });
}

/**
 * Offcanvas custom function
 * 
 */

// Offcanvas toggle
let offcanvas_toggle    = (offcanvas_id, offcanvas_body_id, namespace) => {
    $("#" + offcanvas_id).offcanvas("toggle")
    url = namespace
    $.ajax({
        url     : url,
        type    : "GET",
        success : function(response) {
            $("#" + offcanvas_body_id).html(response)
        }
    })
}