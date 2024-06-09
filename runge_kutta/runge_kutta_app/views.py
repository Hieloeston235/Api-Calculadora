from django.http import JsonResponse
from .models import RungeKuttaResult
import numpy as np
import json

def f(x, y):
    return 2 * x * y

def runge_kutta(x0, y0, xn, n):
    h = (xn - x0) / float(n)
    x = np.linspace(x0, xn, n + 1)
    y = np.zeros(n + 1)
    y[0] = y0
    for i in range(n):
        k1 = h * f(x[i], y[i])
        k2 = h * f(x[i] + 0.5 * h, y[i] + 0.5 * k1)
        k3 = h * f(x[i] + 0.5 * h, y[i] + 0.5 * k2)
        k4 = h * f(x[i] + h, y[i] + k3)
        y[i + 1] = y[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return x, y

def runge_kutta_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            x0 = float(data.get('x0', 0))
            y0 = float(data.get('y0', 1))
            xn = float(data.get('xn', 1))
            n = int(data.get('n', 5))
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        x, y = runge_kutta(x0, y0, xn, n)

        x_json = json.dumps(x.tolist())
        y_json = json.dumps(y.tolist())

        result = RungeKuttaResult.objects.create(
            x_values=x_json,
            y_values=y_json,
            x0=x0,
            y0=y0,
            xn=xn,
            n=n
        )

        response_data = {
            'id': result.id,
            'x': x.tolist(),
            'y': y.tolist(),
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid HTTP method. Please use POST.'}, status=405)
    

def runge_kutta_results(request):
    results = RungeKuttaResult.objects.all()
    data = []
    for result in results:
        data.append({
            'id': result.id,
            'x_values': json.loads(result.x_values),
            'y_values': json.loads(result.y_values),
            'x0': result.x0,
            'y0': result.y0,
            'xn': result.xn,
            'n': result.n,
            'created_at': result.created_at,
        })
    return JsonResponse(data, safe=False)