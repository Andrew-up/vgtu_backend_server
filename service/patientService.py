import ast

from model.model import Patient, Annotations, HistoryNeuralNetwork, HealingHistory
from repository.PatientRepository import PatientRepository


class PatientService(object):

    def __init__(self, doctor_id):
        self.doctor = doctor_id
        self.patient_repo = PatientRepository(self.doctor)

    def getById(self, item_id) -> Patient:
        # repo = PatientRepository(self.doctor)
        dto = self.patient_repo.get(item_id)
        return dto

    def getAll(self) -> list[Patient]:
        repo = PatientRepository(self.doctor)
        listg = repo.find_all()
        return listg

    def add(self, patient: dict) -> Patient:
        patient = {p: patient.get(p) for p in patient if patient.get(p)}
        new_patient: Patient = self.patient_repo.add(Patient(**patient))
        return new_patient

    def deletePatientById(self, id_patient):
        result_delete = self.patient_repo.delete_by_id(id_patient=id_patient)
        return result_delete

    def addHealingHistoryPatient(self, history: dict):
        history_neutral_network: dict = history['history_neutral_network']
        history_neutral_network.pop('healing_history', None)
        history_neutral_network.pop('id_history_neural_network', None)
        history_neutral_network.pop('healing_history_id', None)
        history.pop('patient', None)
        history.pop('doctor', None)

        if 'photo_original' in history_neutral_network:
            history_neutral_network['photo_original'] = ast.literal_eval(history_neutral_network['photo_original'])
        if 'photo_predict' in history_neutral_network:
            history_neutral_network['photo_predict'] = ast.literal_eval(history_neutral_network['photo_predict'])
        if 'photo_predict_edit_doctor' in history_neutral_network:
            if history_neutral_network['photo_predict_edit_doctor']:
                history_neutral_network['photo_predict_edit_doctor'] = ast.literal_eval(
                    history_neutral_network['photo_predict_edit_doctor'])

        result_anns: list[Annotations] = []
        for j in history_neutral_network['annotations']:
            j.pop('category', None)
            j.pop('result_predict', None)
            j.pop('id_annotations', None)
            j['bbox'] = str(j['bbox'])
            j['area'] = str(j['area'])
            j['segmentation'] = str(j['segmentation'])
            anns = Annotations(**j)
            result_anns.append(anns)

        history_neutral_network['annotations'] = result_anns
        hnn = HistoryNeuralNetwork(**history_neutral_network)
        history['history_neutral_network'] = hnn

        hist = HealingHistory(**history)
        new_history = self.patient_repo.addHealingHistoryPatient(hist)

        return 'ok'


if __name__ == '__main__':
    p = PatientService(1)
    p.getAll()

    pass
