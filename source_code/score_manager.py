import os

app_folder = os.path.dirname(os.path.dirname(__file__))


class HighScoreManager:
    def __init__(self) -> None:
        """Reads contents of file with HS"""

        self.path_to_file = app_folder + "/high_score/high_score_tracker.txt"
        self.hs_document = open(self.path_to_file, "r")
        self.high_score = int(self.hs_document.readline())
        self.hs_document.close()

    def check_highcore(self, hs_to_check) -> None:
        """If passed HS > current HS, rewrite the file with new HS"""

        self.hs_document = open(self.path_to_file, "r")
        self.high_score = int(self.hs_document.readline())
        self.hs_document.close()

        if self.high_score < hs_to_check:
            self.hs_document = open(self.path_to_file, "w")
            self.hs_document.write(str(hs_to_check))
            self.hs_document.close()

    def get_highscore(self):
        return self.high_score
