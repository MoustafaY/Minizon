class BaseService:
    def __init__(self, repository):
        self.repository = repository

    def get_all(self):
        instances = self.repository.get_all()
        return [self.format_output(instance) for instance in instances]

    def get_by_id(self, id):
        instance = self.repository.get_by_id(id)
        return self.format_output(instance)

    def create(self, **kwargs):
        instance = self.repository.create(**kwargs)
        return self.format_output(instance)

    def update(self, id, **kwargs):
        instance = self.repository.get_by_id(id)
        newInstance = self.repository.update(instance, **kwargs)
        return self.format_output(newInstance)

    def delete(self, id):
        instance = self.repository.get_by_id(id)
        self.repository.delete(instance)
    
    def reset(self):
        self.repository.reset()
    
    def save(self):
        self.repository.save()
    
    def formatOutput(self, instance):
        return instance.to_dict() if instance else None
