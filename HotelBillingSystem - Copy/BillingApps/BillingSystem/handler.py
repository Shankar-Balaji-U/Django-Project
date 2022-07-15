# from django.views.defaults import ( bad_request, permission_denied, page_not_found, server_error )
from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError, HttpResponse
)


ERROR_PAGE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>%(title)s</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" / 
    integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
    <link href="/static/bootstrap/custom/css/custom.css" rel="stylesheet">
    <style>
        body {
          font-family: "Nunito", sans-serif;
          -webkit-font-smoothing: antialiased;
        }

        .content-wrapper {
          background: #F5F7FF;
          padding: 2.375rem 2.375rem;
          width: 100%%;
          -webkit-flex-grow: 1;
          flex-grow: 1;
        }

        @media (max-width: 767px) {
          .content-wrapper {
            padding: 1.5rem 1.5rem;
          }
        }

        .error-page h1 {
          font-size: 12rem;
        }

        @media (max-width: 991px) {
          .error-page h1 {
            font-size: 8rem;
          }
        }
    </style>
</head>
<body>
    <div class="overflow-hidden">
        <div class="container-fluid flex-row d-flex min-vh-100 w-100 p-0">
            <div class="content-wrapper d-flex align-items-center text-center error-page bg-%(bgcolor)s">
                <div class="row flex-grow-1">
                    <div class="col-lg-8 col-xl-7 mx-auto text-white">
                        <div class="row align-items-center flex-row">
                            <div class="col-lg-6 text-lg-end pe-lg-4">
                                <h1 class="mb-0">%(code)s</h1>
                            </div>
                            <div class="col-lg-6 text-lg-start ps-lg-4">
                                <h2>SORRY!</h2>
                                <h3 class="fw-light">%(detail)s</h3>
                            </div>
                        </div>
                        <div class="row mt-5">
                            <div class="col-12 text-center mt-xl-2">
                                <a class="text-white fw-semibold" href=" ">Back to home</a>
                            </div>
                        </div>
                        <div class="row mt-5">
                            <div class="col-12 mt-xl-2">
                                <p class="text-white fw-semibold text-center">Copyright &copy; 2021  All rights reserved.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''

ERROR_400_CONTEXT = {'title':'Bad Request (400)', 'code':'400', 'detail':'Internal server error!', 'bgcolor':'reddish'}
ERROR_403_CONTEXT = {'title':'Forbidden (403)', 'code':'403', 'detail':'Internal server error!', 'bgcolor':'danger'}
ERROR_404_CONTEXT = {'title':'Not Found (404)', 'code':'404', 'detail':'The page you’re looking for was not found.', 'bgcolor':'primary'}
ERROR_500_CONTEXT = {'title':'Server Error (500)', 'code':'500', 'detail':'Internal server error!', 'bgcolor':'purplish'}









def handler_400(request):
    template_name = ERROR_PAGE_TEMPLATE % ERROR_400_CONTEXT
    return HttpResponse(template_name)

def handler_403(request):
    template_name = ERROR_PAGE_TEMPLATE % ERROR_403_CONTEXT
    return HttpResponse(template_name)

def handler_404(request):
    template_name = ERROR_PAGE_TEMPLATE % ERROR_404_CONTEXT
    return HttpResponse(template_name)

def handler_500(request):
    template_name = ERROR_PAGE_TEMPLATE % ERROR_500_CONTEXT
    return HttpResponse(template_name)





def error_400(request, exception):
    template_name = ERROR_PAGE_TEMPLATE % ERROR_400_CONTEXT
    return HttpResponseBadRequest(template_name, content_type='text/html',)

def error_403(request, exception):
    template_name = ERROR_PAGE_TEMPLATE % ERROR_403_CONTEXT
    return HttpResponseForbidden(template_name, content_type='text/html',)

def error_404(request, exception):
    template_name = ERROR_PAGE_TEMPLATE % ERROR_404_CONTEXT
    return HttpResponseNotFound(template_name, content_type='text/html',)

