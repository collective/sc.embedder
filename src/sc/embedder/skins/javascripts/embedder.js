$(document).ready(function() {
    $('#alt_cont .alt_cont_text').hide();
    $('#alt_cont a').click(function(){
        $('#alt_cont .alt_cont_text').toggleFade();
    });
});

(function($) {
    $.fn.toggleFade = function(settings)
    {
        if(settings === undefined) {
            settings={ speedIn : 'fast'};
        }

        settings = jQuery.extend(
                {
                    speedIn: "normal",
                    speedOut: settings.speedIn
                }, settings
        );
        return this.each(function()
                {
            var isHidden = jQuery(this).is(":hidden");
            jQuery(this)[ isHidden ? "fadeIn" : "fadeOut" ]( isHidden ? settings.speedIn : settings.speedOut);
                });
    };
})(jQuery);