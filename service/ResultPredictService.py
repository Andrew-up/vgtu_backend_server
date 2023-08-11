import json

from repository.ResultPredictRepository import ResultPredictRepository
from model.model import ResultPredict


class ResultPredictService(object):

    def __init__(self, doctor_id):
        self.doctor = doctor_id

    def getAll(self) -> list[ResultPredict]:
        repo = ResultPredictRepository(self.doctor)
        return repo.find_all()

    # def getAllNotNull(self) -> list[ResultPredictDTO]:
    #     repo = ResultPredictRepository(self.doctor)
    #     listg = repo.find_all_not_null()
    #     lists: list[ResultPredictDTO] = []
    #     for i in listg:
    #         h = ResultPredictDTO(**i.__dict__).getDto().__dict__
    #         lists.append(h)
    #     return lists


if __name__ == '__main__':
    p = ResultPredictService(1)
    print(p.getAll())
    pass
