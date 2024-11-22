from rest_framework import serializers
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions, Wishlist # , RentHouseLoan, UserProduct

class DepositProductsSerializer(serializers.ModelSerializer) :
    class Meta:
        model = DepositProducts
        fields = '__all__'

class DepositOptionsSerializer(serializers.ModelSerializer) :
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('product',)

class DepositProductWithOptionSerialzier(serializers.ModelSerializer):
    class OptionForDepositSerializer(serializers.ModelSerializer):
        class Meta:
            model = DepositOptions
            fields = '__all__'
    
    options = OptionForDepositSerializer(many=True, source='depositoptions_set')

    class Meta:
        model = DepositProducts
        fields = '__all__'


class SavingProductsSerializer(serializers.ModelSerializer) :
    class Meta:
        model = SavingProducts
        fields = '__all__'

class SavingOptionsSerializer(serializers.ModelSerializer) :
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('product',)

class SavingProductWithOptionSerialzier(serializers.ModelSerializer):
    class OptionForSavingSerializer(serializers.ModelSerializer):
        class Meta:
            model = SavingOptions
            fields = '__all__'
    
    options = OptionForSavingSerializer(many=True, source='savingoptions_set')

    class Meta:
        model = SavingProducts
        fields = '__all__'
 

class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'
        read_only_fields = ('user',)
