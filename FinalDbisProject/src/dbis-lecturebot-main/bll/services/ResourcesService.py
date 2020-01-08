from bll.dto.ResourceDTO import ResourceDTO

from dal.models.Resource import Resource
from dal.repositories.ResourceRepository import ResourceRepository


# noinspection PyBroadException
class ResourcesService:
    def __init__(self):
        self.resource_repository = ResourceRepository()

    def get_all_user_resources(self, login):
        resources = self.resource_repository.get_resources_by_foreign_key(login)
        mapped_resources = [ResourceDTO(
            url=resource.URL,
            description=resource.Description,
            times_visited=resource.TimesVisited,
            creation_date=resource.Creation_Date
        ) for resource in resources]

        return mapped_resources

    def get_count_of_user_resources(self, login):
        resources = self.get_all_user_resources(login)
        return len(resources)

    def increase_visit_times(self, login, resource):
        resource_to_edit = self.resource_repository.get_resources_by_keys(login, resource.URL)[0]

        try:
            resource_to_edit.TimesVisited += 1
            self.resource_repository.update_resource_fields(resource_to_edit)
            return "Lecture was successfully edited!", 200
        except Exception:
            return "Oops, something went wrong!", 500

    def add_resource(self, login, new_resource):
        resource = self.resource_repository.get_resources_by_keys(login, new_resource.URL)

        if len(resource) != 0:
            return "Resource with this URL already exists!", 400
        else:
            resource_to_insert = Resource(
                url=new_resource.URL,
                description=new_resource.Description,
                times_visited=new_resource.TimesVisited,
                creation_date=new_resource.Creation_Date,
                user_login=login
            )

            try:
                self.resource_repository.insert_resource(resource_to_insert)
                return "Resource was successfully added!", 200
            except Exception:
                return "Oops, something went wrong!", 500

    def edit_resource(self, login, old_url, new_resource):
        resource = self.resource_repository.get_resources_by_keys(login, new_resource.URL)

        if len(resource) == 0:
            return "Resource with this URL already exists!", 400
        else:
            try:
                if old_url != new_resource.URL:
                    self.resource_repository.delete_resource_by_keys(login, old_url)

                    resource_to_insert = Resource(
                        url=new_resource.URL,
                        description=new_resource.Description,
                        times_visited=new_resource.TimesVisited,
                        creation_date=new_resource.Creation_Date,
                        user_login=login
                    )

                    self.resource_repository.insert_resource(resource_to_insert)
                    return "Resource was successfully added!", 200
                else:
                    resource_to_update = Resource(
                        url=new_resource.URL,
                        description=new_resource.Description,
                        times_visited=new_resource.TimesVisited,
                        creation_date=new_resource.Creation_Date,
                        user_login=login
                    )

                    self.resource_repository.update_resource_fields(resource_to_update)
                    return "Resource was successfully edited!", 200
            except Exception:
                return "Oops, something went wrong!", 500

    def delete_resource(self, login, url):
        self.resource_repository.delete_resource_by_keys(login, url)
