from datetime import datetime

def greeting(request):
    hour = datetime.now().hour
    if hour < 12:
        g = 'Morning'
    elif hour < 17:
        g = 'Afternoon'
    else:
        g = 'Evening'
    return {'greeting': g}
