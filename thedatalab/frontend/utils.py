from django.http import Http404

from . import models

def page_resolve(*args, **kwargs):
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

            #exact = True
            #while node is None and not strict:
            #	exact = False
            #	path = ("/".join(path.strip("/").split("/")[:-1]) + "/").lstrip("/")
            #	node = find_node(path)

            if page is None:
                raise Http404()
            
            request.root = root
            request.page = page
            
            return func(request, *args, **kwargs)
        return inner_func

    if len(args)!=1 or not callable(args[0]):
        return arged_func
    
    return arged_func(args[0])
