import math
from decimal import Decimal

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from .models import RoofMaterial
from .serializers import RoofMaterialSerializer


class IsSuperUserOrAUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or (request.user.is_authenticated and request.user.user_role == 'A')


class IsSuperUserOrARole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or (request.user.is_authenticated and request.user.user_role == 'A')

class RoofMaterialViewSet(viewsets.ModelViewSet):
    queryset = RoofMaterial.objects.all()
    serializer_class = RoofMaterialSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='type',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=['p', 's', 'm'],
                required=False,
                description="Filter materials by type (Profnastil, Shifer, Metall)."
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        roof_type = request.query_params.get('type')
        if roof_type:
            queryset = queryset.filter(type=roof_type)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_role != 'A':
            return Response({"error": "Only superuser or user_role='A' can perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_role != 'A':
            return Response({"error": "Only superuser or user_role='A' can perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_role != 'A':
            return Response({"error": "Only superuser or user_role='A' can perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_role != 'A':
            return Response({"error": "Only superuser or user_role='A' can perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)



@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'A': openapi.Schema(type=openapi.TYPE_NUMBER),
            'B': openapi.Schema(type=openapi.TYPE_NUMBER),
            'C': openapi.Schema(type=openapi.TYPE_NUMBER),
            'D': openapi.Schema(type=openapi.TYPE_NUMBER),
            'E': openapi.Schema(type=openapi.TYPE_NUMBER),
            'F': openapi.Schema(type=openapi.TYPE_NUMBER),
            'G': openapi.Schema(type=openapi.TYPE_NUMBER),
            'H': openapi.Schema(type=openapi.TYPE_NUMBER),
            'material_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'materilal_id']
    ),
    responses={
        200: openapi.Response(
            description="Material calculation response",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
            )
        ),
        400: "Bad Request"
    },
)
@api_view(['POST'])
def calculate_roof_p(request):
    """
    Calculate the required material for a given roof.

    ![Roof Image](/static/img.png)

    This API endpoint calculates the amount of material needed for a roof based on its dimensions and the selected material type.
    """
    # Assuming the dimensions of the roof and the selected material type are sent in the POST request
    A = Decimal(request.data.get('A'))
    B = Decimal(request.data.get('B'))
    C = Decimal(request.data.get('C'))
    D = Decimal(request.data.get('D'))
    E = Decimal(request.data.get('E'))
    F = Decimal(request.data.get('F'))
    G = Decimal(request.data.get('G'))
    H = Decimal(request.data.get('H'))

    material_id = request.data.get('material_id')


    try:
        material = RoofMaterial.objects.get(pk=material_id)
    except RoofMaterial.DoesNotExist:
        return JsonResponse({'error': 'Material not found'}, status=400)

    if A <= G+H or B <= C+D+E+F:
        return JsonResponse({'error': 'Not valid sides'}, status=400)

    if material.type == 's':
        g_side = math.ceil(G / material.height_m)
        h_side = math.ceil(H / material.height_m)
        c_side = math.ceil(C / material.height_m)
        d_side = math.ceil(D / material.height_m)
        e_side = math.ceil(E / material.height_m)
        f_side = math.ceil(F / material.height_m)

        c_count = math.ceil(A / material.width_m) * c_side
        d_count = math.ceil((A - G) / material.width_m) * d_side
        e_count = math.ceil((A - G) / material.width_m) * e_side
        f_count = math.ceil(A / material.width_m) * f_side
        g_count = math.ceil(B / material.width_m) * g_side
        h_count = math.ceil((B - C - F) / material.width_m) * h_side

        all_count = sum([c_count, g_count, f_count, h_count, d_count, e_count])
        overall_price = all_count * material.price

        sides = [
            {
                "quantity": all_count,
                "height_meter": material.height_m,
                "price": overall_price
            },
        ]


    else:
        c_f_side_count = math.ceil(A / material.width_m)
        d_e_side_count = math.ceil(A-G / material.width_m)
        h_side_count = math.ceil((B - C - F) / material.width_m)
        g_side_count = math.ceil(B / material.width_m)
        sides = [
            {
                "quantity": c_f_side_count,
                "height_meter": C,
                "price": ((C * material.width_m) * material.price) * c_f_side_count
            },
            {
                "quantity": c_f_side_count,
                "height_meter": F,
                "price": ((F * material.width_m) * material.price) * c_f_side_count
            },
            {
                "quantity": d_e_side_count,
                "height_meter": D,
                "price": ((D * material.width_m) * material.price) * d_e_side_count
            },
            {
                "quantity": d_e_side_count,
                "height_meter": E,
                "price": ((E * material.width_m) * material.price) * d_e_side_count
            },
            {
                "quantity": h_side_count,
                "height_meter": H,
                "price": ((H * material.width_m) * material.price) * h_side_count
            },
            {
                "quantity": g_side_count,
                "height_meter": G,
                "price": ((G * material.width_m) * material.price) * g_side_count
            }
        ]

        overall_price = sum(x['price'] for x in sides)

    response_data = {
        "material_title": material.title,
        "material_type": material.type,
        "material_width": material.width_m,
        "sides": sides,
        "overall_price": overall_price,
    }

    # Return the response
    return JsonResponse(response_data)
