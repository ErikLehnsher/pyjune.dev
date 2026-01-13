from rest_framework import serializers
from  posts.models import Post, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
    
    
        


class PostListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'author_username',
            'category',
            'tags',
            'created_at',
        ]



class PostDetailSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True) 

    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'slug',
            'title',
            'slug',
            'excerpt',
            'html_content',
            'author_username',
            'category',
            'tags',
            'created_at',
            'updated_at',
        ]



class PostCreateUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True) 
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        required=False,
        allow_null=True
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        many=True,
        required=False
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'category_id',
            'tag_ids',
            'content_json',   # 👈 editor.getJSON()
            'html_content',   # 👈 editor.getHTML()
            'status',
            'is_published',
        ]
