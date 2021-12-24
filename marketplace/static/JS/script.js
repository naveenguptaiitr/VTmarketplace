$(document).ready(function(){

    var viewCommentVisibility = false;

    //Ajax interaction for retrieving comments from the database for an item
    $("#comments-recorded").click(function (){
        if(!viewCommentVisibility){

            var item_id1 = $(this).attr('data-item-id');
            var username = $(this).attr('data-user-name');
            var ajax_url1 = $(this).attr('data-ajax-url');

            // Using the core $.ajax() method
            $.ajax({

                // The URL for the request
                url: ajax_url1,

                // The data to send (will be converted to a query string)
                data: {
                    _id: item_id1
                },

                // Whether this is a POST or GET request
                type: "GET",

                headers: {'X-CSRFToken':csrftoken},

                // The type of data we expect back
                dataType : "json",

                context: this
            })
              // Code to run if the request succeeds (is done);
              // The response is passed to the function
              .done(function(json) {
                  //alert("request received successfully")
                  if(json.success == 'success') {
                      if (json.comments.length == 0) {

                          var newCommentFormat = `<div class = "comments-recorded"> <p class="user-comment-recorded"> No Comments Available</p> </div>`;
                          $(".user-commented").append(newCommentFormat);
                          viewCommentVisibility = true;
                      } else {

                          for (let i = 0; i < json.comments.length; i++) {

                              if (username == json.comments[i].user || json.comments[i].role == "admin") {
                                  var newCommentFormat = `<div class = "comments-recorded"> <p class="user-comment-recorded"> ${json.comments[i].comment} &emsp; </p>
                                 <p class=user-comment-time"> Commented By <a href="/users/profile/${json.comments[i].user}">${json.comments[i].user} </a> &emsp; </p>
                                 <p class="user-comment-time">Commented on: ${json.comments[i].date}  </p>
                                 <input type="hidden" class="hidden-id" value="${json.comments[i].id}">
                                 <button id="comment-edit-button" >Edit</button>
                                 <button id="comment-delete-button">Delete</button></div>`;
                              } else {
                                  var newCommentFormat = `<div class = "comments-recorded"> <p class="user-comment-recorded"> ${json.comments[i].comment} &emsp; </p>
                                 <p class=user-comment-time"> Commented By <a href="/users/profile/${json.comments[i].user}">${json.comments[i].user} </a> &emsp; </p>
                                 <p class="user-comment-time">Commented on: ${json.comments[i].date} </p>
                                 <input type="hidden" class="hidden-id" value="${json.comments[i].id}"></div>`;
                              }

                              $(".user-commented").append(newCommentFormat);

                          }
                          viewCommentVisibility = true;
                      }
                  }
                  else {
                      alert("ERROR: " + json.error);
                  }

              })
              // Code to run if the request fails; the raw request and
              // status codes are passed to the function
              .fail(function( xhr, status, errorThrown ) {
                //alert( "Sorry, there was a problem!" );
                console.log( "Error: " + errorThrown );

              })
              // Code to run regardless of success or failure;
              .always(function( xhr, status ) {
                //alert( "The request is complete!" );
              });
        }

    });


    //boolean variable to change and add new comment on detail page
    var userCommentID = 1;

    //For editing the existing comment
    $('.user-commented').on('click', '#comment-edit-button', function(){

        //for EDITING the comment
        var userCommentElement = $("#createUserComment");
        let existingComment =$(this).siblings(('.user-comment-recorded')).html();
        userCommentElement.val(existingComment);
        editCommentHTMLElement = $(this).parent();
        userCommentID = $(this).siblings(".hidden-id").val();
    });

    var editCommentHTMLElement = false;

    $('.user-commented').on('click', '#comment-delete-button', function (){
       var comment_id = $(this).siblings(".hidden-id").val();
       // var ajax_url = $(this).attr('data-ajax-url2');
        $.ajax({

            // The URL for the request
            url: "/marketplace/deletecomment",

            // The data to send (will be converted to a query string)
            data: {
                _comment_id: comment_id,
            },

            // Whether this is a POST or GET request
            type: "POST",

            headers: {'X-CSRFToken': csrftoken},

            // The type of data we expect back
            dataType: "json",

            context: this
        })
        .done(function (json) {
                $(this).siblings().remove();
                $(this).remove();
            })
            // Code to run if the request fails; the raw request and
            // status codes are passed to the function
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);

            })
            // Code to run regardless of success or failure;
            .always(function (xhr, status) {
                // alert("The request is complete!");
            });
    });


    //Ajax interaction to submit or add a comment on the item
    //added and modifying an existing element
    $(".submit-button").click(function(){

        var createUserCommentElement = $("#createUserComment");
        var userComment = createUserCommentElement.val();

        //if the comment length is zero then alert the user when
        //clicking on submit button
        if(userComment.length <= 0){
            alert('No Comment added');
        }

        //Ajax interaction - if the comment is already posted then comment will either be added or modified
        else{

            let commentDate = (new Date()).toLocaleString('en-US');

            //For adding new comment on the page
            if(!editCommentHTMLElement){

                var item_id2 = $(this).attr('data-item-id');
                var ajax_url2 = $(this).attr('data-ajax-url');
                const formData = new FormData();
                formData.append("_id", item_id2);
                formData.append("_comment", userComment);


                // Using the core $.ajax() method
                $.ajax({

                    // The URL for the request
                    url: ajax_url2,
                    data: formData,


                    processData: false,
                    // The data to send (will be converted to a query string)
                    contentType: false,

                    // Whether this is a POST or GET request
                    type: "POST",

                    headers: {'X-CSRFToken':csrftoken},

                    // The type of data we expect back
                    dataType : "json",

                    context: this
                })
                  // Code to run if the request succeeds (is done);
                  // The response is passed to the function
                  .done(function(json) {
                      //alert("request received successfully")
                      if(json.success == 'success'){
                          for(i=0; i<json.comments.length; i++) {
                                var newCommentFormat = `<div class = "comments-recorded"> <p class="user-comment-recorded"> ${json.comments[i].comment} </p>
                             <p class="user-comment-time">Commented: ${json.comments[i].date}</p>
                             <input type="hidden" class="hidden-id" value="${json.comments[i].id}">
                             <p>Commented By: <a href="/users/profile/${json.comments[i].user}">${json.comments[i].user}</a></p>
                            <button id="comment-edit-button">Edit</button>
                            <button id="comment-delete-button"> Delete</button></div>`;
                          }
                          $("#comments-recorded").after(newCommentFormat);
                      }
                      else{
                          alert("ERROR: " + json.error);
                      }

                  })
                  // Code to run if the request fails; the raw request and
                  // status codes are passed to the function
                  .fail(function( xhr, status, errorThrown ) {
                    //alert( "Sorry, there was a problem!" );
                    console.log( "Error: " + errorThrown );

                  })
                  // Code to run regardless of success or failure;
                  .always(function( xhr, status ) {
                    //alert( "The request is complete!" );
                  });

            }

            //For editing already posted comment on the page
            else {
                //locating the correct HTML element to edit
                editCommentHTMLElement.find('.user-comment-recorded').html(userComment);

                let notifySuccess = $('<p class = ".user-comment"> Comment edited successfully</p>');

                //successfully EDITED comment message for users
                $(notifySuccess).appendTo($(".user-comment")).fadeOut('slow', function(){
                        $(this).remove();
                });

                var comment_id = userCommentID;
                var ajax_url = $(this).attr('data-ajax-url2');

                $.ajax({
                    // The URL for the request
                    url: ajax_url,

                    // The data to send (will be converted to a query string)
                    data: {
                        _comment_id: comment_id,
                        _new_comment: userComment
                    },

                    // Whether this is a POST or GET request
                    type: "POST",

                    headers: {'X-CSRFToken': csrftoken},

                    // The type of data we expect back
                    dataType: "json",

                    context: this
                })
                    .done(function (json){

                    })
                    .fail(function (json){

                    })
                    .always(function (json){

                    })


            }
            editCommentHTMLElement = false;
            createUserCommentElement.val("");
        }
    });

    //added and modifying an existing element
    $(".content").on("change","#inputPriceValidation",function(){

        //reading the item price
        var itemPrice = $(this).val();

        //creating warning message element
        var warningMessage = $(`<p class="warning-message"> Price cannot be negative</p>`);

        if(itemPrice<0){

            //modifying the element when the condition is matched
            $("#inputPriceValidation").css("border", "2px solid red");

            //adding the element when the condition is matched
            $(warningMessage).appendTo($(this).parent());

        }
        else{

            //modifying the element when the condition is not matched
            $("#inputPriceValidation").css("border", "2px solid rgb(204 204 204)");

            //removing the added element when the condition is false
            $(".warning-message").remove();
        }
    });

    //Calling the simulated search method
    checkQueryString();

});

