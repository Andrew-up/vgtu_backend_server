import inspect
import os
import sys

# Use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(
    os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from sqlalchemy import Column, Integer, String, BLOB, ForeignKey, Float
from sqlalchemy.orm import relationship
from definitions import DATABASE_DIR
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Patient(Base, SerializerMixin):
    __tablename__ = 'Patient'
    id_patient: int = Column(Integer, primary_key=True)
    firstname: str = Column(String(250))
    surname: str = Column(String(250))
    middlename: str = Column(String(250))
    gender: str = Column(String(50))
    date_of_birth: str = Column(String(250))
    address: str = Column(String(250))
    phone: str = Column(String(250))
    polis_oms: str = Column(String(250))
    snils: str = Column(String(250))
    document: str = Column(String(250))
    dianosis: str = Column(String(250))
    date_healing_start: str = Column(String(250))
    date_healing_end: str = Column(String(250))
    history: list["HealingHistory"] = relationship("HealingHistory", back_populates="patient", cascade="all,delete")
    doctor: "Doctor" = relationship("Doctor", back_populates="patient", uselist=False)
    photo: bytearray = Column(BLOB)

    serialize_rules = ('-history', '-doctor', '-photo')


# Результат распознавания нейронной сети
class ResultPredict(Base, SerializerMixin):
    __tablename__ = 'Result_predict'
    id_category: int = Column(Integer, primary_key=True)
    name_category_eng: str = Column(String(50))
    name_category_ru: str = Column(String(50))
    annotations: list["Annotations"] = relationship("Annotations", back_populates="result_predict")
    color: str = Column(String(50))

    serialize_rules = ('-annotations.result_predict', '-annotations.history_nn')


# История распознавания нейронной сети

class HistoryNeuralNetwork(Base, SerializerMixin):
    __tablename__ = 'History_neural_network'
    id_history_neural_network: int = Column(Integer, primary_key=True)
    photo_original: bytearray = Column(BLOB)
    photo_predict: bytearray = Column(BLOB)
    photo_predict_edit_doctor: bytearray = Column(BLOB)
    healing_history: "HealingHistory" = relationship("HealingHistory", back_populates="history_neutral_network",
                                                     uselist=False)
    annotations: list["Annotations"] = relationship("Annotations", back_populates="history_nn")


# История лечения пациента
class HealingHistory(Base, SerializerMixin):
    __tablename__ = 'Healing_history'
    id_healing_history: int = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey(Patient.id_patient))
    history_neural_network_id: int = Column(Integer, ForeignKey(HistoryNeuralNetwork.id_history_neural_network))
    """
    Внешний ключ, связь по :class:`HistoryNeuralNetwork.id_history_neural_network`
    """
    history_neutral_network: list[HistoryNeuralNetwork] = relationship(HistoryNeuralNetwork,
                                                                       back_populates="healing_history")
    patient: list[Patient] = relationship(Patient, back_populates="history")
    doctor: "Doctor" = relationship("Doctor", back_populates="healing_history", uselist=False)
    comment: str = Column(String(500))
    date: str = Column(String(100))

    serialize_rules = ('-doctor',
                       '-patient',
                       '-history_neutral_network.annotations.history_nn',
                       '-history_neutral_network.annotations.result_predict.annotations',
                       '-history_neutral_network.healing_history')


class Annotations(Base, SerializerMixin):



    __tablename__ = 'Annotations_image'


    id_annotations: int = Column(Integer, primary_key=True)
    area: str = Column(Float(500))
    """
    Пример::
    
        5230.5
    """
    bbox: str = Column(String(500))
    """
    Пример::
    
        [91, 235, 142, 82]
    """
    segmentation: str = Column(String(500))
    """
    Пример::

         [91.0, 316.0, 121.0, 235.0, 232.0, 284.0, 91.0, 316.0]
     """
    history_nn_id: int = Column(Integer, ForeignKey(HistoryNeuralNetwork.id_history_neural_network))
    """
    Внешний ключ, связь по :class:`HistoryNeuralNetwork.id_history_neural_network`
    """
    history_nn: HistoryNeuralNetwork = relationship("HistoryNeuralNetwork", back_populates="annotations", uselist=False)
    category_id: str = Column(Integer, ForeignKey(ResultPredict.id_category))
    """
    Внешний ключ, связь по :class:`ResultPredict.id_category`
    """
    result_predict: ResultPredict = relationship(ResultPredict, back_populates="annotations", uselist=False)


# Профиль доктора
class Doctor(Base, SerializerMixin):
    __tablename__ = 'Doctor'
    id_doctor: int = Column(Integer, primary_key=True)
    firstname: str = Column(String(250))
    surname: str = Column(String(250))
    middlename: str = Column(String(250))
    photo: bytearray = Column(BLOB)
    patient_id: int = Column(Integer, ForeignKey(Patient.id_patient))
    """
    Внешний ключ, связь по :class:`Patient.id_patient`
    """
    patient: list[Patient] = relationship(Patient, back_populates="doctor")
    healing_history_id: int = Column(Integer, ForeignKey(HealingHistory.id_healing_history))
    healing_history: list[HealingHistory] = relationship(HealingHistory, back_populates="doctor")


class ModelUnet(Base, SerializerMixin):
    __tablename__ = 'Model_unet'
    id: int = Column(Integer, primary_key=True)
    version: str = Column(String(50))
    name_file: str = Column(String(50))
    accuracy: float = Column(Float(50))
    date_train: str = Column(String(100))
    quality_dataset: int = Column(Integer)
    quality_train_dataset: int = Column(Integer)
    quality_valid_dataset: int = Column(Integer)
    current_epochs: str = Column(Integer)
    total_epochs: int = Column(Integer)
    time_train: str = Column(String(50))
    num_classes: int = Column(Integer)
    input_size: str = Column(String(50))
    output_size: str = Column(String(50))
    status: str = Column(String(50))
    path_dataset: str = Column(String(250))


def init_db():
    engine = create_engine(f"sqlite:///{DATABASE_DIR}", echo=True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    # tyfyvhjgb()
    init_db()
