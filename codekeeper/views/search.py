from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from codekeeper.serializers.search import SearchSerializer
from codekeeper.renderers.custom_html_renderer import CustomHTMLRenderer

class SearchViewHTMLRenderer(CustomHTMLRenderer):
    template_name = "search/search.html"

class SearchView(GenericAPIView):
    serializer_class = SearchSerializer
    renderer_class = (JSONRenderer, SearchViewHTMLRenderer)

    def get(self, request, *args, **kwargs):
        querydict = request.GET
        if not querydict:
            return Response({"results": []})

        import pdb
        pdb.set_trace()

        solrconn = scorched.SolrInterfaace(settings.SOLR_SERVER)
        resp = solrconn.query(title=querydict.get('q')).execute()

        result = {'results': querydict}
        return Response(result)

    #   s = SolrSearch(request)
    #   s.search()
    #   result = {'results': search_results}
    #   response = Response(result)
    #   return response 


