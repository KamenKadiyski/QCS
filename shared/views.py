from django.shortcuts import render

def custom_error_404(request, exception):
    return render(request, 'shared/404.html', status=404)

def custom_error_500(request):
    return render(request, 'shared/500.html', status=500)
