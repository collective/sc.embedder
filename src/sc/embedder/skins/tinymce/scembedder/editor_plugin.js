/**
 * sc.embedder plugin
 *
 * @author Juan Pablo Gimenez
 */

(function() {
    tinymce.create('tinymce.plugins.SCEmbedderPlugin', {
        init : function(ed, url) {
            ed.settings.extended_valid_elements = "iframe[src|title|width|height|allowfullscreen|webkitallowfullscreen|mozallowfullscreen|frameborder]";
            // Register commands
            ed.addCommand('mceSCEmbedder', function() {
                // Internal image object like a flash placeholder
                if (ed.dom.getAttrib(ed.selection.getNode(), 'class').indexOf('mceItem') != -1)
                    return;

                ed.windowManager.open({
                    file : url + '/scembedder.htm',
                    width : 840 + parseInt(ed.getLang('scembedder.delta_width', 0)),
                    height : 530 + parseInt(ed.getLang('scembedder.delta_height', 0)),
                    inline : 1
                }, {
                    plugin_url : url
                });
            });

            // Register buttons
            ed.addButton('scembedder', {
                title : 'advanced.scembedder_desc',
                cmd : 'mceSCEmbedder',
                image : url + '/embedder.png'
            });
        },

        getInfo : function() {
            return {
                longname : 'sc.embedder',
                author : 'Simples Consultoria',
                authorurl : 'http://simplesconsultoria.com.br',
                infourl : 'http://github.com/simplesconsultoria/sc.embedder',
                version : tinymce.majorVersion + "." + tinymce.minorVersion
            };
        }
    });

    // Register plugin
    tinymce.PluginManager.add('scembedder', tinymce.plugins.SCEmbedderPlugin);
})();