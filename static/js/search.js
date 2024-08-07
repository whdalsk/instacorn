$(document).ready(function() {
    $('#search-input').on('keypress',function(event) {
        if(event.which == 13){
            var keyword = $('#search-input').val();
            alert('keyword ' + keyword)
            $.ajax({
                url: 'instaselect.do',
                type: 'GET',
                data: { sval : keyword} ,
                success: function(data) {
                    $('#results').empty();
                    $.each(data.hashresult, function(index,item) {
                        $('#results').append('<p>' + item.content + '</p>');
                        
                    });

                    
                    $.each(data.justresult, function(index,item) {
                        $('#results').append(
                            '<a href="/myprofile.do/?b_no='+item.m_no+'">' +
                                '<div class="card-heading">' +
                                //'<img src="/static/images/img2.jpg" class="profile">' +
                                    '<img src="/static/images/' + item.profileimg + '" class="profile">' + 
                                    '<div class="cardusername">' +
                                        '<p><b>' + item.id + '</b></p>' + 
                                        '<p class="item-name">' + item.name + '</p>' + 
                                    '</div>' +
                                '</div>' +
                            '</a>'


                        );
                        
                    });
                },
                error: function() {
                    $('#results').append('<p>검색 중 오류가 발생했습니다.</p>')
                }
            });
        }
    });
});


          
function w3_open() {
  document.getElementById("search-input").value = "";
  document.getElementById("mySidebar").style.display = "block";
}

function w3_close() {
  var searchInput = document.getElementById("search-input");
  document.getElementById("mySidebar").style.display = "none";
  
}
