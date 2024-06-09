# runge_kutta_app/models.py

from django.db import models

class RungeKuttaResult(models.Model):
    x_values = models.TextField()
    y_values = models.TextField()
    x0 = models.FloatField()
    y0 = models.FloatField()
    xn = models.FloatField()
    n = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Runge-Kutta Result from x0={self.x0} to xn={self.xn} with n={self.n}"
