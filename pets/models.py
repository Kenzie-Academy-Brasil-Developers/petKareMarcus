from django.db import models


class Seasons(models.TextChoices):
    FEMALE = "Female"
    MALE = "Male"
    DEFAULT = "Not informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(null=True, default=0)
    weight = models.FloatField(null=True, default=0)
    sex = models.CharField(
        max_length=20,
        choices=Seasons.choices,
        default=Seasons.DEFAULT,
        )
    
    
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        related_name="pets",
    )


    traits = models.ManyToManyField(
        "traits.Trait",
        related_name="pets",
    )

    def __repr__(self) -> str:
        return f"<Pet [{self.id}] - {self.name}>"