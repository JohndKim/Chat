from django.shortcuts import render
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import viewsets 
# ^^ provides crud operations i think
# viewsets is class based view w/ list + create (built in?) vs get + post (html request)
from .serializer import ServerSerializer
from .models import Server
from .schema import server_list_docs


# Create your views here.

# CLASS BASED VIEW
# creating an endpoint (location within api that accepts requests and sends response)
class ServerListViewSet(viewsets.ViewSet):
    # front end (get request) --> retrieve data about servers
    
    queryset = Server.objects.all() # collection of data from db
    
    # RETURNS LIST OF SERVERS FILTERED BY VARIOUS PARAMETERS
    @server_list_docs
    def list(self, request):
        """
        Handles a GET request to retrieve a filtered list of servers based on specified parameters.

        Args:
            request (HttpRequest): The HTTP request object containing client's request details.

        Raises:
            AuthenticationFailed: If the request requires authentication, but the user is not authenticated.
            ValidationError: If there are issues with the provided server ID or other validation errors.

        Returns:
            Response: A serialized representation of the server data in JSON format.

        Query Parameters:
            - `category` (str): Filter servers by category name.
            - `qty` (str): Limit the number of servers to be returned.
            - `by_user` (bool): Filter servers based on user membership.
            - `by_serverid` (int): Filter servers by a specific server ID.
            - `with_num_members` (bool): Include the count of members for each server.

        Usage Example:
            # In a Django ViewSet
            class ServerListViewSet(viewsets.ViewSet):
                def list(self, request):
                    # Implementation details...
        """
        # request.query_params is synonymous to .get
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # authentication to ensure user is signed in
        # if by_user or by_serverid and not request.user.is_authenticated:
        #     raise AuthenticationFailed()
        
        # running query
        if category:
            # update queryset
            self.queryset = self.queryset.filter(category__name=category)
            # access name of category
            
        # show servers the member is a part of
        if by_user:
            if by_user and not request.user.is_authenticated:
                raise AuthenticationFailed()
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)
        
        # count number of memebers
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members = Count("member"))
            
        # return number of servers to show
        if qty:
            self.queryset = self.queryset[: int(qty)]
            
        # need to know we can access the server
        if by_serverid:
            if by_serverid and not request.user.is_authenticated:
                    raise AuthenticationFailed()
            # if server DNE or unavailable
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_serverid} not found")
            except ValueError:
                raise ValidationError(detail=f"Server with id {by_serverid} value error")
                
                
         
        
            
            
        # convert queryServerSerializer
        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})        
        return Response(serializer.data)
    