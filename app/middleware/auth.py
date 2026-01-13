from django.shortcuts import redirect

def auth_middleware(get_response):
    def middleware(request):
        # Pages that don't require login
        free_urls = ['/login/', '/signup/', '/admin/']  # add more if needed

        if request.path not in free_urls:
            print(request.session.get('customer'))
            if not request.session.get('customer'):
                return redirect('login')
        
        return get_response(request)
    return middleware
