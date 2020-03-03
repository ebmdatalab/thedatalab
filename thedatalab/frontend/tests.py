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
            
        self.about_page = Page.objects.create(
            parent=self.home_page,
            slug='about-us',
            body="Test content x93idd02o"
            )
        
        self.project = Project.objects.create(
            parent=self.home_page,
            menu_title='Pond project',
            topics = ['ducks'],
            colour_scheme='orange',
            )

        # work around tagulous bug
        self.project.topics.save()
        
    def test_page_rendering(self):
        content = self.client.get('/about-us/').content.decode('utf-8')
        
        # Check that our sentinel body string is in the page somewhere
        assert 'x93idd02o' in content
        
        # Check that the footer is present
        assert '<img src="/static/images/logos/nhs-england.png" />' in content
        
    def test_paper_rendering(self):
        content = self.client.get('/papers/%d/'%self.paper.id).content.decode('utf-8')
        
        # Check that the paper title appears in the page somewhere
        assert self.paper.title in content
        
        # Check that the citation appears in the page somewhere
        assert self.paper.citation in content
        
    def test_author_rendering(self):
        content = self.client.get('/authors/%s/'%self.author_1.slug).content.decode('utf-8')
        
        # Check that the institution appears in the page somewhere
        assert self.author_1.institution in content
        
    def test_colour_scheme(self):
        # The paper is linked to an orange project via a shared topic (ducks)
        assert self.paper.get_colour_scheme()=="orange"

    
