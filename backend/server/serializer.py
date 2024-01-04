from rest_framework import serializers
from .models import Category, Server, Channel

class ChannelSerializer(serializers.ModelSerializer):
    # meta is reusable validator that is applied on complete set of field data
    class Meta:
        model = Channel
        fields = "__all__"

class ServerSerializer(serializers.ModelSerializer):
    # derive value using annotate
    num_members = serializers.SerializerMethodField()
    # shows all the channels in the server
    channel_server = ChannelSerializer(many=True) 
    
    
    class Meta:
        model = Server
        exclude = ("member", )
        # fields = "__all__"
        
    # runs this function whenever it tries to find what run_members is
    def get_num_members(self, obj):
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None
    
    # representation of serializer
    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get("num_members") # use key to get data with_num_members
        
        if not num_members: #if true not passed in
            data.pop("num_members", None)
        return data