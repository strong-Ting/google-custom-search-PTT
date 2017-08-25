//test
$(document).ready(function(){
    
    var config = {
      //  siteURL     : 'tutorialzine.com',   // Change this to your site
        searchSite  : true,
      //  type        : 'web',
        append      : false,
        perPage     : 10,            // A maximum of 8 is allowed by Google
        page        : 1             // The start page
    }
    
    // The small arrow that marks the active search icon:
    var arrow = $('<span>',{className:'arrow'}).appendTo('ul.icons');
    
    $('ul.icons li').click(function(){
        var el = $(this);
        
        if(el.hasClass('active')){
            // The icon is already active, exit
            return false;
        }
        
        el.siblings().removeClass('active');
        el.addClass('active');
        
        // Move the arrow below this icon
        arrow.stop().animate({
            left        : el.position().left,
            marginLeft  : (el.width()/2)-4
        });
        
        // Set the search type
      //  config.type = el.attr('data-searchType');
        $('#more').fadeOut();
    });
    
    // Adding the site domain as a label for the first radio button:
//    $('#siteNameLabel').append(' '+config.siteURL);
    
    // Marking the Search tutorialzine.com radio as active:
    $('#searchSite').click();   
    
    // Marking the web search icon as active:
    $('li.web').click();
    
    // Focusing the input text box:
    $('#s').focus();

    $('#searchForm').submit(function(){
        run()
        return false;
    });
    
    $('#searchSite,#searchWeb').change(function(){
        // Listening for a click on one of the radio buttons.
        // config.searchSite is either true or false.
        
        config.searchSite = this.id == 'searchSite';
    });
    
    function run() {
    //get form element
    var oform = document.forms['searchForm'];
    var queryID = oform.elements['query'].value;
        
    $.ajax({
            url: '/query',
            data:{
                query:queryID,
                page:config.page,
                perPage:config.perPage
            },
            type: 'POST',
            dataType: 'json',
            success: function(data) {

            var resultsDiv = $('#resultsDiv');
            var pageContainer = $('<div>',{className:'pageContainer'});
           for(var i=0;i<data['num'];i++)
            {
                var perData = data['data'][i];
                pageContainer.append(new query_result(perData));
                pageContainer.append('<div class="clear"></div>')
                             .hide().appendTo(resultsDiv)
                             .fadeIn('slow');

            }
              
            },
            error: function(error) {
                alert(error);
            }

    });
  }

    function query_result(perData){
        
    var title = perData['title'];   
    var link = perData['link'];
    var  web =  '<div class="webResult">';
    var  title =' <h2><a href='+link +'>'+title+'</a></h2>' ;
 
    if ('push' in perData)
    {
        var IDcontent = perData['push'];
    }  
    else 
    {
        var IDcontent = perData['post_content'];
    }
    var  content = ' <p>'+IDcontent+'</p>';

    var readMore = '<a href="'+link +'">閱讀全文</a>'

    var  result = [ web+title+content+readMore+ '</div>'];
    

    return result;

    }




});



