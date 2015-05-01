from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class Language(models.Model):
    class Meta:
        app_label = "codekeeper"

    name = models.CharField(max_length = 128)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0}".format(self.name)

@receiver(post_save, sender=Language)
def solr_index(sender, instance, created, **kwargs):
    import uuid 
    from django.conf import settings
    import scorched

    solrconn = scorched.SolrInterface(settings.SOLR_SERVER)
    
    #check if it already exists
    records = solrconn.query(type="language", item_id="{0}".format(instance.id)).execute()
    if records:
        #delete first. then add
        solrconn.delete_by_ids([x['id'] for x in records])

    d = {
        'id': str(uuid.uuid4()),
        'type': 'language',
        'item_id': instance.id,
        'name': instance.name,
    }

    solrconn.add(d)
    solrconn.commit()

@receiver(post_delete, sender=Language)
def solr_delete(sender, instance, created, **kwargs):
    from django.conf import settings
    import scorched

    solrconn = scorched.SolrInterface(settings.SOLR_SERVER)
    records = solrconn.query(type="language", item_id="{0}".format(instance.id)).execute()
    solrconn.delete_by_ids([x['id'] for x in records])
    solrconn.commit()
