class Mapper:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def model_val_assign(self, param):
        print(param, ':', self.view.get(param))
        if self.view.get(param) is not None:
            setattr(self.model, param, self.view[param])