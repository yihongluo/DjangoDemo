from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class Person(models.Model):
    class Meta:
        app_label = "codekeeper"
        verbose_name_plural = "people"

    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0}, {1}".format(self.last_name, self.first_name)

    @property
    def full_name(self):
        return "{0}, {1}".format(self.first_name,self.last_name)

@receiver(post_save, sender=Person)
def solr_index(sender, instance, created, **kwargs):
    import uuid 
    from django.conf import settings
    import scorched

    solrconn = scorched.SolrInterface(settings.SOLR_SERVER)
    
    #check if it already exists
    records = solrconn.query(type="person", item_id="{0}".format(instance.pk)).execute()
    if records:
        #delete first. then add
        solrconn.delete_by_ids([x['id'] for x in records])

    d = {
        'id': str(uuid.uuid4()),
        'type': 'person',
        'item_id': instance.pk,
        'person': instance.snippet,
        'first_name': instance.first_name
    }

    solrconn.add(d)
    solrconn.commit()

@receiver(post_delete, sender=Person)
def solr_delete(sender, instance, created, **kwargs):
    from django.conf import settings
    import scorched

    solrconn = scorched.SolrInterface(settings.SOLR_SERVER)
    records = solrconn.query(type="person", item_id="{0}".format(instance.pk)).execute()
    solrconn.delete_by_ids([x['id'] for x in records])
    solrconn.commit()
      