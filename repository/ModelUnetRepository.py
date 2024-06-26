from sqlalchemy.orm import sessionmaker

from model.model import ModelUnet
from repository import ENGINE
from repository.abstractRepository import AbstractRepository


class ModelUnetRepository(AbstractRepository):

    def __init__(self, doctor_id):
        self.session = sessionmaker(bind=ENGINE)()
        self.doctor = doctor_id

    def get(self, id_model):
        self.session.connection()
        get: ModelUnet = self.session.query(ModelUnet).get(id_model)
        self.session.close()
        return get

    def add(self, data: ModelUnet):
        print('add: ')
        print(data)
        self.session.connection()
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        self.session.close()
        return data

    def update(self, new_history: ModelUnet):
        self.session.connection()
        # Получение истории обучения по id
        history: ModelUnet = self.session.query(ModelUnet).get(new_history.id)

        # Обновление данных
        if new_history:
            if new_history.current_epochs is not None:
                history.current_epochs = new_history.current_epochs
            if new_history.total_epochs is not None:
                history.total_epochs = new_history.total_epochs
            if new_history.status:
                history.status = new_history.status
            if new_history.date_train is not None:
                history.date_train = new_history.date_train
            if new_history.quality_dataset is not None:
                history.quality_dataset = new_history.quality_dataset
            if new_history.quality_valid_dataset is not None:
                history.quality_valid_dataset = new_history.quality_valid_dataset
            if new_history.quality_train_dataset is not None:
                history.quality_train_dataset = new_history.quality_train_dataset
            if new_history.num_classes is not None:
                history.num_classes = new_history.num_classes
            if new_history.time_train is not None:
                history.time_train = new_history.time_train
            if new_history.output_size is not None:
                history.output_size = new_history.output_size
            if new_history.input_size is not None:
                history.input_size = new_history.input_size
            if new_history.name_file is not None:
                history.name_file = new_history.name_file
        # ------------

        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        self.session.close()
        return history

    def get_last_history_train(self) -> ModelUnet:
        self.session.connection()
        m = self.session.query(ModelUnet).order_by(ModelUnet.id.desc()).first()
        self.session.close()
        if m:
            return m
        return ModelUnet()

    def get_history_by_version(self, version) -> ModelUnet:
        m = self.session.query(ModelUnet).filter(ModelUnet.version == version).first()
        return m

    def all_history(self) -> list[ModelUnet]:
        self.session.connection()
        m = self.session.query(ModelUnet).order_by(ModelUnet.id.desc()).all()
        self.session.close()
        return m

    def delete_by_id(self, id_model):
        self.session.connection()
        print('ИД: ========== ' + str(id_model))
        model = self.session.query(ModelUnet).filter(ModelUnet.id == id_model).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            self.session.close()
            return {'status': 'ok'}
        else:
            return {'status': 'error'}


if __name__ == '__main__':
    p = ModelUnetRepository(1)
    sss = p.get_last_history_train()
    print(sss)
