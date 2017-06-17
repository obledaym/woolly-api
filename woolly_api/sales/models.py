from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Sum


class Association(models.Model):
    """
    Represents the association information
    """
    name = models.CharField(max_length=200)
    bank_account = models.CharField(max_length=30)
    # The foundation ID is used to  link the app to NemoPay
    # No calculations are going to be made with it
    # So it's a char field
    foundation_id = models.CharField(max_length=30)

    class JSONAPIMeta:
        resource_name = "associations"


class PaymentMethod(models.Model):
    """Define the payment options"""
    name = models.CharField(max_length=200)
    api_url = models.CharField(max_length=500, blank=True)

    class JSONAPIMeta:
        resource_name = "paymentmethods"


class Sale(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    creation_date = models.DateField(auto_now_add=True)
    begin_date = models.DateField()
    end_date = models.DateField()
    max_payment_date = models.DateField()
    # max_item_quantity = models.IntegerField()

    paymentmethods = models.ForeignKey(
        PaymentMethod,
        on_delete=None,
        related_name='sales',
        blank=True)

    association = models.ForeignKey(
        Association, on_delete=None, related_name='sales', blank=True)

    class JSONAPIMeta:
        resource_name = "sales"


# class ItemGroup(models.Model):
# name = models.CharField(max_length=200)


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    initial_quantity = models.IntegerField()
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE, related_name='items')

    class JSONAPIMeta:
        resource_name = "items"

    def remaining(self, woollyusertype):
        """
        Return the remaining items, using the minimum between initial_quantity of the item minus the sold items,
        the quantity of the item_group minus the sold items of this group and the quantity of the itemspecification for
        the woollyusertype and the sold items for this usertype

        :param woollyusertype: The type of the user to check the remaining quantity
        :return: The number of remaining items for this woollyusertype
        :raise: ValidationError if the item is not in db yet or if the corresponding WoollyUserType has no access to this
        item (no corresponding ItemSpecification for his type)
        """
        if self.pk == None:
            raise ValidationError('Primary key not set')

        # No itemspecifications corresponding to this user type
        if len(ItemSpecifications.objects.filter(woolly_user_type=woollyusertype, item__pk=self.pk)) == 0:
            raise ValidationError('This UserType does not have access to his item')

        # Simple condition on the initial item quantity
        sold_quantity = OrderLine.objects.filter(item=self).aggregate(Sum('quantity'))
        sold = sold_quantity.get('quantity__sum') if sold_quantity.get('quantity__sum') is not None else 0
        remaining = self.initial_quantity - sold

        # Complex condition using the user type and the quantity in the corresponding itemspecification
        sold_quantity = OrderLine.objects.filter(order__owner__type=woollyusertype, item=self).aggregate(Sum('quantity'))
        sold = sold_quantity.get('quantity__sum') if sold_quantity.get('quantity__sum') is not None else 0
        initial = ItemSpecifications.objects.get(item=self, woolly_user_type=woollyusertype).quantity
        remaining = initial - sold if initial - sold < remaining else remaining

        return remaining

class ItemSpecifications(models.Model):
    woolly_user_type = models.ForeignKey(
        'authentication.WoollyUserType', on_delete=models.CASCADE, related_name='itemspecifications')
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='itemspecifications')
    quantity = models.IntegerField()
    price = models.FloatField()
    nemopay_id = models.CharField(max_length=30)

    class JSONAPIMeta:
        resource_name = "itemspecifications"


class AssociationMember(models.Model):
    woollyUser = models.ForeignKey(
        'authentication.WoollyUser', on_delete=models.CASCADE, related_name='associationmembers')
    association = models.ForeignKey(
        Association, on_delete=models.CASCADE, related_name='associationmembers')
    role = models.CharField(max_length=50)
    rights = models.CharField(max_length=50)

    class JSONAPIMeta:
        resource_name = "associationmembers"


class Order(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='orders',
        on_delete=models.CASCADE)

    status = models.CharField(max_length=50)
    date = models.DateField()

    class JSONAPIMeta:
        resource_name = "orders"


class OrderLine(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='orderlines')
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='orderlines')
    quantity = models.IntegerField()

    class JSONAPIMeta:
        resource_name = "orderlines"
