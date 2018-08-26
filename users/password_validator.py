from django.core.exceptions import ValidationError


class MinimumLengthValidator:
    min_length = 8

    @classmethod
    def validate(cls, password):
        if len(password) < cls.min_length:
            return False
        return True
            # raise ValidationError(
            #     "The password must contain at least %(min_length)d characters.",
            #     code='password_too_short',
            #     params={'min_length': cls.min_length},
            # )

class NumericPasswordValidator:

    @classmethod
    def validate(cls, password):
        return any(i.isdigit() for i in password)
#     def normalmethod(self):
#         print(self.min_length)
#         print("hau!")
#
#     @staticmethod
#     def static_method():
#         # cls.min_length
#         # self.min_length
#         print("hau!")
#
# def static_method():
#     print("hau!")