//Simulated Search Result method
function checkQueryString(){

    var queryString = window.location.search;
    var urlParams = new URLSearchParams(queryString);

    //parsing the search phrase
    if(urlParams.has("search-items")){
        var keyword = urlParams.get("search-items");

        //using if statement to match for the keyboard phrase and
        //return result for keyboard items
        if(keyword == 'keyboard'){

            //creating result for the searched key phrase when the
            //match is true
            var searchedItem = $('<div class="item-list">' + '<a href ="detail.html" class="link">' +
                '<img src="data/Simulated%20Search%20Result/keyboard%205.png" alt="Item 1" class = "individual-item-image" />' +
                '<p class = "item-caption">Light up Keyboard </p>' + '</a>' +
                '</div>' +

                '<div class="item-list">' + '<a href ="detail.html" class="link">' +
                '<img src="data/Simulated%20Search%20Result/keyboard%202.jpeg" alt="Item 1" class = "individual-item-image" />' +
                '<p class = "item-caption">Light up Keyboard </p>' + '</a>' +
                '</div>' +

                '<div class="item-list">' + '<a href ="detail.html" class="link">' +
                '<img src="data/Simulated%20Search%20Result/keyboard%203.jpeg" alt="Item 1" class = "individual-item-image" />' +
                '<p class = "item-caption">Light up Keyboard </p>' + '</a>' +
                '</div>' +

                '<div class="item-list">' + '<a href ="detail.html" class="link">' +
                '<img src="data/Simulated%20Search%20Result/keyboard%204.jpeg" alt="Item 1" class = "individual-item-image" />'+
                '<p class = "item-caption">Light up Keyboard </p>' + '</a>' +
                '</div>');

             //appending the search result to html page
             $(".search-result-content").append(searchedItem);

             //notifying the user  as alert message
             window.alert("You searched keyboard");

        }

        //using if statement to match for the laptop phrase and
        //return result for laptop items
        else if(keyword == 'laptop'){

            //creating result for the searched key phrase when the
            //match is true
            var searchedItem = $('<div class="item-list">' + '<a href ="detail.html" class="link">' +
                '<img src="data/Simulated%20Search%20Result/laptop_4.jpeg" alt="Item 1" class = "individual-item-image" />' +
                '<p class = "item-caption">MacBook Air 11" </p>' + '</a>' +
                '</div>' +

                '<div class="item-list">' + '<a href ="detail.html" class="link">' +
                '<img src="data/Simulated%20Search%20Result/laptop_3.jpeg" alt="Item 1" class = "individual-item-image" />' +
                '<p class = "item-caption">Dell Inspiron 15 </p>' + '</a>' +
                '</div>' +

                '<div class="item-list">' + '<a href ="detail.html" class="link">' +
                '<img src="data/Simulated%20Search%20Result/laptop_2.jpeg" alt="Item 1" class = "individual-item-image" />' +
                '<p class = "item-caption">Dell laptop </p>' + '</a>' +
                '</div>' +

                '<div class="item-list">' + '<a href ="detail.html" class="link">' +
                '<img src="data/Simulated%20Search%20Result/laptop_1.jpeg" alt="Item 1" class = "individual-item-image" />'+
                '<p class = "item-caption">Surface Pro 3 </p>' + '</a>' +
                '</div>');

            //appending the search result to html page
            $(".search-result-content").append(searchedItem);

            //notifying the user  as alert message
            window.alert("You searched laptop");
        }

        //if the search phrase does not match defined keywords then
        //return no search found result
        else{

            //creating result for the searched key phrase when the
            //match is false
            var noItem = $('<h2>No Result Found</h2>');

            //appending the search result to html page
            $(".search-result-content").append(noItem);

            //notifying the user  as alert message
            window.alert("No Item Found");
        }

    }

}

//function to get cookie for ajax header
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');