from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count as DbCount
from django.utils import timezone
from .models import OrderManagement
from project_management.models import ProjectManagement
from cases.models import Case
from .serializers import OrderManagementSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

token_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description='Token authentication. Example: "Token your-token-here"',
    type=openapi.TYPE_STRING,
    required=True
)



class OrderManagementViewSet(viewsets.ModelViewSet):
    queryset = OrderManagement.objects.all()
    serializer_class = OrderManagementSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
    
    @swagger_auto_schema(
        operation_description="Create a new donation order",
        manual_parameters=[token_param],
        request_body=OrderManagementSerializer
    )
    def create(self, request, *args, **kwargs):
        """Create a new donation order"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            serializer.validated_data['payment_status'] = 'completed'
            self.perform_create(serializer)
            
            donation = serializer.instance
            total_donations = None
            
            if donation.project:
                total_donations = self._get_project_donations_summary(donation.project.pk)
            elif donation.case:
                total_donations = self._get_case_donations_summary(donation.case.pk)
            
            response_data = serializer.data
            response_data.update({
                'total_donations': total_donations,
                'donation_timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            headers = self.get_success_headers(serializer.data)
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        operation_description="List all donation orders",
        manual_parameters=[token_param]
    )
    def list(self, request, *args, **kwargs):
        """List all donation orders"""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description="Retrieve a specific donation order",
        manual_parameters=[token_param]
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific donation order"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

    def _get_project_donations_summary(self, project_id):
        """Helper method to get project donations summary"""
        try:
            project = ProjectManagement.objects.get(pk=project_id)
            donations = OrderManagement.objects.filter(
                project=project,
                payment_status='completed'
            )
            
            total = donations.aggregate(
                total_amount=Sum('donation_amount'),
                total_donors=DbCount('sender_name', distinct=True)
            )
            
            return {
                'amount': float(total['total_amount'] or 0),
                'currency': 'SAR',
                'donor_count': total['total_donors'],
                'project_id': project.pk,
                'project_name': project.project_name,
                'last_updated': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except ProjectManagement.DoesNotExist:
            return {
                'amount': 0,
                'currency': 'SAR',
                'donor_count': 0,
                'project_id': project_id,
                'error': 'Project not found'
            }
        except Exception as e:
            return {
                'amount': 0,
                'currency': 'SAR',
                'donor_count': 0,
                'project_id': project_id,
                'error': str(e)
            }

    def _get_case_donations_summary(self, case_id):
        """Helper method to get case donations summary"""
        try:
            case = Case.objects.get(pk=case_id)
            donations = OrderManagement.objects.filter(
                case=case,
                payment_status='completed'
            )
            
            total = donations.aggregate(
                total_amount=Sum('donation_amount'),
                total_donors=DbCount('sender_name', distinct=True)
            )
            
            return {
                'amount': float(total['total_amount'] or 0),
                'currency': 'SAR',
                'donor_count': total['total_donors'],
                'case_id': case.pk,
                'case_name': case.case_name,
                'last_updated': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Case.DoesNotExist:
            return {
                'amount': 0,
                'currency': 'SAR',
                'donor_count': 0,
                'case_id': case_id,
                'error': 'Case not found'
            }
        except Exception as e:
            return {
                'amount': 0,
                'currency': 'SAR',
                'donor_count': 0,
                'case_id': case_id,
                'error': str(e)
            }

    @swagger_auto_schema(
        operation_description="Get all donations for all projects or a specific project",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description='Token authentication. Example: "Token your-token-here"',
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'project_id',
                openapi.IN_QUERY,
                description='Optional project ID to filter donations',
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def project_donations(self, request):
        """Get all donations for all projects or a specific project"""
        project_id = request.query_params.get('project_id')

        try:
            if not project_id:
                # Return all project donations grouped by project
                projects = ProjectManagement.objects.all()
                result = []
                
                for project in projects:
                    donations = OrderManagement.objects.filter(
                        project=project,
                        payment_status='completed'
                    ).order_by('-created_date')
                    
                    if donations.exists():
                        serializer = self.get_serializer(donations, many=True)
                        summary = self._get_project_donations_summary(project.pk)
                        
                        result.append({
                            'project_id': project.pk,
                            'project_name': project.project_name,
                            'summary': summary,
                            'donations': serializer.data
                        })
                
                return Response(result)
            else:
                project = ProjectManagement.objects.get(pk=project_id)
                donations = OrderManagement.objects.filter(
                    project=project,
                    payment_status='completed'
                ).order_by('-created_date')
                
                serializer = self.get_serializer(donations, many=True)
                summary = self._get_project_donations_summary(project_id)
                
                return Response({
                    'project_id': project.pk,
                    'project_name': project.project_name,
                    'summary': summary,
                    'donations': serializer.data
                })

        except ProjectManagement.DoesNotExist:
            return Response(
                {"error": f"Project with id {project_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description="Get all donations for all cases or a specific case",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description='Token authentication. Example: "Token your-token-here"',
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'case_id',
                openapi.IN_QUERY,
                description='Optional case ID to filter donations',
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def case_donations(self, request):
        """Get all donations for all cases or a specific case"""
        case_id = request.query_params.get('case_id')

        try:
            if not case_id:
                # Return all case donations grouped by case
                cases = Case.objects.all()
                result = []
                
                for case in cases:
                    donations = OrderManagement.objects.filter(
                        case=case,
                        payment_status='completed'
                    ).order_by('-created_date')
                    
                    if donations.exists():
                        serializer = self.get_serializer(donations, many=True)
                        summary = self._get_case_donations_summary(case.pk)
                        
                        result.append({
                            'case_id': case.pk,
                            'case_name': case.case_name,
                            'summary': summary,
                            'donations': serializer.data
                        })
                
                return Response(result)
            else:
                case = Case.objects.get(pk=case_id)
                donations = OrderManagement.objects.filter(
                    case=case,
                    payment_status='completed'
                ).order_by('-created_date')
                
                serializer = self.get_serializer(donations, many=True)
                summary = self._get_case_donations_summary(case_id)
                
                return Response({
                    'case_id': case.pk,
                    'case_name': case.case_name,
                    'summary': summary,
                    'donations': serializer.data
                })

        except Case.DoesNotExist:
            return Response(
                {"error": f"Case with id {case_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )