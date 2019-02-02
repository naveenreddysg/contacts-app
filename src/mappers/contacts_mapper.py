from mappers.mapper import Mapper


class ContactsMapper(Mapper):

    def model_mapping(self):
        if self.view and self.model:
            self.model_val_assign('id')