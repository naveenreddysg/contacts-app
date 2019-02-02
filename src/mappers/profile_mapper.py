from mappers.mapper import Mapper


class ProfileMapper(Mapper):

    def model_mapping(self):
        if self.view and self.model:
            self.model_val_assign('id')
            self.model_val_assign('email')
            self.model_val_assign('password')
            self.model_val_assign('name')
            self.model_val_assign('createdOn')
            self.model_val_assign('updateOn')