def error_500(request):
    template_name = ERROR_PAGE_TEMPLATE % ERROR_500_CONTEXT
    return HttpResponseServerError(template_name, content_type='text/html',)





















'''

from urllib.parse import quote

from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError,
)
from django.template import Context, Engine, TemplateDoesNotExist, loader
from django.views.decorators.csrf import requires_csrf_token






def handle_no_permission(request):          # redirect 403 page to my custom page
    return render(request, 'ErrorPage/forbidden403.html')




# This can be called when CsrfViewMiddleware.process_view has not run,
# therefore need @requires_csrf_token in case the template needs
# {% csrf_token %}.
@requires_csrf_token
def page_not_found(request, exception, template_name=ERROR_404_TEMPLATE_NAME):
    """
    Default 404 handler.

    Templates: :template:`404.html`
    Context:
        request_path
            The path of the requested URL (e.g., '/app/pages/bad_page/'). It's
            quoted to prevent a content injection attack.
        exception
            The message from the exception which triggered the 404 (if one was
            supplied), or the exception class name
    """
    exception_repr = exception.__class__.__name__
    # Try to get an "interesting" exception message, if any (and not the ugly
    # Resolver404 dictionary)
    try:
        message = exception.args[0]
    except (AttributeError, IndexError):
        pass
    else:
        if isinstance(message, str):
            exception_repr = message
    context = {
        'request_path': quote(request.path),
        'exception': exception_repr,
    }
    try:
        template = loader.get_template(template_name)
        body = template.render(context, request)
        content_type = None             # Django will use 'text/html'.
    except TemplateDoesNotExist:
        if template_name != ERROR_404_TEMPLATE_NAME:
            # Reraise if it's a missing custom template.
            raise
        # Render template (even though there are no substitutions) to allow
        # inspecting the context in tests.
        template = Engine().from_string(
            ERROR_PAGE_TEMPLATE % {
                'title': 'Not Found',
                'details': 'The requested resource was not found on this server.',
            },
        )
        body = template.render(Context(context))
        content_type = 'text/html'
    return HttpResponseNotFound(body, content_type=content_type)


@requires_csrf_token
def server_error(request, template_name=ERROR_500_TEMPLATE_NAME):
    """
    500 error handler.

    Templates: :template:`500.html`
    Context: None
    """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        if template_name != ERROR_500_TEMPLATE_NAME:
            # Reraise if it's a missing custom template.
            raise
        return HttpResponseServerError(
            ERROR_PAGE_TEMPLATE % {'title': 'Server Error (500)', 'details': ''},
            content_type='text/html',
        )
    return HttpResponseServerError(template.render())


@requires_csrf_token
def bad_request(request, exception, template_name=ERROR_400_TEMPLATE_NAME):
    """
    400 error handler.

    Templates: :template:`400.html`
    Context: None
    """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        if template_name != ERROR_400_TEMPLATE_NAME:
            # Reraise if it's a missing custom template.
            raise
        return HttpResponseBadRequest(
            ERROR_PAGE_TEMPLATE % {'title': 'Bad Request (400)', 'details': ''},
            content_type='text/html',
        )
    # No exception content is passed to the template, to not disclose any sensitive information.
    return HttpResponseBadRequest(template.render())


# This can be called when CsrfViewMiddleware.process_view has not run,
# therefore need @requires_csrf_token in case the template needs
# {% csrf_token %}.
@requires_csrf_token
def permission_denied(request, exception, template_name=ERROR_403_TEMPLATE_NAME):
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        if template_name != ERROR_403_TEMPLATE_NAME:
            # Reraise if it's a missing custom template.
            raise
        return HttpResponseForbidden(
            ERROR_PAGE_TEMPLATE % {'title': '403 Forbidden', 'details': ''},
            content_type='text/html',
        )
    return HttpResponseForbidden(
        template.render(request=request, context={'exception': str(exception)})
    )
'''