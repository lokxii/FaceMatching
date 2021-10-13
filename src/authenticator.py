from src.model import *
from src.dataset import *
from torch.utils.data import DataLoader

class Authenticator():

    def __init__(self, batch_size, threshold, path):
        self.batch_size = batch_size
        self.user_id = ""
        self.user_dict = {}
        self.threshold =  threshold
        self.matching = False

        self.save_path = path
        self.model = SiameseNet()
        load_checkpoint(self.save_path, self.model)


    def isLoggedIn(self):
        return self.user_id != ""


    def login(self, user_id):
        self.user_id = user_id
        print(f"{user_id} login")


    def logout(self):
        print(f"{self.user_id} logout")
        self.user_id = ""


    def get_user_id(self):
        return self.user_id


    def register(self, user_id, frames):
        self.user_dict[user_id] = frames


    def can_match(self):
       return not self.isLoggedIn() and not self.matching


    def match(self, frame):
        if not self.can_match():
            return
        self.matching = True

        # Loop for each user
        for (user_id, frames) in self.user_dict.items():
            print("Matching {}".format(user_id))
            dataset = FaceDataset(frames, frame)
            loader = DataLoader(
                    dataset,
                    batch_size=self.batch_size,
                    shuffle=False)
            count = self.__pred__(loader)
            if count > self.batch_size * 0.8:
                self.login(user_id)
                break

        self.matching = False
        return self.isLoggedIn()


    def __pred__(self, loader):
        self.model.eval()
        all_outputs = torch.empty(0)
        for images1, images2, _ in loader:
            outputs = self.model((images1, images2))
            all_outputs = torch.cat((all_outputs, outputs))
        casted_outputs = torch.where(all_outputs > self.threshold, 1, 0)
        return torch.sum(casted_outputs)
