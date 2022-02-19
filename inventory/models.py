from django.db import models
import uuid   
import secrets
import string

class StockCategory(models.Model):
    category = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
	    return self.category


def create_unique_id():
    res = ''.join(secrets.choice( string.digits) for i in range(12))
    return res


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    category = models.ForeignKey('StockCategory', blank= True, null = True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=15, unique=True, editable=False)
    sell_price = models.IntegerField(default=599)
    quantity = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.code


    def save(self, *args, **kwargs):
        if not self.pk: 
            code = create_unique_id()
            unique = False
            while not unique:
                if not Stock.objects.filter(code=code).exists():
                    unique = True
                    self.code = code
                else:
                    print('clashed')
                    code = create_unique_id()
        super(Stock, self).save(*args, **kwargs)