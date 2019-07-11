import datetime as dt


class Task:

    def __init__(self, name, deadline):

        self.name = name
        if "," in deadline:
            self.temp = deadline.split(",")
            if len(self.temp) == 4:
                self.deadline = dt.datetime(year=dt.datetime.now().year, month=int(
                    self.temp[1]), day=int(self.temp[0]), hour=int(self.temp[2]), minute=int(self.temp[3]))

            elif len(self.temp) == 2:
                self.deadline = dt.datetime(year=dt.datetime.now(
                ).year, month=int(self.temp[1]), day=int(self.temp[0]))
            else:
                self.deadline = "Ei dedistä"

        else:
            self.deadline = deadline

    def __repr__(self):
        return str(self.name) + ", dedis : " + str(self.deadline)
