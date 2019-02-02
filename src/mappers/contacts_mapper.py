from mappers.mapper import Mapper


class ContactsMapper(Mapper):

    def model_mapping(self):
        if self.view and self.model:
            self.model_val_assign('id')
            self.model_val_assign('name')
            self.model_val_assign('email')
            self.model_val_assign('mobile')
            self.model_val_assign('phone')
            self.model_val_assign('createdOn')
            self.model_val_assign('updatedOn')