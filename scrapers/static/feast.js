$(document).ready(function(){


// $(".noUiSlider").noUiSlider({
//     range: [0, 100],
//     start: 0,
//     step: 1,
//     handles: 1,
//     slide: function(){
//       var value = $(this).val();
//       console.log(value);
//       // track.seek(value);
//       seek(value);
//    }
// });


// function seek(num){
//     track.seek(num);

// }
// $("ul ul").click(function(this){
// 	alert(this);
// };


var h=$(window).height();
console.log(h)
$('.scrollable').height(h+'px');


$("#track-seek").click(function(){
    track.seek(30);
});

$("#artist-sort").click(function(){
    $('ul').tsort({data:'artist'});

});

$("#type-sort").click(function(){
    $('.stream-item').tsort('span.release-type');
});


$("#label-sort").click(function(){
    //$('ul').tsort('span.label');
    //$('ul').tsort({data:'label'});
    $(".stream-item").tsort("div.label");
});

$("#date-sort").click(function(){
    // for (var i=0; i < $("span.date").length; i++){
    //     var day = $("span.date")[i];
    //     day_long = day.innerText;
    //     var seconds = Date.parse(day_long);
    //     //  console.log(seconds);
    //     //doesn't work on single element, only on list, which seems wrong/sloppy
    //     $(day).attr("data-seconds", seconds);
    // }
    // $(".stream-item").tsort("span.date", {data:'seconds', order:'desc'});

    sort_by_date();

    //$(".stream-item").tsort("span.date", {order:'desc'});
    //$(".stream-item").tsort(Date.parse($("ul.stream-item span.date").innerText));
});

$("#catalog-sort").click(function(){
    //$('.stream-item').tsort('ul span.catalog-number');
    //$('ul').tsort({data:'catalog-number'});
    $(".stream-item").tsort("div.catalog-number");
});

function sort_by_date(){
    for (var i=0; i < $("span.date").length; i++){
        var day = $("span.date")[i];
        day_long = day.innerText;
        var seconds = Date.parse(day_long);
        //  console.log(seconds);
        //doesn't work on single element, only on list, which seems wrong/sloppy
        $(day).attr("data-seconds", seconds);
    }
    $(".stream-item").tsort("span.date", {data:'seconds', order:'desc'});
}

sort_by_date();

$.ajaxSetup({ 

    "error":function(XMLHttpRequest,textStatus, errorThrown) {   
      // alert(textStatus);
      // alert(errorThrown);
      alert(XMLHttpRequest.responseText);
  },

     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     },


});



$('.follow-artist').click(function(e){
    var button = $(e.target)
    // var $target = $(e.target).parent();
    // var $target_parent = $($target).parent();
    // console.log($target);
    // console.log($target_parent);
    // var artist_id = $($target).data('artist-id');
    // var artist_name = $($target_parent).data('artist');
    var artist_id = $(button).data('artist-id');
    console.log('artist id: ' +artist_id);
    // console.log("artist" +artist)
    // console.log('artist name: '+artist_name);
    $release = $(button).closest('.release');
    console.log("this is the album element: "+$release)
    artist_name = $($release).data("artist")
    console.log("artist name is "+artist_name)
    data = {'type':'artist', 'artist_id':artist_id, 'artist_name':artist_name};
    $.ajax({
        type: "POST",
        url: "/follow_toggle/",
        data: data ,
        success: function(){
            //alert("it worked");
            console.log( button);
            if ($(button).text() != "Following"){
                $(button).text("Following");
            }
            else{
                $(button).text("Follow");
            }
        },
        })

    // .then(
    //         function(){ alert(" follow succeeded"); 
    //             },
    //         function(){ alert(" follow failed!"); 
    //             }
    //     );

})


$('.follow-label').click(function(e){
    var button = $(e.target)
    // var $target = $(e.target).parent();
    // var $target_parent = $($target).parent();
    // console.log($target);
    // console.log($target_parent);
    var label_id = $(button).data('label-id');
    var label_name = $(button).data('label-name');
    console.log(label_id)
    //var artist_name = $($target_parent).data('artist');
    // console.log('artist id: ' +artist_id);
    // console.log('artist name: '+artist_name);
    data = {'type':'label', 'label_id':label_id, 'label_name':label_name};
    $.ajax({
        type: "POST",
        url: "/follow_toggle/",
        data: data,
        success: function(){
            //alert("it worked");
            console.log( button);
            if ($(button).text() != "Following"){
                $(button).text("Following");
            }
            else{
                $(button).text("Follow");
            }
        },
        })

})


$('.love-album').click(function(e){
    var button = $(e.target)
    // var $target = $(e.target).parent();
    // var $target_parent = $($target).parent();
    // console.log($target);
    // console.log($target_parent);
    var reid = $(button).data('reid');
    var artist = $(button).data('artist');
    var title = $(button).data('album-title');
    
    console.log(reid)
    //var artist_name = $($target_parent).data('artist');
    // console.log('artist id: ' +artist_id);
    // console.log('artist name: '+artist_name);
    data = {'type':'album', 'reid':reid, 'artist':artist, 'title':title};
    $.ajax({
        type: "POST",
        url: "/follow_album/",
        // url: "/follow_toggle/",
        data: data,
        success: function(){
            //alert("it worked");
            console.log( button);
            if ($(button).hasClass("red")){
                $(button).removeClass("red");
            }
            else{
                $(button).addClass("red");
            }
        },
    })

})

// for albums
$(".add-album").click(function(e){
    addPopover(e, 'album-to-playlist')
    e.stopPropagation();
})

$(document).on('click', ".add-track", function(e) {
// $(".add-track").on('click',function(e){
    console.log("add-track clicked  ")
    addPopover(e, 'track-to-playlist')
    e.stopPropagation();
})





//close popovers on outside click
$(document).on("click", function (e) {
    console.log("clicked document")
    var $target = $(e.target),
        isPopover = $(e.target).is('.popover'),
        inPopover = $(e.target).closest('.popover').length > 0
        var $popover = $('.popover');
        console.log("")

    //hide only if clicked on button or inside popover
    if (!isPopover && !inPopover) {
        // $popover.popover('hide');
        // $popover.remove()
        $(".add-album, .add-track").popover('destroy')
    }   
});


function addPopover(e, add_class){

    var $target = $(e.target)
    $(".add-album, .add-track").not($target).popover('destroy')


    if ($($target).next(".popover").length>0){
        // $(".add-album").next(".popover").toggle()
        // $($target).popover("toggle")
        $($target).next(".popover").toggle()
        // $($target).popover("destroy")
        console.log("popover exists");
    }
    else{
    console.log("popover does not exist")


    $.ajax({
        url: "/get_playlists/",
        }).done(function(data){
            console.log(".done worked, this is the data");
            console.log(data);
            var $div = $('<div>');
            var $create = $('<div><a href = "/create_playlist/">Create Playlist</a></div><br></br>');
            $($div).append($create)


            var playlists = data['playlists']
            console.log('playlists: ', playlists)

            for(i=0; i< playlists.length; i++){

                console.log("looping through playlist")
                var name = playlists[i]['name']
                console.log("playlist name: ", name)
                var $a = $('<a>')
                $($a).attr("href", "/playlist/"+playlists[i]['pk'])
                $($a).text(playlists[i]['name']+ " ")
                var $add_button = $("<button>", {class:"btn btn-default "+add_class, type:"button", "data-playlist-id":playlists[i]['pk']})
                $($add_button).text("Add")
                
                var $div2 = $("<div>", {class: "playlist", 'data-playlist-id':playlists[i]['pk']})
                $div2.append($a)
                $div2.append($add_button)
                $div.append($div2)
            }
            var $h5 = $("<h5>")
            $h5.append($div)
            // $('body').popover({
            //         selector: '[rel=popover]'
            // })
            console.log('$div: ', $div)
            console.log("$target: ", $target)
            $target.popover(
                {placement:'bottom', 
                html:true, 
                content: $h5,
                trigger: 'focus',
                toggle: 'popover',
                selector: '[rel="popover"]',
                // content: "<a href = '/create_playlist'>Create New Playlist</a><span><a class = btn btn-default>Add</a></span>"
            })
            $target.popover('show')
        })
    }
}


$(document).on('click', ".track-to-playlist", function(e){
    console.log('popover add button clicked')
    var $target = $(e.target)
    var $playlist = $(e.target).closest(".playlist")
    var playlist_id = $($playlist).data("playlist-id")

    var $track = $($target).closest(".track")
    var artist_name = $($track).data("artist")
    var artist_id = $($track).data("artist-id")
    var title = $($track).data("title")
    var mbid = $($track).data("track-id")

    data = {'playlist_id':playlist_id, 'artist_name':artist_name, 'artist_id':artist_id, 'title':title, 'mbid':mbid};
    console.log(data)
    $.ajax({
        type: "POST",
        url: "/track_to_playlist/",
        // url: "/follow_toggle/",
        data: data,
    }).done(function(){
        alert("track was added to playlist")
    })
})



$(document).on('click', ".album-to-playlist", function(e){
    console.log('popover add button clicked')
    var $target = $(e.target)
    var $playlist = $(e.target).closest(".playlist")
    var playlist_id = $($playlist).data("playlist-id")


    var $album = $($target).closest(".album")
    var artist_name = $($album).data("artist")
    var artist_id = $($album).data("artist-id")
    var title = $($album).data("album-title")
    var reid = $($album).data("reid")

    data = {'playlist_id':playlist_id, 'artist_name':artist_name, 'artist_id':artist_id, 'title':title, 'reid':reid};
    console.log(data)
    $.ajax({
        type: "POST",
        url: "/album_to_playlist/",
        // url: "/follow_toggle/",
        data: data,
    }).done(function(){
        alert("album was added to playlist")
    })



})
//     // var $target = $(e.target)
//     // var playlist_id = $($target).data("playlist-id")
//     // var album_title
//     // var artist
//     // var artist_id
//     // var album_id  =



    // call back end to get user playlists

    // write 'content'
    // generate popover, include content


    // var $target = $(e.target)


    // toggle popover

    // $(".glyphicon-plus").popover({placement:'bottom', 
    //     html:true, 
    //     content: "<a href = '/create_playlist'>Create New Playlist</a><span><a class = btn btn-default>Add</a></span>"})



// $(document).on('click', ".like-track", function(e) {
// // $('.like-track').click(function(e){
//     var button = $(e.target)
//     console.log("like button clicked");
//     // var $target = $(e.target).parent();
//     // var $target_parent = $($target).parent();
//     // console.log($target);
//     // console.log($target_parent);
//     var track_id = $(button).data('track-id');
//     // console.log(label_id)
//     //var artist_name = $($target_parent).data('artist');
//     // console.log('artist id: ' +artist_id);
//     // console.log('artist name: '+artist_name);
//     data = {'type':'track', 'track_id':track_id,};
//     $.ajax({
//         type: "POST",
//         url: "/follow_toggle/",
//         data: data,
//         success: function(){
//             //alert("it worked");
//             console.log( button);
//             if ($(button).text() != "Like"){
//                 $(button).text("Like");
//             }
//             else{
//                 $(button).text("You Like This");
//             }
//         },
//         })

// })



$(document).on('click', ".delete-playlist", function(e){
    var $target = $(e.target)
    var $playlist = $target.closest(".playlist")
    var playlist_id = $target.data("playlist-id")
    console.log(playlist_id, $playlist)
    var result = window.confirm("Are you sure you want to delete this playlist? You won't be able to get it back if you do.")
    if(result){
        // $playlist.remove()
        data = {'playlist_id':playlist_id};
        $.ajax({
            type: "POST",
            url: "/remove_playlist/",
            data: data,
            success: function(){
                //alert("it worked");
                $playlist.remove()
            },
        })
    }
    
})

$(document).on('click', ".delete-track", function(e) {
    console.log("delete-track clicked")
     var $target = $(e.target)
     var $track = $target.closest(".track")
     console.log("track: ",$track)
     var entry_id = $target.data('entry-id')
     console.log(entry_id)
     var result = window.confirm("Are you sure you want to delete this from your playlist?")
     if (result){
        delete_entry(entry_id, $track)
     }
     
})

$(document).on('click', ".delete-album", function(e) {
    console.log("delete-album clicked")
     var $target = $(e.target)
     var $album = $target.closest(".album")
     console.log("album: ",$album)
     var entry_id = $target.data('entry-id')
     console.log(entry_id)
     var result = window.confirm("Are you sure you want to delete this from your playlist?")
     if (result){
        delete_entry(entry_id, $album)
     }
     
})





function delete_entry(entry_id, $element_to_remove){
    console.log("will remove this element", $element_to_remove)
    data = {'entry_id':entry_id};
    $.ajax({
        type: "POST",
        url: "/delete_entry/",
        data: data,
        success: function(){
            //alert("it worked");
            $element_to_remove.remove()
        },
    })
}

$(document).on('click', ".love-track", function(e) {
// $('.like-track').click(function(e){
    var button = $(e.target)
    // $track = $(button).closest("[data-track-id]")
    $track = $(button).closest(".track")
    console.log("love track button clicked");
    // var $target = $(e.target).parent();
    // var $target_parent = $($target).parent();
    // console.log($target);
    // console.log($target_parent);
    var track_id = $($track).data('track-id');
    var artist = $($track).data('artist');
    var artist_id = $($track).data('artist-id');
    var title = $($track).data('title');
    // console.log(label_id)
    //var artist_name = $($target_parent).data('artist');
    // console.log('artist id: ' +artist_id);
    // console.log('artist name: '+artist_name);
    data = {'type':'track', 'track_id':track_id, 'artist':artist, 'artist_id':artist_id, 'title':title};
    $.ajax({
        type: "POST",
        url: "/follow_toggle/",
        data: data,
        success: function(){
            //alert("it worked");
            console.log( button);
            if ($(button).hasClass("red")){
                $(button).removeClass("red");
            }
            else{
                $(button).addClass("red");
            }
        },
        })

})


var currentTrack;




$('.play-entire-album').click(function(e){
    expand_album(e, true) 
})



//expand album
$('.expand-album').click(function(e){
    expand_album(e, false)
});

function expand_album(e, play_on_expand){
    console.log("album expanded")
    //alert("album clicked")
    var $target = $(e.target);
    console.log($target);
    var album = $($target).closest(".release")
    console.log(album)
    var tracklist = $(album).find(".album-tracks")

    if($(tracklist).children("li").length >= 1 && play_on_expand){
        $(tracklist).children("li").show()
        play_album(album)
    }

    else if($(tracklist).children("li").length >= 1){
        $(tracklist).children("li").toggle();
    }
    else{
        var reid = $(album).data('reid');
        console.log("reid: "+reid)
        var artist = $(album).data("artist");
        console.log("artist: ", artist)
        var title = $(album).data("album-title");
        $ul = tracklist;

        if (reid !== undefined && reid !== ""){
            
            var data = {"reid": reid, 'artist':artist, 'title':title};
            // $.getJSON("/lastfm_album_tracks/", data, function(json){
            $.getJSON("/album_ajax/", data, function(json){
                console.log("calling getJSON")
                if(json['tracks']){
                    //alert("json?: " + json["tracks"]+" reid: "+json['reid']);
                    // var album = $('data-reid ='+)
                    for(var i=0; i<json['tracks'].length; i++){
                        //console.log(json['tracks'][i]['title'])
                        var artist = json['tracks'][i]['artist']
                        var title = json['tracks'][i]['title']
                        var track_id = json['tracks'][i]['track_id']
                        var following = json['tracks'][i]['following_sound']
                        var artist_id = json['tracks'][i]['artist_id']

                        var $li = create_album_track(artist, title, track_id, following, artist_id);
                        // $($ul).append("<li class = 'album-track track' data-artist = '"+escape(artist) +"' data-title ='" + escape(title) +"' data-track-id = '"+track_id+"'>"+artist +" - "+ title+"<button type='button' class = 'like-track' data-track-id = '"+track_id+"'>"+following+"</button></li>");

                        $($ul).append($li)

                    }
                }
                else{
                    alert('no results')
                }

                if (play_on_expand){
                    // $album = $(e.target).parents(".album")
                    play_album(album)

                }

            })
        }
        else{

            var data = {'artist':artist, 'title':title};
            $.getJSON("/lastfm_album_tracks/", data, function(json){
            // $.getJSON("/album_ajax/", data, function(json){
                console.log("calling getJSON")
                if(json['tracks']){
                    //alert("json?: " + json["tracks"]+" reid: "+json['reid']);
                    // var album = $('data-reid ='+)
                    for(var i=0; i<json['tracks'].length; i++){
                        //console.log(json['tracks'][i]['title'])
                        var artist = json['tracks'][i]['artist']
                        var title = json['tracks'][i]['title']
                        var track_id = json['tracks'][i]['track_id']
                        var following = json['tracks'][i]['following_sound']
                        var artist_id = ""

                        var $li = create_album_track(artist, title, track_id, following, artist_id);
                        // $($ul).append("<li class = 'album-track track' data-artist = '"+escape(artist) +"' data-title ='" + escape(title) +"' data-track-id = '"+track_id+"'>"+artist +" - "+ title+"<button type='button' class = 'like-track' data-track-id = '"+track_id+"'>"+following+"</button></li>");

                        $($ul).append($li)

                    }
                }
                else{
                    alert('no results')
                }

                if (play_on_expand){
                    // $album = $(e.target).parents(".album")
                    play_album(album)

                }

            })
        }
    }
}



function create_album_track(artist, title, track_id, following, artist_id){
    var $li = $("<li>", {class:"album-track track"})

    $($li).attr("data-artist",artist);
    $($li).attr("data-artist-id",artist_id);
    $($li).attr("data-title",title);
    $($li).attr("data-track-id", track_id);
    $($li).attr("data-following", following);

    var $play_a = $("<a>")
    var $play_span = $("<span>", {class:"glyphicon glyphicon-play play-track"})
    $($play_a).append($play_span);
    $($li).append($play_a);


    var $artist_a = $("<a>", {href:"/artist/"+artist_id})
    $artist_a.text(artist)
    $($li).append($artist_a)
    // console.log($artist_a)

    var $title_span = $("<span>", {text:" - "+title})
    $($li).append($title_span);

    var $playlist_a = $("<a>", {class:"pull-right", title:"Add to Playlist"})
    var $playlist_span = $("<span>", {class:"glyphicon glyphicon-plus playlist-add add-track"})
    $($playlist_a).append($playlist_span);
    $($li).append($playlist_a);

    var $love_a = $("<a>", {class:"pull-right", title:"Love Track"})
    var $love_span = $("<span>", {class:"glyphicon glyphicon-heart love-track"})
    if (following == true){
        $($love_span).addClass("red")
    }
    $($love_a).append($love_span);
    $($li).append($love_a);

    
    return $li;
}


function play_album($album){
    // console.log($album)
    $tracks = ($album).find(".album-tracks")
    $li = ($tracks).find("li")
    console.log($li)
    play($li[0])
}



// function FollowButtons(){
//     var f_artists = $("[data-following-artist = Following]")
//     for (var i; i<f_artists.length; i+=1){
//         $(f_artists[i]).removeClass("btn-default")
//         $(f_artists[i]).addClass("btn-primary")
//     }
// }

// FollowButtons();

// $('.album').click(function(e){
//     console.log("album clicked")
//     //alert("album clicked")
// 	var $target = $(e.target).parent();
//     console.log($target);
//     if(!$target.is("ul"))
//     //if(!$target.is("div")) //magic happens here!!
//         {
//             console.log("target is not ul");
//             return;
//         }
// 	if($(this).children("li").length >= 1){
// 		$(this).children("li").toggle();
// 	}
// 	else{
//         var reid = $($target).data('reid');
// 	    //var reid = $(this).data('reid');
//         if (reid !== undefined){
//             console.log("reid: "+reid)
//     	    ul = this;
//     	    var data = {"reid": reid};
//     	    // var args = { type:"GET", url:"/album/", data:data, complete:done };
//     	    // $.ajax(args);
//     	    $.getJSON("/album_ajax/", data, function(json){
//                 console.log("calling getJSON")
//         	    if(json['tracks']){
//         	    	//alert("json?: " + json["tracks"]+" reid: "+json['reid']);
//         	    	// var album = $('data-reid ='+)
//         	    	for(var i=0; i<json['tracks'].length; i++){
//         	    		//console.log(json['tracks'][i]['title'])
//         	    		var artist = json['tracks'][i]['artist']
//         	    		var title = json['tracks'][i]['title']
//                         var track_id = json['tracks'][i]['track_id']
//                         var following = json['tracks'][i]['following_sound']
//         	    		$(ul).append("<li class = 'album-track track' data-artist = '"+escape(artist) +"' data-title ='" + escape(title) +"' data-track-id = '"+track_id+"'>"+artist +" - "+ title+"<button type='button' class = 'like-track' data-track-id = '"+track_id+"'>"+following+"</button></li>");
//         	    	}
//                 }
//     		else{
//     			alert('no results')
//     		}

// 		})
//     }
// 	}
// });

// $(document).on('click', ".album-track", function(e) {
// 	// var artist = $(this).data('artist');
// 	// var title = $(this).data('title');
//  //    artist = unescape(artist);
//  //    title = unescape(title);
// 	// alert(artist + " - "+title);
// 	// renderTrack(artist, title);

//     var $target = $(e.target)
//     var track = $(e).closest(".album-track")
//     if(!$target.is("li"))
//         {
//             console.log("target is not li");
//             return;
//         }
// 	play(this);
// 	// alert("you clicked a track");
// });



$(document).on('click', ".play-track", function(e) {
    // var artist = $(this).data('artist');
    // var title = $(this).data('title');
 //    artist = unescape(artist);
 //    title = unescape(title);
    // alert(artist + " - "+title);
    // renderTrack(artist, title);
    console.log("track clicked")
    var track = $(e.target).closest(".album-track")
    console.log(track)
    play(track);
    // alert("you clicked a track");
});


// $(document).on('click', ".track", function(e) {
//     // var artist = $(this).data('artist');
//     // var title = $(this).data('title');
//  //    artist = unescape(artist);
//  //    title = unescape(title);
//     // alert(artist + " - "+title);
//     // renderTrack(artist, title);
//     console.log("track clicked")
//     var track = $(e.target)
//     console.log(track)
//     play(track);
//     // alert("you clicked a track");
// });

function htmlEncode(value){
  //create a in-memory div, set it's inner text(which jQuery automatically encodes)
  //then grab the encoded contents back out.  The div never exists on the page.
  return $('<div/>').text(value).html();
}

function htmlDecode(value){
  return $('<div/>').html(value).text();
}

var lastfm_api_key = "c43db4e93f7608bb10d96fa5f69a74a1"

function loadArt(){
    var releases = $('.release');
    // var tracks = $(".track");
    var artists = $('.artist');

    for (i=0; i<releases.length; i++){

        var release_id = $(releases[i]).data("reid");
        // console.log(release_id);
        var album_art_url = get_album_art(release_id, insert_album_art);
        // console.log(album_art_url);
        // console.log("this is the url loadArt has: " + album_art_url);

    }
}

function get_album_art(release_id, callback){
     var url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key="+lastfm_api_key+"&mbid="+release_id+"&format=json"
     var album_art_url
     var images
     try{
        $.getJSON(url, function(data){
        // console.log(url);
        // console.log(data);
        // console.log(release_id);

            if ('album' in data){
                images = data['album']['image'];

            var sizes_by_rank = { 'mega' : 10, 'extralarge' : 1, 'large' : 0, 'medium' : 3, 'small': 4};

            images = images.sort(function(a,b){
                return (sizes_by_rank[a['size']] - sizes_by_rank[b['size']])
                })
            // console.log(images[0])
            album_art_url = images[0]['#text'];
            callback(album_art_url);
            // console.log("this is the album art URL: " + album_art_url);
            }
            else{
                album_art_url = "";
                callback(album_art_url);
            }
        })
     }
     catch(e){
        console.log(e);
        album_art_url = "";
        callback(album_art_url);
     }
}

function insert_album_art(url){
    if (url != ""){
        console.log("this is the insert_album_art url: " + url)
    }
    // console.log("this is the insert_album_art url: " + url)
}

function hacked_album_art(){
    artist_url = "http://ws.audioscrobbler.com/2.0/?method=artist.imageredirect&mbid="+artist_id+"&autocorrect=1&size=largesquare&api_key="+lastfm_api_key
    album_url = "http://ws.audioscrobbler.com/2.0/?method=album.imageredirect&mbid="+album_id+"&autocorrect=1&size=largesquare&api_key="+lastfm_api_key
}

loadArt();


function getNextElement(currElement, className){
    var elements = $('.' + className);
    var currentIndex = elements.index(currElement);
    return elements[currentIndex + 1];
}

function getPreviousElement(currElement, className){
    var elements = $('.' + className);
    var currentIndex = elements.index(currElement);
    if (currentIndex >= 1){
        return elements[currentIndex -1];
    }
    else{
        return null;
    }
}


function playNext(currElement, className){
    var nextItem = getNextElement(currentTrack, "track");
    if (nextItem !== null){
        play(nextItem);
    }
    else{}
}

function playPrevious(currElement, className){
    var previousItem = getPreviousElement(currentTrack, "track");
    if (previousItem !== null){
        play(previousItem);
    }
    else{}
}



function play(element){


        if (playerTimeout){
            clearTimeout(playerTimeout);

        }

        console.log("play called")
        // ct = $("#current-track")
        
        // $(currentTrack).removeAttr("style")
        // $("#current-track span.play-track").removeAttr("style")
        // console.log("style removed")
        
        // $(currentTrack).find(".play-track").attr("class","glyphicon glyphicon-play play-track")
        $(currentTrack).find(".play-track").removeClass("red")
        $(currentTrack).removeAttr("id")
        // $("#current-track span.play-track").attr("class","glyphicon glyphicon-play play-track")
        console.log("current track class reset")



    	currentTrack = element;
        $(element).attr("id", "current-track")
        // $("#current-track span.play-track").attr("style","color:red")
        // $("#current-track span.play-track").attr("class","glyphicon glyphicon-play play-track red")
        $("#current-track span.play-track").addClass("red")




        if (title === null || artist === null){

        }
        else{
            var artist = $(element).data('artist');
            var title = $(element).data('title');

            $("#now-playing").text(artist +" - "+title);


            var type = $(element).data('type');
            console.log("type", type)

            if(type !== "text"){
                play_embed(element);
                }

            if (type === undefined || type ==="text"){

                console.log("track is not type text")
                artist = unescape(artist);
                artist = removeDiacritics(artist);
                title = unescape(title);
                title = removeDiacritics(title);

                renderTrack(artist, title);  
                console.log("track rendered")
                }
    	   }
}


function play_embed(element){

    // playerEl.innerHTML = "";
    $("#player").empty()

    var type = $(element).data('type');
    var id = $(element).data('id');
    if (type === "yt"){
        var embed = '<iframe width="560" height="315" src="//www.youtube.com/embed/'+id+'?autoplay=1?rel=0" frameborder="0" allowfullscreen></iframe>'
    }
    if (type === "sc"){
        var embed = '<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F'+id+'&amp;auto_play=true"></iframe>'
    }
    if (type === "vimeo"){
        var embed = '<iframe src="//player.vimeo.com/video/'+id +'"width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
    }

    $("#player").append(embed)
    // playerEl.appendChild(embed);



}


$('#play-pause').click(function(){
    // play_pause()
    if (track){
    track.play();
    }
})


$('#play-next').click(function(){
    // play_pause()
    playNext(currentTrack, "track");
})


$('#play-previous').click(function(){
    // play_pause()
    playPrevious(currentTrack, "track");
})


var track;
var playerEl = document.getElementById("player");
var playerTimeout;
var seekbar= false;

renderTrack = function(artist, title){
    var title = title;
    var artist = artist;
    var width = 250;
    var height = 250;

    seekbar = false;

    var disabled0 = undefined;
    var disabled1 = undefined;

    playerEl.innerHTML = "";


    track = window.tomahkAPI.Track(title,artist, {
        

        width:width,
        height:height,
        disabledResolvers: [ disabled0, disabled1 ],
        handlers: {
            onloaded: function() {
                console.log(track.connection+":\n  api loaded");
                hasResolved = false;
                playerTimeout = setTimeout(function(){
                    console.log("Out of patience.")
                    if(!hasResolved){
                        //play($(currentTrack).next(".track"));
                    	//play(getNextElement(currentTrack, "track"));
                        playNext(currentTrack, "track");
                    }
                }
                ,5000);
            },
            onended: function() {
                console.log(track.connection+":\n  Song ended: "+track.artist+" - "+track.title);
                //play($(currentTrack).next("li.track"));
                //play(getNextElement(currentTrack, "track"));
                playNext(currentTrack, "track");
                seekbar = false;
                $(".noUiSlider").empty();
                // $(".noUiSlider").noUiSlider("disabled", true);
            },
            onplayable: function() {
                console.log(track.connection+":\n  playable");
                track.play();
            },
            onresolved: function(resolver, result) {
                hasResolved = true;
                //track.play();
                console.log(track.connection+":\n  Track found: <b>"+resolver+"</b> - "+ result.track + " by "+result.artist);
            },
            ontimeupdate: function(timeupdate) {
                
                var currentTime = timeupdate.currentTime;
                var duration = timeupdate.duration;
                currentTime = parseInt(currentTime);
                duration = parseInt(duration);

                if (!duration){
                    console.log("Duration does not exist yet")
                }

                
                if(duration && seekbar == false){
                    seekbar = true;
                    $(".noUiSlider").empty();
                    $(".noUiSlider").noUiSlider({
                        range: [0, duration],
                        start: currentTime,
                        step: 1,
                        handles: 1,
                        slide: function(){
                          var value = $(this).val();
                          console.log(value)
                          if(track){
                            track.seek(value);
                          }
                          
                       }
                    });
                    console.log("seekbar status: " ,seekbar)
                    console.log("nouislider initiated, duration: ", duration)
                }

                
                else if(seekbar == true && currentTime){
                    $(".noUiSlider").val(currentTime);
                    // console.log("currentTime exists and should be setting the slider to : ", currentTime)
                }


                //console.log(track.connection+":\n  Time update: "+currentTime + " "+duration);
            }  
        }
    });

    playerEl.appendChild(track.render());
}


var defaultDiacriticsRemovalMap = [
    {'base':'A', 'letters':/[\u0041\u24B6\uFF21\u00C0\u00C1\u00C2\u1EA6\u1EA4\u1EAA\u1EA8\u00C3\u0100\u0102\u1EB0\u1EAE\u1EB4\u1EB2\u0226\u01E0\u00C4\u01DE\u1EA2\u00C5\u01FA\u01CD\u0200\u0202\u1EA0\u1EAC\u1EB6\u1E00\u0104\u023A\u2C6F]/g},
    {'base':'AA','letters':/[\uA732]/g},
    {'base':'AE','letters':/[\u00C6\u01FC\u01E2]/g},
    {'base':'AO','letters':/[\uA734]/g},
    {'base':'AU','letters':/[\uA736]/g},
    {'base':'AV','letters':/[\uA738\uA73A]/g},
    {'base':'AY','letters':/[\uA73C]/g},
    {'base':'B', 'letters':/[\u0042\u24B7\uFF22\u1E02\u1E04\u1E06\u0243\u0182\u0181]/g},
    {'base':'C', 'letters':/[\u0043\u24B8\uFF23\u0106\u0108\u010A\u010C\u00C7\u1E08\u0187\u023B\uA73E]/g},
    {'base':'D', 'letters':/[\u0044\u24B9\uFF24\u1E0A\u010E\u1E0C\u1E10\u1E12\u1E0E\u0110\u018B\u018A\u0189\uA779]/g},
    {'base':'DZ','letters':/[\u01F1\u01C4]/g},
    {'base':'Dz','letters':/[\u01F2\u01C5]/g},
    {'base':'E', 'letters':/[\u0045\u24BA\uFF25\u00C8\u00C9\u00CA\u1EC0\u1EBE\u1EC4\u1EC2\u1EBC\u0112\u1E14\u1E16\u0114\u0116\u00CB\u1EBA\u011A\u0204\u0206\u1EB8\u1EC6\u0228\u1E1C\u0118\u1E18\u1E1A\u0190\u018E]/g},
    {'base':'F', 'letters':/[\u0046\u24BB\uFF26\u1E1E\u0191\uA77B]/g},
    {'base':'G', 'letters':/[\u0047\u24BC\uFF27\u01F4\u011C\u1E20\u011E\u0120\u01E6\u0122\u01E4\u0193\uA7A0\uA77D\uA77E]/g},
    {'base':'H', 'letters':/[\u0048\u24BD\uFF28\u0124\u1E22\u1E26\u021E\u1E24\u1E28\u1E2A\u0126\u2C67\u2C75\uA78D]/g},
    {'base':'I', 'letters':/[\u0049\u24BE\uFF29\u00CC\u00CD\u00CE\u0128\u012A\u012C\u0130\u00CF\u1E2E\u1EC8\u01CF\u0208\u020A\u1ECA\u012E\u1E2C\u0197]/g},
    {'base':'J', 'letters':/[\u004A\u24BF\uFF2A\u0134\u0248]/g},
    {'base':'K', 'letters':/[\u004B\u24C0\uFF2B\u1E30\u01E8\u1E32\u0136\u1E34\u0198\u2C69\uA740\uA742\uA744\uA7A2]/g},
    {'base':'L', 'letters':/[\u004C\u24C1\uFF2C\u013F\u0139\u013D\u1E36\u1E38\u013B\u1E3C\u1E3A\u0141\u023D\u2C62\u2C60\uA748\uA746\uA780]/g},
    {'base':'LJ','letters':/[\u01C7]/g},
    {'base':'Lj','letters':/[\u01C8]/g},
    {'base':'M', 'letters':/[\u004D\u24C2\uFF2D\u1E3E\u1E40\u1E42\u2C6E\u019C]/g},
    {'base':'N', 'letters':/[\u004E\u24C3\uFF2E\u01F8\u0143\u00D1\u1E44\u0147\u1E46\u0145\u1E4A\u1E48\u0220\u019D\uA790\uA7A4]/g},
    {'base':'NJ','letters':/[\u01CA]/g},
    {'base':'Nj','letters':/[\u01CB]/g},
    {'base':'O', 'letters':/[\u004F\u24C4\uFF2F\u00D2\u00D3\u00D4\u1ED2\u1ED0\u1ED6\u1ED4\u00D5\u1E4C\u022C\u1E4E\u014C\u1E50\u1E52\u014E\u022E\u0230\u00D6\u022A\u1ECE\u0150\u01D1\u020C\u020E\u01A0\u1EDC\u1EDA\u1EE0\u1EDE\u1EE2\u1ECC\u1ED8\u01EA\u01EC\u00D8\u01FE\u0186\u019F\uA74A\uA74C]/g},
    {'base':'OI','letters':/[\u01A2]/g},
    {'base':'OO','letters':/[\uA74E]/g},
    {'base':'OU','letters':/[\u0222]/g},
    {'base':'P', 'letters':/[\u0050\u24C5\uFF30\u1E54\u1E56\u01A4\u2C63\uA750\uA752\uA754]/g},
    {'base':'Q', 'letters':/[\u0051\u24C6\uFF31\uA756\uA758\u024A]/g},
    {'base':'R', 'letters':/[\u0052\u24C7\uFF32\u0154\u1E58\u0158\u0210\u0212\u1E5A\u1E5C\u0156\u1E5E\u024C\u2C64\uA75A\uA7A6\uA782]/g},
    {'base':'S', 'letters':/[\u0053\u24C8\uFF33\u1E9E\u015A\u1E64\u015C\u1E60\u0160\u1E66\u1E62\u1E68\u0218\u015E\u2C7E\uA7A8\uA784]/g},
    {'base':'T', 'letters':/[\u0054\u24C9\uFF34\u1E6A\u0164\u1E6C\u021A\u0162\u1E70\u1E6E\u0166\u01AC\u01AE\u023E\uA786]/g},
    {'base':'TZ','letters':/[\uA728]/g},
    {'base':'U', 'letters':/[\u0055\u24CA\uFF35\u00D9\u00DA\u00DB\u0168\u1E78\u016A\u1E7A\u016C\u00DC\u01DB\u01D7\u01D5\u01D9\u1EE6\u016E\u0170\u01D3\u0214\u0216\u01AF\u1EEA\u1EE8\u1EEE\u1EEC\u1EF0\u1EE4\u1E72\u0172\u1E76\u1E74\u0244]/g},
    {'base':'V', 'letters':/[\u0056\u24CB\uFF36\u1E7C\u1E7E\u01B2\uA75E\u0245]/g},
    {'base':'VY','letters':/[\uA760]/g},
    {'base':'W', 'letters':/[\u0057\u24CC\uFF37\u1E80\u1E82\u0174\u1E86\u1E84\u1E88\u2C72]/g},
    {'base':'X', 'letters':/[\u0058\u24CD\uFF38\u1E8A\u1E8C]/g},
    {'base':'Y', 'letters':/[\u0059\u24CE\uFF39\u1EF2\u00DD\u0176\u1EF8\u0232\u1E8E\u0178\u1EF6\u1EF4\u01B3\u024E\u1EFE]/g},
    {'base':'Z', 'letters':/[\u005A\u24CF\uFF3A\u0179\u1E90\u017B\u017D\u1E92\u1E94\u01B5\u0224\u2C7F\u2C6B\uA762]/g},
    {'base':'a', 'letters':/[\u0061\u24D0\uFF41\u1E9A\u00E0\u00E1\u00E2\u1EA7\u1EA5\u1EAB\u1EA9\u00E3\u0101\u0103\u1EB1\u1EAF\u1EB5\u1EB3\u0227\u01E1\u00E4\u01DF\u1EA3\u00E5\u01FB\u01CE\u0201\u0203\u1EA1\u1EAD\u1EB7\u1E01\u0105\u2C65\u0250]/g},
    {'base':'aa','letters':/[\uA733]/g},
    {'base':'ae','letters':/[\u00E6\u01FD\u01E3]/g},
    {'base':'ao','letters':/[\uA735]/g},
    {'base':'au','letters':/[\uA737]/g},
    {'base':'av','letters':/[\uA739\uA73B]/g},
    {'base':'ay','letters':/[\uA73D]/g},
    {'base':'b', 'letters':/[\u0062\u24D1\uFF42\u1E03\u1E05\u1E07\u0180\u0183\u0253]/g},
    {'base':'c', 'letters':/[\u0063\u24D2\uFF43\u0107\u0109\u010B\u010D\u00E7\u1E09\u0188\u023C\uA73F\u2184]/g},
    {'base':'d', 'letters':/[\u0064\u24D3\uFF44\u1E0B\u010F\u1E0D\u1E11\u1E13\u1E0F\u0111\u018C\u0256\u0257\uA77A]/g},
    {'base':'dz','letters':/[\u01F3\u01C6]/g},
    {'base':'e', 'letters':/[\u0065\u24D4\uFF45\u00E8\u00E9\u00EA\u1EC1\u1EBF\u1EC5\u1EC3\u1EBD\u0113\u1E15\u1E17\u0115\u0117\u00EB\u1EBB\u011B\u0205\u0207\u1EB9\u1EC7\u0229\u1E1D\u0119\u1E19\u1E1B\u0247\u025B\u01DD]/g},
    {'base':'f', 'letters':/[\u0066\u24D5\uFF46\u1E1F\u0192\uA77C]/g},
    {'base':'g', 'letters':/[\u0067\u24D6\uFF47\u01F5\u011D\u1E21\u011F\u0121\u01E7\u0123\u01E5\u0260\uA7A1\u1D79\uA77F]/g},
    {'base':'h', 'letters':/[\u0068\u24D7\uFF48\u0125\u1E23\u1E27\u021F\u1E25\u1E29\u1E2B\u1E96\u0127\u2C68\u2C76\u0265]/g},
    {'base':'hv','letters':/[\u0195]/g},
    {'base':'i', 'letters':/[\u0069\u24D8\uFF49\u00EC\u00ED\u00EE\u0129\u012B\u012D\u00EF\u1E2F\u1EC9\u01D0\u0209\u020B\u1ECB\u012F\u1E2D\u0268\u0131]/g},
    {'base':'j', 'letters':/[\u006A\u24D9\uFF4A\u0135\u01F0\u0249]/g},
    {'base':'k', 'letters':/[\u006B\u24DA\uFF4B\u1E31\u01E9\u1E33\u0137\u1E35\u0199\u2C6A\uA741\uA743\uA745\uA7A3]/g},
    {'base':'l', 'letters':/[\u006C\u24DB\uFF4C\u0140\u013A\u013E\u1E37\u1E39\u013C\u1E3D\u1E3B\u017F\u0142\u019A\u026B\u2C61\uA749\uA781\uA747]/g},
    {'base':'lj','letters':/[\u01C9]/g},
    {'base':'m', 'letters':/[\u006D\u24DC\uFF4D\u1E3F\u1E41\u1E43\u0271\u026F]/g},
    {'base':'n', 'letters':/[\u006E\u24DD\uFF4E\u01F9\u0144\u00F1\u1E45\u0148\u1E47\u0146\u1E4B\u1E49\u019E\u0272\u0149\uA791\uA7A5]/g},
    {'base':'nj','letters':/[\u01CC]/g},
    {'base':'o', 'letters':/[\u006F\u24DE\uFF4F\u00F2\u00F3\u00F4\u1ED3\u1ED1\u1ED7\u1ED5\u00F5\u1E4D\u022D\u1E4F\u014D\u1E51\u1E53\u014F\u022F\u0231\u00F6\u022B\u1ECF\u0151\u01D2\u020D\u020F\u01A1\u1EDD\u1EDB\u1EE1\u1EDF\u1EE3\u1ECD\u1ED9\u01EB\u01ED\u00F8\u01FF\u0254\uA74B\uA74D\u0275]/g},
    {'base':'oi','letters':/[\u01A3]/g},
    {'base':'ou','letters':/[\u0223]/g},
    {'base':'oo','letters':/[\uA74F]/g},
    {'base':'p','letters':/[\u0070\u24DF\uFF50\u1E55\u1E57\u01A5\u1D7D\uA751\uA753\uA755]/g},
    {'base':'q','letters':/[\u0071\u24E0\uFF51\u024B\uA757\uA759]/g},
    {'base':'r','letters':/[\u0072\u24E1\uFF52\u0155\u1E59\u0159\u0211\u0213\u1E5B\u1E5D\u0157\u1E5F\u024D\u027D\uA75B\uA7A7\uA783]/g},
    {'base':'s','letters':/[\u0073\u24E2\uFF53\u00DF\u015B\u1E65\u015D\u1E61\u0161\u1E67\u1E63\u1E69\u0219\u015F\u023F\uA7A9\uA785\u1E9B]/g},
    {'base':'t','letters':/[\u0074\u24E3\uFF54\u1E6B\u1E97\u0165\u1E6D\u021B\u0163\u1E71\u1E6F\u0167\u01AD\u0288\u2C66\uA787]/g},
    {'base':'tz','letters':/[\uA729]/g},
    {'base':'u','letters':/[\u0075\u24E4\uFF55\u00F9\u00FA\u00FB\u0169\u1E79\u016B\u1E7B\u016D\u00FC\u01DC\u01D8\u01D6\u01DA\u1EE7\u016F\u0171\u01D4\u0215\u0217\u01B0\u1EEB\u1EE9\u1EEF\u1EED\u1EF1\u1EE5\u1E73\u0173\u1E77\u1E75\u0289]/g},
    {'base':'v','letters':/[\u0076\u24E5\uFF56\u1E7D\u1E7F\u028B\uA75F\u028C]/g},
    {'base':'vy','letters':/[\uA761]/g},
    {'base':'w','letters':/[\u0077\u24E6\uFF57\u1E81\u1E83\u0175\u1E87\u1E85\u1E98\u1E89\u2C73]/g},
    {'base':'x','letters':/[\u0078\u24E7\uFF58\u1E8B\u1E8D]/g},
    {'base':'y','letters':/[\u0079\u24E8\uFF59\u1EF3\u00FD\u0177\u1EF9\u0233\u1E8F\u00FF\u1EF7\u1E99\u1EF5\u01B4\u024F\u1EFF]/g},
    {'base':'z','letters':/[\u007A\u24E9\uFF5A\u017A\u1E91\u017C\u017E\u1E93\u1E95\u01B6\u0225\u0240\u2C6C\uA763]/g}
];
var changes;
function removeDiacritics (str) {
    if(!changes) {
        changes = defaultDiacriticsRemovalMap;
    }
    for(var i=0; i<changes.length; i++) {
        str = str.replace(changes[i].letters, changes[i].base);
    }
    return str;
}

});



