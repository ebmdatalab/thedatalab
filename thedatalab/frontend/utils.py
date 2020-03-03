from django.http import Http404

from . import models

def page_resolve(*args, **kwargs):
    """
    Decorator to find a CMS page corresponding to the current URL and add it to the request object.
    
    If `strict` is `True` only match the exact URL, if `False` then find the the page matching the longest prefix of the URL.
    
    """
    strict = kwargs.get("strict", True)
    
    def arged_func(func):
        def inner_func(request, *args, **kwargs):
            root = models.Page.objects.filter(url='', level=0).first()
            
            def find_page(p):
                return root.get_descendants(include_self=True).filter(url=p).first()
            
            if request.path=='/':
                page = root
            else:
                path = request.path.rstrip('/')
                page = find_page(path)
            
            #if node is None and not path.endswith("/"):
            #	n = find_node(path + "/")
            #	if n: return HttpResponseRedirect('/' + n.url)

            exact = True
            while page is None and not strict:
                exact = False
                
                path = path.rsplit("/", 1)[0]
                page = find_page(path)

            if page is None:
                raise Http404()
            
            request.root = root
            request.page = page
            
            return func(request, *args, **kwargs)
        return inner_func

    if len(args)!=1 or not callable(args[0]):
        return arged_func
    
    return arged_func(args[0])
