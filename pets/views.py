from rest_framework.views import APIView, Response, Request, status
from django.forms.models import model_to_dict
from .models import Pet

import ipdb
from django.shortcuts import get_object_or_404
from .serializers import PetSerializer
from django.shortcuts import get_list_or_404


class PetView(APIView):
    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()

        
        serializer = PetSerializer(pets, many=True)


        return Response(serializer.data)
    

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        # pet = Pet.objects.create(**serializer.validated_data)

        # serializer = PetSerializer(pet)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)



class PetDetailView(APIView):

    def get(self, request: Request, pet_id: int) -> Response:
               
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)


        return Response(serializer.data)
    

    def delete(self, request: Request, pet_id: int) -> Response:
               
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()


        return Response(status=status.HTTP_204_NO_CONTENT)

    
    def patch(self, request: Request, pet_id: int) -> Response:
        
        pet = get_object_or_404(Pet, pk=pet_id)
        
        serializer = PetSerializer(pet, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

       

        serializer.save()


        return Response(serializer.data, status.HTTP_200_OK)