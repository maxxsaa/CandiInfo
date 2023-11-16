from django.db import models

# Create your models here.

class User(models.Model):

    email= models.EmailField(max_length=30)
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'X'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    gerant = models.BooleanField()
    clientde = models.ForeignKey('Lieu',on_delete=models.CASCADE, null=True)
    positif = models.BooleanField(null=True)
    DateTest= models.DateField(null=True)
    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Lieu(models.Model):
    name= models.CharField(max_length=30)
    capacity=models.IntegerField()
    PROVIRUS_CHOICES = (
        ('Provirus', 'Provirus'),
        ('Antivirus', 'Antivirus')
    )
    provirus = models.CharField(max_length=10, choices=PROVIRUS_CHOICES)
    proprietaire = models.ForeignKey('User', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class Reservation(models.Model):
    nombre= models.IntegerField()
    lieu = models.ForeignKey('Lieu', on_delete=models.CASCADE)
    date = models.DateField(null=True)
    personne = models.ForeignKey('User', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.lieu} {self.date}"
