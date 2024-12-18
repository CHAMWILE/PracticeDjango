import json
import graphene
from graphene_federation import key, external, extend


@key(fields='id')
class ResponseObject(graphene.ObjectType):
    id = graphene.String()
    status = graphene.Boolean()
    code = graphene.Int()
    message = graphene.String()

    def __read_code_file(code_id):
        file = open('project_assets/project_assets_response_code.json', 'r')
        file_codes = file.read()
        response_codes = json.loads(file_codes)
        response_code = next(code for code in response_codes if code["id"] == code_id)
        return response_code
    
    def get_response(id):
        # try:

            response_code = ResponseObject.__read_code_file(id)
            return ResponseObject(
                response_code['id'],
                response_code['status'],
                response_code['code'],
                response_code['message'],
            )
        # except Exception:
        #     return ResponseObject()
        

class PageObject(graphene.ObjectType):
    number = graphene.Int()
    has_next_page = graphene.Boolean()
    has_previous_page = graphene.Boolean()
    next_page_number = graphene.Int()
    previous_page_number = graphene.Int()

    def get_page(page_object):

        previous_page_number = 0
        next_page_number = 0

        if page_object.number > 1:
            previous_page_number = page_object.previous_page_number()

        try:
            next_page_number = page_object.next_page_number()
        except:
            next_page_number + page_object.number

        return PageObject(
            number=page_object.number,
            has_next_page=page_object.has_next(),
            has_previous_page=page_object.has_previous(),
            next_page_number=next_page_number,
            previous_page_number=previous_page_number,
        )


    
    

