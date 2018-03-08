from django.test import TestCase
from lists.models import Item

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        data = {'item_text': 'A new list item'}
        response = self.client.post('/', data=data)
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_text = 'The first (ever) list item'
        first_item.text = first_text
        first_item.save()

        second_item = Item()
        second_text = "Item the second"
        second_item.text = second_text
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, first_text)
        self.assertEqual(saved_items[1].text, second_text)