from django.test import TestCase
from django.core.exceptions import ValidationError
from sales.models import Item, OrderLine, Order, ItemSpecifications, Association, Sale, PaymentMethod
from authentication.models import WoollyUserType, WoollyUser
import datetime

class ItemTestCase(TestCase):
    ITEM_QUANTITY = 100
    ITEM_EXTERNAL_QUANTITY = 50
    COTISANT_USER_TYPE = WoollyUserType.objects.get(name=WoollyUserType.COTISANT)
    EXTE_USER_TYPE = WoollyUserType.objects.get(name=WoollyUserType.EXTERIEUR)
    def setUp(self):
        # init user types if not done before
        try:
            WoollyUserType.init_values()
        except:
            pass

        # init users
        WoollyUser.objects.create_user(WoollyUserType.COTISANT, None, woollyusertype=self.COTISANT_USER_TYPE)
        WoollyUser.objects.create_user(WoollyUserType.EXTERIEUR, None, woollyusertype=self.EXTE_USER_TYPE)

        # init sale
        asso = Association.objects.create(name='sdf')
        pay = PaymentMethod.objects.create(name='card')
        sale = Sale.objects.create(name='sdf', begin_date=datetime.datetime.now(), end_date=datetime.datetime.now(),
                                   max_payment_date=datetime.datetime.now(), association=asso, paymentmethods=pay)

        # init item for test_remaining_quantity_sum_orderlines_quantities
        item_test1 = Item.objects.create(name='test1', initial_quantity=self.ITEM_QUANTITY, sale=sale)
        ItemSpecifications.objects.create(woolly_user_type=self.COTISANT_USER_TYPE,
                                          item=item_test1, quantity=self.ITEM_QUANTITY, price=0)

        # init item for test_remaining_quantity_sum_itemspecs_quantities
        item_test2 = Item.objects.create(name='test2', initial_quantity=self.ITEM_QUANTITY, sale=sale)
        ItemSpecifications.objects.create(woolly_user_type=self.EXTE_USER_TYPE,
                                          item=item_test2, quantity=self.ITEM_EXTERNAL_QUANTITY, price=0)

    def test_remaining_quantity_sum_orderlines_quantities(self):
        """
        Test if the Item.remaining() function is returning the right value when checking against the item initial_quantity
        """
        # delete all previously created orders
        Order.objects.all().delete()
        OrderLine.objects.all().delete()

        order = Order.objects.create(owner=WoollyUser.objects.get(login=WoollyUserType.COTISANT), date=datetime.datetime.now())
        item = Item.objects.get(name='test1')

        for ii in range(0, self.ITEM_QUANTITY*2):
            remaining = item.remaining(self.COTISANT_USER_TYPE)
            should_remain = self.ITEM_QUANTITY - ii
            assert (remaining == should_remain), 'Item.remaining() returns ' + str(remaining)+ ' instead of ' + \
                                                str(should_remain)
            OrderLine.objects.create(order=order, item=item, quantity=1)

        # delete all created orders for next tests
        Order.objects.all().delete()
        OrderLine.objects.all().delete()

    def test_remaining_quantity_sum_itemspecs_quantities(self):
        """
        Test if the Item.is_left() function is returning the right value when checking against the initial quantity for
        a specific WoollyUserType
        """
        # delete all previously created orders
        Order.objects.all().delete()
        OrderLine.objects.all().delete()

        order_exterieur = Order.objects.create(owner=WoollyUser.objects.get(login=WoollyUserType.EXTERIEUR),
                                              date=datetime.datetime.now())
        item = Item.objects.get(name='test2')

        # wrong type
        try:
            item.remaining(self.COTISANT_USER_TYPE)
        except ValidationError:
            pass
        else:
            assert(False), 'Item.remaining() accepts a usertype wich does not have access to the sale'


        for ii in range(0, self.ITEM_EXTERNAL_QUANTITY*2):
            remaining = item.remaining(self.EXTE_USER_TYPE)
            should_remain = ItemSpecifications.objects.get(woolly_user_type=self.EXTE_USER_TYPE, item=item).quantity - ii
            assert (remaining == should_remain), 'Item.remaining() returns ' + str(remaining) + ' instead of ' + \
                                                 str(should_remain)
            OrderLine.objects.create(order=order_exterieur, item=item, quantity=1)

        # delete all created orders for next tests
        Order.objects.all().delete()
        OrderLine.objects.all().delete()