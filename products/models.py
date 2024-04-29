from django.db import models

YAHYOBEK, ASRORBEK, ASADBEK = ('yahyobek', "asrorbek", 'asadbek')

class Category(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Products(models.Model):
    AUTH_TYPE = (
        (YAHYOBEK,YAHYOBEK),
        (ASRORBEK, ASRORBEK),
        (ASADBEK, ASADBEK),

    )
    name = models.CharField(max_length=100, blank=False, null=False, )
    price = models.IntegerField(blank=False, null=False)
    photo = models.ImageField(upload_to='product_image/', blank=False, null=False)
    product_owner = models.CharField(max_length=50, choices=AUTH_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


