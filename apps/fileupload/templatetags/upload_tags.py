from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def upload_js(per):
    if per=='Administrador':
        return mark_safe("""
        <!-- The template to display files available for upload -->
        <script id="template-upload" type="text/x-tmpl">
        {% for (var i=0, file; file=o.files[i]; i++) { %}
            <tr class="template-upload fade">

                <td>
                    <p class="name">{%=file.name%}</p>
                    {% if (file.error) { %}
                        <div><span class="label label-important">{%=locale.fileupload.error%}</span> {%=file.error%}</div>
                    {% } %}
                </td>
                <td>
                    <p class="size">{%=o.formatFileSize(file.size)%}</p>
                    {% if (!o.files.error) { %}
                        <div class="progress progress-striped active" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="progress-bar progress-bar-success" style="width:0%;"></div></div>
                    {% } %}
                </td>

                <td>
                    {% if (!o.files.error && !i && !o.options.autoUpload) { %}
                        <button class="btn btn-primary start">
                            <i class="glyphicon glyphicon-upload"></i>
                            <span>{%=locale.fileupload.start%}</span>
                        </button>
                    {% } %}


                </td>

            </tr>
        {% } %}
        </script>
        <!-- The template to display files{%=file.name%} available for download -->
        <script id="template-download" type="text/x-tmpl">
        {% for (var i=0, file; file=o.files[i]; i++) { %}
            <tr class="template-download fade">

                <td>
                    <p class="name">
                       <a href={%=file.url%}>{%=file.name%}</a>
                    </p>
                    {% if (file.error) { %}
                        <div><span class="label label-important">{%=locale.fileupload.error%}</span> {%=file.error%}</div>
                    {% } %}
                </td>

                <td>
                    <span class="size">{%=o.formatFileSize(file.size)%}</span>
                </td> 
                <td>
                    
                    <form>
                      <button class="btn btn-danger"  formaction={%=file.deleteUrl%}>
                      <i class="glyphicon glyphicon-trash"></i>
                      Eliminar
                      </button>
                    </form>
                    
                </td>
                <td>
                         <a href="{%=file.thumbnailUrl%}  ">
                            Descargar
                        </a> 
                </td>

                <td>
                   <p style={%=file.color%} class="Verificacion" >{%=file.verificacion%} </p>
                
                </td>
            </tr>
        {% } %}

        </script>  
        """)
    else:
        return mark_safe("""
        <!-- The template to display files available for upload -->
        <script id="template-upload" type="text/x-tmpl">
        {% for (var i=0, file; file=o.files[i]; i++) { %}
            <tr class="template-upload fade">

                <td>
                    <p class="name">{%=file.name%}</p>
                    {% if (file.error) { %}
                        <div><span class="label label-important">{%=locale.fileupload.error%}</span> {%=file.error%}</div>
                    {% } %}
                </td>
                <td>
                    <p class="size">{%=o.formatFileSize(file.size)%}</p>
                    {% if (!o.files.error) { %}
                        <div class="progress progress-striped active" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="progress-bar progress-bar-success" style="width:0%;"></div></div>
                    {% } %}
                </td>

                <td>
                    {% if (!o.files.error && !i && !o.options.autoUpload) { %}
                        <button class="btn btn-primary start">
                            <i class="glyphicon glyphicon-upload"></i>
                            <span>{%=locale.fileupload.start%}</span>
                        </button>
                    {% } %}


                </td>

            </tr>
        {% } %}
        </script>
        <!-- The template to display files{%=file.name%} available for download -->
        <script id="template-download" type="text/x-tmpl">
        {% for (var i=0, file; file=o.files[i]; i++) { %}
            <tr class="template-download fade">

                <td>
                    <p class="name">
                       <a href={%=file.url%}>{%=file.name%}</a>
                    </p>
                    {% if (file.error) { %}
                        <div><span class="label label-important">{%=locale.fileupload.error%}</span> {%=file.error%}</div>
                    {% } %}
                </td>

                <td>
                    <span class="size">{%=o.formatFileSize(file.size)%}</span>
                </td> 
                <td>
                <a href="{%=file.thumbnailUrl%}  ">
                            Descargar
                        </a> 
                </td>
                <td>
                   <p style={%=file.color%} class="Verificacion" >{%=file.verificacion%}</p>  
                </td>
            </tr>
        {% } %}

        </script>
        """)











