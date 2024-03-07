from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import BlogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator
from .models import Blog
from rest_framework_simplejwt.tokens import RefreshToken


class PubicView(APIView):

    def get(self,request):

        try:
            blog = Blog.objects.all().order_by('?')
            
            if request.GET.get('search'):
                search = request.GET.get('search')
                blog = blog.filter(title__icontains=search)

            page_naumber = request.GET.get('page',1)
            paginator=  Paginator(blog,2)

            serializer = BlogSerializer(paginator.page(page_naumber),many=True)

            return Response({

                "data":serializer.data,
                "message":"Your blogs fetched successfully"

            },status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({

                    "data":{},
                    "message":"something went wrong"

                },status=status.HTTP_400_BAD_REQUEST)
        
    
class BlogView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self,request):

        try:
            data = request.data
            data['user']=request.user.id
            serializer = BlogSerializer(data=data)

            if not serializer.is_valid():
                return Response({

                    "data":serializer.errors,
                    "message":"validation error"

                },status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({

                "data":serializer.data,
                "message":"blog created success fully",

            },status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({

                    "data":{},
                    "message":"something went wrong"

                },status=status.HTTP_400_BAD_REQUEST)
        

    def get(self,request):

        try:
            blog = Blog.objects.filter(user = request.user)
            
            if request.GET.get('search'):
                search = request.GET.get('search')
                blog = blog.filter(title__icontains=search)

            serializer = BlogSerializer(blog,many=True)

            return Response({

                "data":serializer.data,
                "message":"Your blogs fetched successfully"

            },status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({

                    "data":{},
                    "message":"something went wrong"

                },status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self,request):

        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get('uid'))

            if not blog.exists():
                 return Response({

                    "data":{},
                    "message":"no such blog uid"

                },status=status.HTTP_204_NO_CONTENT)
            
            if request.user != blog[0].user:
                return Response({

                    "data":{},
                    "message":"you are not autherized to do this"

                },status=status.HTTP_401_UNAUTHORIZED)
            
            serializer = BlogSerializer(blog[0],data=data,partial=True)

            if not serializer.is_valid():
                return Response({

                    "data":serializer.errors,
                    "message":"validation error"

                },status=status.HTTP_400_BAD_REQUEST)
            print(blog)
            serializer.save()

            return Response({

                "data":serializer.data,
                "message":"Your blogs updated successfully"

            },status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({

                    "data":{},
                    "message":"something went wrong"

                },status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self,request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get('uid'))

            if not blog.exists():
                    return Response({

                    "data":{},
                    "message":"no such blog uid"

                },status=status.HTTP_204_NO_CONTENT)
            
            if request.user != blog[0].user:
                return Response({

                    "data":{},
                    "message":"you are not autherized to do this"

                },status=status.HTTP_401_UNAUTHORIZED)
            
            blog.delete()
            
            return Response({

                    "data":{},
                    "message":"blog deleted success fully",

                },status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({

                    "data":{},
                    "message":"something went wrong"

                },status=status.HTTP_400_BAD_REQUEST)
        

