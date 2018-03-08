from django.test import TestCase
from lists.models import Item, List

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        first_item = Item()
        first_text = 'The first (ever) list item'
        first_item.text = first_text
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_text = "Item the second"
        second_item.text = second_text
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, first_text)
        self.assertEqual(saved_items[1].text, second_text)

        self.assertEqual(saved_items[0].list, list_)
        self.assertEqual(saved_items[1].list, list_)


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        first_item_text = 'A new list item'
        data = {'item_text': first_item_text}

        response = self.client.post('/lists/new', data=data)
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, first_item_text)

    def test_redirects_after_POST(self):
        first_item_text = 'A new list item'
        data = {'item_text': first_item_text}
        response = self.client.post('/lists/new', data=data)
        self.assertRedirects(response, '/lists/only-list/')


class ListViewTest(TestCase):
    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get('/lists/only-list/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2') 
    def test_uses_list_template(self):
        response = self.client.get('/lists/only-list/')
        self.assertTemplateUsed(response, 'list.html')