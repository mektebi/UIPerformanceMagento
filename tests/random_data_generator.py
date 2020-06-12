import names

class DataGenerator:

    def firstname_generator(self):
        name = names.get_first_name()
        return name

    def lastname_generator(self):
        surname = names.get_last_name()
        return surname

    def email_generator(self):
        email= self.firstname_generator() + self.lastname_generator() + "@yopmail.com"
        return email