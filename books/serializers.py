from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Book

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'content', 'subtitle', 'author', 'isbn', 'price',)


# class BookSerializer(serializers.Serializer): #ozimiz yozgan serilayzer. tepadagi esa modelserialer
#     title = serializers.CharField(max_length=200)
#     content = serializers.CharField()
#     subtitle = serializers.CharField()


    def validate(self, data):
        title = data.get('title', None)
        author = data.get('author', None)

        # check title if it contains only alphabetical chars
        if not title.isalpha():
            raise ValidationError(
            {
                'status': False,
                'message': 'Kitobni sarlavhasi harflardan tashkil topgan bo\'lishi kerak!'
            })

        # check title and author from database existance
        if Book.objects.filter(title=title, author=author).exist():
            raise ValidationError(
                {
                    'status': False,
                    'message': 'Kitobni sarlavhasi va muallifi bir xil bo\'lgan kitobni yuklay olmaysiz'
                })
        return data

    def validate_price(self, price):
        if price < 0 or price > 99999999:
            raise ValidationError(
                {
                    'status': False,
                    'message': 'Narx noto\'g\'ri kiritilgan.'
                }
            )