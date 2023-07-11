import json

from  model.model  import HealingHistory, HistoryNeuralNetwork, ResultPredict
from dto.HistoryNeutralNetworkDTO import HistoryNeutralNetworkDTO


class HealingHistoryDTO(object):

    def __init__(self, **entries):
        self.id_healing_history: int = int()
        self.patient_id: int = int()
        self.comment: str = str()
        self.date: str = str()
        self.history_neural_network_id: int = int()
        self.doctor = None
        self.history_neutral_network = None
        self.__dict__.update(entries)

    def getHealingHistory(self):
        h = HealingHistory()
        h.patient_id = self.patient_id
        h.comment = self.comment
        h.doctor = self.doctor
        h.date = self.date
        if self.history_neutral_network is not None:
            h.history_neutral_network = HistoryNeutralNetworkDTO(**self.history_neutral_network).getHistoryNeutralNetwork()
        return h

    def getDto(self):
        dto = HealingHistoryDTO()
        dto.id_healing_history = self.id_healing_history
        dto.patient_id = self.patient_id
        dto.comment = self.comment
        dto.date = self.date
        dto.history_neural_network_id = self.history_neural_network_id
        if self.history_neutral_network is not None:
            dto.history_neutral_network = HistoryNeutralNetworkDTO(**self.history_neutral_network.__dict__).getDto().__dict__
        return dto

