from django.test import TestCase
from lists.models import Item

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        first_item_text = 'A new list item'
        data = {'item_text': first_item_text}

        response = self.client.post('/', data=data)
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, first_item_text)

    def test_redirects_after_POST(self):
        first_item_text = 'A new list item'
        data = {'item_text': first_item_text}
        response = self.client.post('/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/only-list/')

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

class ListViewTest(TestCase):
    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/only-list/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2') 
    def test_uses_list_template(self):
        response = self.client.get('/lists/only-list/')
        self.assertTemplateUsed(response, 'list.html')