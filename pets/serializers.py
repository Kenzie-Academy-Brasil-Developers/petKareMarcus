from rest_framework import serializers
from groups.models import Group
from pets.models import Seasons, Pet
from traits.models import Trait

from rest_framework.validators import UniqueValidator
import ipdb
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=Seasons.choices, default=Seasons.DEFAULT )
    # group_id = serializers.IntegerField(read_only=True)
    traits_count = serializers.SerializerMethodField()

    traits = TraitSerializer(many=True)
    group = GroupSerializer()



    def get_traits_count(self, obj:Pet):
        return obj.traits.count()


    def create(self, validated_data:dict)-> Pet:
        group_dict = validated_data.pop("group")
        group_obj, is_created = Group.objects.get_or_create(**group_dict)

        traits_list =  validated_data.pop("traits")       

        
        pet_obj = Pet.objects.create(**validated_data, group=group_obj)
        
        for trait in traits_list:
            trait_obj, is_created = Trait.objects.get_or_create(**trait)
            pet_obj.traits.add(trait_obj)
        
        
        return pet_obj

      


    def update(self, instance: Pet, validated_data: dict):
        
        group_dict = validated_data.pop("group", None)
        
        traits_list =  validated_data.pop("traits", None)
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        if group_dict:
            group_obj, is_created = Group.objects.get_or_create(**group_dict)
            instance.group = group_obj
        
        if traits_list:
            new_traits = []
            for trait in traits_list:
                trait_obj, is_created = Trait.objects.get_or_create(**trait)
                new_traits.append(trait_obj)

            instance.traits.set(new_traits)
        
        instance.save()
        
        return instance