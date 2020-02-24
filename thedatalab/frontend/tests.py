from django.test import TestCase
from thedatalab.frontend.models import *

class ThingTestCase(TestCase):
    def setUp(self):
        self.author_1 = Author.objects.create(
            name="Author One",
            institution="University of One",
            )
        self.author_2 = Author.objects.create(
            name="Author Two",
            institution="University of Two",
            )

        self.paper = Paper.objects.create(
            title="Test paper",
            description="A paper to test the system",
            citation="CITATION",
            topics = ['ducks', 'sheep'],
            )
        self.paper.authors.set([self.author_1, self.author_2])
        
        #tagulous is buggy and doesn't handle multi-table inheritance very well - it misses save events on the model so needs forcibly saving
        self.paper.topics.save()
        
        self.home_page = Page.objects.create(
            menu_title = "Home"
            )
        
        self.project = Project.objects.create(
            parent=self.home_page,
            menu_title='Pond project',
            topics = ['ducks'],
            colour_scheme='orange',
            )

        # work around tagulous bug
        self.project.topics.save()
        

    def test_colour_scheme(self):
        # The paper is linked to an orange project via a shared topic (ducks)
        assert self.paper.get_colour_scheme()=="orange"

    
